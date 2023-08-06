import websockets
import websocket
import json
import re
import random
import argparse
import sys
from attrdict import AttrDict
import attrdict
from getpass import getpass
from queue import Queue
from threading import *
from colorama import Fore, init, Style

init()

class Bot:

    @staticmethod
    def randomize_between(*responses):
        response = random.choice(responses)
        return response

    def __init__(self, nick, **kwargs):
        vars = ["userEmail",
            "userPassword",
            "help",
            "ping",
            "killed",
            "function",
            "_cookie",
            "human",
            "_copy",
            "sendable",
            "APITimeout",
            "advanced",
            "owner",
            "important",
            "killChildren",
            "queue"]
        noneVars = ["userEmail",
            "userPassword",
            "help",
            "ping",
            "killed",
            "function",
            "_cookie"]
        self.nick = nick
        self.normname = re.sub(r"\s+", "", self.nick)
        self.owner = "nobody"
        self.handlers = {}
        self.children = []
        self.important = False
        self.APITimeout = 10
        self.advanced = False
        self.sendable = False
        self.childThreads = []
        self.parents = []
        self.parentThreads = []
        self.conn = None
        self.human = False
        self._regexes = {}
        self._copy = False
        self.killChildren = False
        self.queue = Queue()
        for item in vars:
            if item in kwargs:
                setattr(self, item, kwargs[item])
            elif item in noneVars:
                setattr(self, item, None)
        self.normowner = re.sub(r"\s+", "", self.owner)
        self.parser = argparse.ArgumentParser(description=f'{nick}: A euphoria.io bot.' if 'description' not in kwargs else kwargs['description'])
        if 'customArgs' in kwargs and kwargs['customArgs']:
            self.room = "bots" if "room" not in kwargs else kwargs["room"]
            self.password = "" if "password" not in kwargs else kwargs["password"]
        else:
            self.add_command_line_arg("--test", "--debug", "-t", help = "Used to debug dev builds. Sends bot to &test instead of its default room.", action = 'store_true')
            self.add_command_line_arg("--room", "-r", help = f"Set the room the bot will be placed in. Default: {'bots' if 'room' not in kwargs else kwargs['room']}", default = "bots" if "room" not in kwargs else kwargs["room"])
            self.add_command_line_arg("--password", "-p", help = "Set the password for the room the bot will be placed in.", default = "" if "password" not in kwargs else kwargs["password"])
            self.args = self.parser.parse_args()
            self.room = self.args.room if self.args.test != True or self._copy else "test"
            self.password = self.args.password
            if not self._copy:
                self.log(f"Debug: {str(self.args.test)}")

    def _wait_for(self, response):
        if self.conn.sock:
            reply = None
            i = 0
            waitlist = Queue()
            for msgJSON in self.conn:
                i += 1
                msg = AttrDict(json.loads(msgJSON))
                if msg.type == response:
                    reply = msg
                    break
                else:
                    waitlist.put(msg)
                if i > self.APITimeout:
                    self.log(f"{response} API response not recorded. reason: too many events before {response}.", error = True)
                    reply = None
                    break
            while not waitlist.empty():
                self._handle(waitlist.get())
            return reply
        else:
            return None

    def _recv(self):
        try:
            msg = AttrDict(json.loads(self.conn.recv()))
            self.queue.put(msg)
            return msg
        except json.decoder.JSONDecodeError:
            self.kill()

    def _handle(self, msg):
        if msg is None:
            return
        if msg.type == 'send-event':
            if re.search(f'^!kill @{re.escape(self.normname)}$', msg.data.content) is not None:
                self._handle_kill(msg)
            if re.search(f'^!forcekill @{re.escape(self.normname)}$', msg.data.content) is not None:
                self.kill()
            if re.search(f'^!restart @{re.escape(self.normname)}$', msg.data.content) is not None:
                self.restart(msg = msg)
                raise KilledError(bot = self, message = f"old {self.nick} in &{self.room} killed. Restarted.")
        if msg.type == 'error':
            self.log(msg, error = True)
        elif msg.type in self.handlers:
            self.handlers[msg.type](msg)
        else:
            if callable(self.function):
                self.function(msg)
            else:
                self.log("Advanced start must be given a callable message handler function that takes an AttrDict as its argument.", error = True)

    def _is_privileged(self, user):
        if "is_manager" in user or user.name == self.owner:
            return True
        else:
            return False

    def _handle_ping(self, msg):
        self.send_command(type = 'ping-reply', data = {'time': msg.data.time})

    def _handle_message(self, msg):
        if re.search('^!ping$', msg.data.content) is not None or re.search(f'^!ping @(?i){re.escape(self.normname)}$', msg.data.content) is not None:
            self.send_msg(self.ping, parent = msg)
        if re.search(f'^!help @(?i){re.escape(self.normname)}$', msg.data.content) is not None:
            self.send_msg(self.help, parent = msg)
        if re.search(f'^!send @(?i){re.escape(self.normname)} &(\w+)$', msg.data.content) is not None and self.sendable:
            self.move_to(re.search(f'^!send @(?i){re.escape(self.normname)} &(\w+)$', msg.data.content).group(0))
        for regex, response in self._regexes.items():
            if re.search(regex, msg.data.content) is not None:
                if callable(response):
                    result = response(self, msg, re.search(regex, msg.data.content))
                    if isinstance(result, str):
                        self.send_msg(msgString = result, parent = msg)
                    elif isinstance(result, dict):
                        for send, nick in result.items():
                            self.set_nick(nick)
                            self.send_msg(send, parent = msg)
                        self.set_nick(self.nick)
                    elif isinstance(result, list):
                        for send in result:
                            self.send_msg(send, parent = msg)
                else:
                    if isinstance(response, str):
                        self.send_msg(msgString = response, parent = msg)
                    elif isinstance(response, dict):
                        for send, nick in response.items():
                            self.set_nick(nick)
                            self.send_msg(send, parent = msg)
                        self.set_nick(self.nick)
                    elif isinstance(response, list):
                        for send in response:
                            self.send_msg(send, parent = msg)
                    else:
                        raise BadMessageError(message = f"Response type: {type(response)}", bot = self)
                break

    def _handle_kill(self, msg):
        if self._is_privileged(msg.data.sender) or not self.important:
            self.send_msg(self.killed, msg)
            self.kill()
        else:
            self.send_msg(f"Bot not killed because you are not a host or @{self.normowner}, and this bot is marked as important.\nFor emergencies, use !forcekill.", parent = msg)

    def _handle_auth(self, pw):
        self.send_command(type = 'auth', data = {'type': 'passcode', 'passcode': pw})
        reply = self._wait_for("auth-reply")
        if reply is not None:
            if reply.data.success == True:
                self.log(f'Successfully logged into {self.room}.')
            else:
                self.log(f'Login unsuccessful. Reason: {reply.data.reason}', error = True)
                self._handle_auth(getpass("Enter the correct password: "))

    def log(self, message, error = False):
        print(f'{Fore.RED if error else Style.RESET_ALL}{"COPY: " if self._copy else ""}{message}{Style.RESET_ALL}')
        sys.stdout.flush()

    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws{"?h=0" if not self.human else "?h=1"}', cookie = self._cookie, enable_multithread = True)
        if self._cookie is None:
            self._cookie = self.conn.headers['set-cookie']
        hello = self._recv()
        reply = self._recv()
        self._handle_ping(reply)
        reply = self._recv()
        if reply.type == "snapshot-event":
            self.set_nick(self.nick)
        elif reply.type == "bounce-event":
            self._handle_auth(self.password)
            self.set_nick(self.nick)
        else:
            self.log(reply, error = True)
        self.log(f'connected to &{self.room}.')
        return hello

    def start(self, function = None, advanced = False):
        if not advanced and not self.advanced:
            self.set_handler('ping-event', self._handle_ping)
            self.set_handler('send-event', self._handle_message)
            self.set_handler('bounce-event', self._handle_auth)
            self.function = lambda msg: None
        else:
            if self.function is None and function is not None and callable(function):
                self.function = function
            else:
                self.log("No valid function passed to advanced bot's start function. Using filler function")
                self.function = lambda msg: None
        try:
            while True:
                msg = self._recv()
                self._handle(msg)
        except KilledError:
            pass

    def start_in_new_thread(self, function = None, advanced = False):
        t = Thread(target = self.start, kwargs = {"function": function, "advanced" : advanced}, name = f"{self.nick} in &{self.room}")
        t.start()
        t.join(0)
        return t

    def kill(self):
        if self.killChildren:
            for child in self.children:
                if copy.conn is not None and copy.conn.sock:
                    copy.conn.close()
                    copy.conn = None
        if self.conn is not None and self.conn.sock:
            self.conn.close()
        self.conn = None
        raise KilledError(message = f'{self.nick} in &{self.room} killed.', bot = self)

    def send_msg(self, msgString, parent = None):
        try:
            if isinstance(parent, AttrDict):
                self.send_command(data = {'content': msgString, 'parent': parent.data.id})
                reply = self._wait_for("send-reply")
                self.log(f'Message sent: {reply} replying to: {parent.data.id} by {parent.data.sender.name}')
            elif isinstance(parent, str):
                self.send_command(data = {'content': msgString, 'parent': parent})
                reply = self._wait_for("send-reply")
                self.log(f'Message sent: {reply} replying to: {parent}')
            elif parent is None:
                self.send_command(data = {'content': msgString})
                reply = self._wait_for("send-reply")
                self.log(f'Message sent: {reply}')
            else:
                raise BadMessageError(message = f'message not sent, because type of parent was {type(parent)}. \nParent printed: \n{parent}', bot = self)
        except BadMessageError:
            pass

    def restart(self, msg = None, advanced = False):
        if self.conn is not None:
            self.conn.close(timeout = 0)
            self.conn = None
            self.log("restarting...")
        else:
            self.log("starting...")
        self.connect()
        t = Thread(target = self.start, kwargs = {"advanced" : advanced}, name = f"{self.nick} in &{self.room}")
        t.start()
        t.join(0)

    def add_command_line_arg(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)
        self.args = self.parser.parse_args()
        if "name" in kwargs:
            return self.args.kwargs["name"]
        else:
            return self.args

    def send_command(self, type = "send", data = {}):
        self.conn.send(json.dumps({'type' : type, 'data' : data}))

    def set_regexes(self, regexes):
        self._regexes = regexes
        if self.help is None:
            if f"^!help @{re.escape(self.normname)}$" in regexes:
                self.help = regexes[f"^!help @{re.escape(self.normname)}$"]
            else:
                self.help = f"@{self.normname} is a bot made with Doctor Number Four's Python 3 bot library, DocLib (link: https://github.com/milovincent/DocLib) by @{self.normowner}.\nIt follows botrulez and does not have a custom !help message yet."
        if self.ping is None:
            if '^!ping$' in regexes:
                self.ping = regexes['^!ping$']
            elif f'^!ping @{re.escape(self.normname)}$' in regexes:
                self.ping = regexes[f'^!ping @{re.escape(self.normname)}$']
            else:
                self.ping = "Pong!"
        if self.killed is None:
            if f"^!kill @{re.escape(self.normname)}$" in regexes:
                self.killed = regexes[f"^!kill @{re.escape(self.normname)}$"]
            else:
                self.killed = "/me has died."

    def set_nick(self, nick):
        self.send_command(type = 'nick', data = {'name': nick})

    def get_userlist(self):
        self.send_command(type = 'who')
        reply = self._wait_for("who-reply")
        if reply is not None:
            return reply.data.listing

    def move_to(self, roomName, password = "", _copyStart = False):
        self.room = roomName
        self.password = password
        self.restart()
        if _copyStart:
            self.log(f"Copy started in &{self.room}.")

    def set_handler(self, eventString, function):
        if callable(function):
            self.handlers[eventString] = function
        else:
            self.log(f"WARNING: handler for {eventString} not callable, handler not set.", error = True)

    def set_handlers(self, handlers):
        for eventString, function in handlers.items():
            self.set_handler(eventString, function)

    def copy_to(self, roomName, password = None):
        copy = Bot(nick = self.nick,
            room = roomName,
            owner = self.owner,
            userEmail = self.userEmail,
            userPassword = self.userPassword,
            password = self.password if password is None else password,
            help = self.help,
            ping = self.ping,
            important = self.important,
            killed = self.killed,
            APITimeout = self.APITimeout,
            advanced = self.advanced,
            function = self.function,
            sendable = self.sendable,
            _copy = True,
            _cookie = self._cookie,
            human = self.human
            queue = self.queue)
        copy.set_handlers(self.handlers)
        copy.set_regexes(self._regexes)
        self.children.append(copy)
        copy.parents.append(self)
        copy.parentThreads.append(current_thread())
        return copy

    def login(self, email = None, password = None, setDefaults = False):
        if email is not None and password is not None:
            self.send_command(type = 'login', data = {'namespace' : "email", 'id' : email, 'password' : password})
            if setDefaults:
                self.userEmail = email
                self.userPassword = password
        elif (self.userEmail is not None and email is None) or (self.userPassword is not None and password is None):
            self.login(email = self.userEmail if email is None else email, password = self.userPassword if password is None else password, setDefaults = setDefaults)
        else:
            self.login(email = input("Enter your email: ") if email is None else email, password = getpass("Enter your password: ") if password is None else password, setDefaults = setDefaults)
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "login-reply":
                reply = msg
                if reply.data.success:
                    self.log("Login successful.")
                    self.account = reply.data.account_id
                else:
                    self.log(f"Access denied. Reason: {reply.data.reason}", error = True)
                    self.login(email = input("Enter your email: "), password = getpass("Enter your password: "), setDefaults = setDefaults)
                return reply
            if i > self.APITimeout:
                self.log("login-reply API response not recorded. reason: too many events before pm-initiate-reply.", error = True)
                return None

    def initiate_pm(self, id, bot = None, room = "pmtest", hostEmail = None, hostPassword = None):
        copy = Bot(nick = self.nick, room = room)
        copy.connect()
        copy.login(email = hostEmail, password = hostPassword, setDefaults = False)
        copy.conn.close()
        copy.conn = None
        copy.connect()
        self.send_command(type = 'pm-initiate', data = {'user_id' : id})
        to = self._wait_for("pm-initiate-reply")
        if to is not None:
            if to.data is not None:
                if bot is not None:
                    bot.copy_to(f"pm:{to.data.pm_id}")
                else:
                    self.copy_to("pm:{to.data.pm_id}")
            else:
                self.log("Access Denied: This bot does not have permission to initiate PMs.", error = True)
        return to

class BotError(Exception):
    pass

class KilledError(BotError):
    def __init__(self, bot, message = "bot killed."):
        self.message = message
        bot.log(f'KilledError: {message}', error = True)

class BadMessageError(BotError):
    def __init__(self, bot, message):
        self.message = message
        bot.log(f'BadMessageError: {message}', error = True)
