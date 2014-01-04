from wand.image import Image

import tornado.ioloop
import tornado.web
from tornado.options import define, parse_command_line


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Imagine this!")


class ResizeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Imagine this!")


class CropHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Imagine this!")


class MagicHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Imagine this!")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/resize/", ResizeHandler),
    (r"/crop/", CropHandler),
    (r"/magic/", MagicHandler),
])


if __name__ == "__main__":
    define("port", default=5000, help="Can I haz port?", type=int)
    parse_command_line()
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()