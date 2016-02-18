import os
import settings
import motor
import tornado.httpserver
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")
 
def main():
    
    database = motor.motor_tornado.MotorClient(os.environ.get('MONGOLAB_URI'))
    application = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
        (r"/", MainHandler)
    ], database=database)
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()