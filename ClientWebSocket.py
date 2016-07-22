import txaio
from cv2 import *
import cv2
import base64
import json
import time

txaio.use_twisted()


from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory


class MyClientProtocol(WebSocketClientProtocol):


    def enviarIMG(self):


        print("Haciendo foto...")


        cam = VideoCapture(0)
        s,img = cam.read()

        if s:

            img = cv2.resize(img ,(400, 300))

            cnt = cv2.imencode('.jpeg',img)[1]
            fotourl = base64.b64encode(cnt)

            data = {'type':'FRAME',
                    'dataURL': 'data:image/jpeg;base64,'+fotourl,
                    'identity': -1}

            data_json = json.dumps(data)


            self.sendMessage(b""+data_json, isBinary=True)
            print ("Foto enviada")


    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))



    def onOpen(self):

        data = {'type':'TRAINING',
                'val': ''}

        data_json = json.dumps(data)
        self.sendMessage(b""+data_json, isBinary=True)

        for x in range(0, 15):
            self.enviarIMG()


    def onMessage(self, payload, isBinary):

        msg = json.loads(payload)
        nombre = msg.get('identificado')

        if nombre is not None:
            print(nombre)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory(u"ws://127.0.0.1:9000", debug=False)
    factory.protocol = MyClientProtocol

    reactor.connectTCP("127.0.0.1", 9000, factory)
    reactor.run()