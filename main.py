import os
import urlparse
import redis
import motor

import settings
import handlers

import tornado.httpserver
import tornado.ioloop
import tornado.web
 
def main():
    
    database = motor.motor_tornado.MotorClient(os.environ.get('MONGOLAB_URI'))
    
    url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
    redis = redis.Redis(
        host=url.hostname, 
        port=url.port, 
        password=url.password
    )
    
    application = tornado.web.Application(
        [
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
            (r"/", handlers.MainHandler)
        ], 
        database=database,
        redis=redis
    )
    
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()