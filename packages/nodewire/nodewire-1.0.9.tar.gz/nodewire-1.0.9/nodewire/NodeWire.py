'''
Copyright (c) 2016, nodewire.org
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:
   This product includes software developed by nodewire.org.
4. Neither the name of nodewire.org nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY nodewire.org ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL nodewire.org BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import time, threading
import requests
from nodewire.splitter import split, getsender, getnode
import asyncio
from nodewire.client import client
import json
import uuid
import inspect

debug = False # False for deployment

class Message:
    def __init__(self, msg):
        words = split(msg)
        self.Address = words[0]
        self.Command = words[1] if len(words)>1 else words[0]
        self.Params = words[2:-1] if len(words)>2 else words[0]
        self.Port = words[2] if len(words)>=4 else None
        try:
            self.Value = json.loads(words[3]) if len(words)>=5 else None
        except:
            self.Value = None
        self.Sender = words[-1]

    def __str__(self):
        return self.Address + ' ' + self.Command + ' ' + ' '.join(p for p  in self.Params) + ' ' + self.Sender


class NodeWire:
    def __init__(self, node_name='node', server='secure.nodewire.org', process=None):
        self.name = node_name
        self.type = node_name
        self.server_address = server
        self.gateway = ''
        self.id = 'None'
        self.callbacks = {}
        self.terminated = False
        self.client = client()
        self.called_connected =  False
        self.connected = False

        self.ack = False
        self.waiting_config = False

        try:
            self.readconfig()
            print(self.uuid)
        except Exception as ex:
            print('Failed to read configuration file. Creating new config...')
            self.uuid = str(uuid.uuid4())
            print(f'New UUID is {self.uuid}')
            self.token = 'None'
            self.name = node_name
            self.id = 'None'
            self.saveconfig()

        if self.process_command:
            self.client.received = self.process_command

        self.process = process
        self.on_connected = None
        self.debug = False

    def saveconfig(self):
        file = open('nw.cfg', 'w')
        file.write(json.dumps({
            'uuid': self.uuid,
            'token': self.token,
            'name': self.name,
            'id': self.id,
            'gateway': self.gateway
        }))
        file.close()

    def readconfig(self):
        file = open('nw.cfg', 'r')
        config = json.loads(file.read())
        self.uuid = config['uuid']
        self.token = config['token']
        self.name = config['name']
        self.id = config['id']
        self.gateway = config['gateway']
        file.close()

    async def start(self, loop):
        if self.token == 'None':
            await self.client.sendasync('cp Gateway id={}\n'.format(self.uuid))
            self.waiting_config = True
        else:
            await self.client.sendasync('cp Gateway key={} {}\n'.format(self.token, self.uuid))
        self.connected = True

    def send(self, Node, Command, *Params):
        if self.connected:
            try:
                #todo rewrite this as format function
                cmd = Node + ' ' + Command + ' ' + ' '.join(param for param in Params) + (' ' + self.name if len(Params) != 0 else self.name)
                if self.debug:print(cmd)
                self.client.send(cmd+'\n')
                return True
            except Exception as ex:
                if self.debug:print('failed to send command over LAN')
                self.connected = False
                return False

    async def pinger(self):
        if self.debug: print('pinging...')
        while not self.ack:
            self.send('cp', 'ThisIs', self.id)
            await asyncio.sleep(5)

    async def keepalive(self):
        await asyncio.sleep(60)
        while True:
            self.ack = False
            try:
                self.send('cp', 'keepalive')
            except:
                await self.start(asyncio.get_event_loop())
            await asyncio.sleep(5)
            if not self.ack:
                if self.debug: print('didn\'t recieve ack')
                self.client.close_connection()
                self.connected = False
                await self.start(asyncio.get_event_loop())
            await asyncio.sleep(300)

    def when(self, cmd, func):
        self.callbacks[cmd] = func

    async def process_command(self, cmd):
        self.last = time.time()
        if cmd == 'disconnected':
            self.connected = False
            return
        msg = Message(cmd)

        if self.debug: print(cmd)

        if msg.Command == 'ack':
            self.ack = True
        elif msg.Command == 'gack' and not self.called_connected:
            print('connected')
            if self.waiting_config:
                self.waiting_config = False
                self.gateway = msg.Address.split(':')[0]
                self.token = msg.Address.split(':')[1]
                self.saveconfig()
                self.client.close_connection()
                self.connected = False
                await self.start(asyncio.get_event_loop())
            if self.on_connected:
                self.called_connected = True
                if inspect.iscoroutinefunction(self.on_connected):
                    asyncio.create_task(self.on_connected())
                else:
                    self.on_connected()
        elif msg.Command == 'authfail':
            if self.token != 'None':
                if self.debug: print('we have been deleted')
                self.token = 'None'
                self.saveconfig()
        elif msg.Command == 'ping':
            self.ack = False
            asyncio.Task(self.pinger())
        elif msg.Command == 'get' and msg.Params[0] == 'id':
            self.send(msg.Sender, 'id', self.id)
        elif msg.Command == 'get' and msg.Params[0] == 'type':
            self.send(msg.Sender, 'type', self.type)
        elif msg.Command == 'set' and msg.Params[0] == 'id':
            self.id = msg.Params[1]
            self.saveconfig()
        elif msg.Command == 'set' and msg.Params[0] == 'name':
            self.name = msg.Params[1]
            self.saveconfig()
            self.send(msg.Sender, 'ThisIs')
        else:
            if self.process:
                self.process(msg)
        if msg.Command == 'portvalue':
            signal = (msg.Sender.split(':')[1] if ':' in msg.Sender else msg.Sender) + '.' + msg.Params[0]
            if signal in self.callbacks:
                self.callbacks[signal](msg)
        elif msg.Command in self.callbacks:
                self.callbacks[msg.Command](msg)

    async def run_async(self):
        loop = asyncio.get_event_loop()
        await asyncio.gather(
            asyncio.create_task(self.client.connect(serverHost=self.server_address)),
            asyncio.create_task(self.start(loop)),
            asyncio.create_task(self.keepalive())
        )

    def run(self, tsk=None):
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(self.client.connect(serverHost=self.server_address)),
            loop.create_task(self.start(loop)),
            loop.create_task(self.keepalive())
        ]
        if tsk:
            if self.debug: print('starting task')
            tasks+=[loop.create_task(tsk)]
        wait_tasks = asyncio.wait(tasks)
        try:
            loop.run_until_complete(wait_tasks)
        except KeyboardInterrupt:
            # Canceling pending tasks and stopping the loop
            asyncio.gather(*asyncio.Task.all_tasks()).cancel()
            # Stopping the loop
            loop.stop()
            # Received Ctrl+C
            loop.close()

if __name__ == '__main__':
    nw = NodeWire('pyNode')
    nw.debug = True
    nw.run()

