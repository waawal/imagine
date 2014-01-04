from wand.image import Image

import tornado.ioloop
import tornado.web
from tornado.options import define, parse_command_line


define("port", default=5000, help="Can I haz port?", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Imagine this!")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    parse_command_line()
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()