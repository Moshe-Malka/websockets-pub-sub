import json
import os
from datetime import datetime
from uuid import uuid4
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from autobahn.twisted.websocket import WebSocketServerProtocol

class MyServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        self.msg_counter = 0
        self.msg_buffer = []

    def custom_reducer(self):
        try:
            now = datetime.now()
            uid = str(uuid4())
            df = pd.DataFrame({
                'Timestamp': [now.isoformat()],
                'Result' : [sum([x['data']['amount'] for x in self.msg_buffer ])],
                'UID' : [uid]
            })
            table = pa.Table.from_pandas(df)
            path = f"{os.getcwd()}/{now.year}/{now.month}/{now.day}/{now.hour}/{uid}/data.parquet"
            print(f"Writting data to: {path}")
            directory = os.path.dirname(path)
            if not os.path.exists(directory): os.makedirs(directory)
            pq.write_table(table, path)
        except Exception as e:
            print(e)

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        data_json = json.loads(payload.decode('utf8'))
        print(data_json)
        if data_json['data']['organization'] == 'bank' and data_json['data']['credit_score'] == 1:
            self.msg_buffer.append(data_json)
            # TODO: uncomment this
            # if self.counter < 1000:
            if self.msg_counter < 10:
                self.msg_counter += 1
            else:
                self.custom_reducer()
                self.msg_counter = 0
                self.msg_buffer = []
        else:
            pass

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

if __name__ == '__main__':

   import sys

   from twisted.python import log
   from twisted.internet import reactor
   log.startLogging(sys.stdout)

   from autobahn.twisted.websocket import WebSocketServerFactory
   factory = WebSocketServerFactory()
   factory.protocol = MyServerProtocol

   reactor.listenTCP(9090, factory)
   reactor.run()