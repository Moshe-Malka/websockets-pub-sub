import websockets
import asyncio
from random import randint, choice
import json
import time
from uuid import uuid4

class WebSocketClient():

    def __init__(self):
        self.org_options = ['bank', 'shop', 'university', 'school']

    async def connect(self):
        '''
            Connecting to webSocket server

            websockets.client.connect returns a WebSocketClientProtocol, which is used to send and receive messages
        '''
        self.connection = await websockets.client.connect('ws://127.0.0.1:9090')
        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            # # Send greeting
            # await self.sendMessage('Hey server, this is webSocket client')
            return self.connection


    # async def sendMessage(self, message):
    #     '''
    #         Sending message to webSocket server
    #     '''
    #     await self.connection.send(message)

    async def receiveMessage(self, connection):
        '''
            Receiving all server messages and handling them
        '''
        while True:
            try:
                message = await connection.recv()
                print('Received message from server: ' + str(message))
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    async def heartbeat(self, connection):
        '''
        Sending heartbeat to server every 5 seconds
        Ping - pong messages to verify connection is alive
        '''
        while True:
            try:
                data = {
                    "id" : str(uuid4()),
                    "data" : {
                        "id" : str(uuid4()),
                        "organization" : choice(self.org_options),
                        "credit_score" : randint(1,10),
                        "amount" : randint(1,10000)
                    }
                }
                await connection.send(json.dumps(data))
                await asyncio.sleep(0.5)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break