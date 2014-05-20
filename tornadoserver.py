from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from tornado.websocket import WebSocketHandler
import logging
from labdemo import app

flask_app = WSGIContainer(app)

class PingPongSocket(WebSocketHandler):
    def open(self):
        logging.debug('New websocket connection opened.')

    def on_message(self, message):
        if(str(message) == 'Ping'):
            logging.debug('"Ping" received, "Pong" sent.')
            self.write_message('Pong')
        elif(str(message) == 'Pong'):
            logging.debug('"Pong" received, "Ping" sent.')
            self.write_message('Ping')
        else:
            logging.debug('Unknown messaged received, nothing sent.')

    def on_close(self):
        logging.debug('Existing websocket connection closed.')

application = Application([
    (r'/ws', PingPongSocket),
    (r'.*', FallbackHandler, dict(fallback=flask_app))
    ], debug=True, autoreload=True)

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.DEBUG)

if __name__ == '__main__':
    application.listen(5000, address='0.0.0.0')
    IOLoop.instance().start()
