from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from tornado.websocket import WebSocketHandler
from labdemo import app

flask_app = WSGIContainer(app)

class PingPongSocket(WebSocketHandler):
    def open(self):
        print('new websocket connection')

    def on_message(self, message):
        print(message)
        if(str(message) == 'Ping'):
            self.write_message('Pong')
        if(str(message) == 'Pong'):
            self.write_message('Ping')

    def on_close(self):
        print('websocket connection closed')

application = Application([
    (r'/ws', PingPongSocket),
    (r'.*', FallbackHandler, dict(fallback=flask_app))
    ], debug=True, autoreload=True)

if __name__ == '__main__':
    application.listen(5000, address='0.0.0.0')
    IOLoop.instance().start()
