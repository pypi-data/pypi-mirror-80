import json
from telethon import TelegramClient
from telethon.sessions.memory import MemorySession
from telethon import events

from .bot_logging import introduce_myself
from .data import Data


class Bot:
    data = Data
    steps = {}
    callback_commands = {}

    def on(self, step = '*', command = '*', callback = None):
        def inner(function):
            if callback:
                self.callback_commands[callback] = function
            else:
                self.steps.setdefault(step, {})
                self.steps[step][command] = function
            return function
        return inner


    async def connect(self, api_id, api_hash, bot_token):
        self.client = await TelegramClient(
    		MemorySession(),
    		api_id,
    		api_hash
    	).start(bot_token=bot_token)

        me = await self.client.get_me()
        introduce_myself(me)


    async def run_forever(self):
        nml, cql = self.get_functions()
        self.client.on(events.NewMessage(incoming=True))(nml)
        self.client.on(events.CallbackQuery)(cql)
        await self.client.run_until_disconnected()


    def get_functions(self):

        def enable_traceback(handler):
            async def inner(event):
                try:
                    await handler(event)
                except Exception as e:
                    print(e)
            return inner


        @enable_traceback
        async def new_message_listener(event) -> None:
            data = await self.data.build(event)

            message_text = event.message.message
            current_step = await data.current_step()

            async def find_command_on_step(step):
                commands = self.steps.get(step)
                if commands:
                    func = commands.get(message_text) or commands.get('*')
                    if func:
                        await func(event, data)
                        return True

            (await find_command_on_step(current_step)) or \
            (await find_command_on_step('*'))



        @enable_traceback
        async def callback_query_listener(event) -> None:
            data = await self.data.build(event)

            event_data = json.loads(event.data.decode('utf-8'))
            command = event_data['command']
            arguments = event_data['arguments']

            func = self.callback_commands.get(command)
            if func:
                await func(event, data, arguments)
        return new_message_listener, callback_query_listener
