from wand.image import Image

import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado.options import define, parse_command_line


class ImageProcessingMixin(object):

    def download_image(self, url):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(url, self.download_callback)

    def download_callback(self, response):
        if response.error:
            print("Error:", response.error)
            raise tornado.web.HTTPError(404, "Error: %s" % response.error)
            self.finish()
        else:
            with Image(file=response.buffer) as img:
                self.process_image(img)

    def process_image(self, img):
        raise NotImplementedError('Override me please')

    def respond_with_image(self, img):
        self.set_header('Content-Type', img.mimetype)
        self.write(img.make_blob())
        self.finish()

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Imagine this!")


class ResizeHandler(ImageProcessingMixin, tornado.web.RequestHandler):

    def process_image(self, img):
        img.transform(resize=self.proportions)
        self.respond_with_image(img)

    @tornado.web.asynchronous
    def get(self, proportions):
        self.proportions = proportions
        try:
            self.download_image(self.get_argument('img'))
        except MissingArgumentError:
            raise tornado.web.HTTPError(404, "Error: No img") # FIXME!



class CropHandler(ImageProcessingMixin, tornado.web.RequestHandler):

    def process_image(self, img):
        img.transform(crop=self.proportions)
        self.respond_with_image(img)

    @tornado.web.asynchronous
    def get(self, proportions):
        self.proportions = proportions
        try:
            self.download_image(self.get_argument('img'))
        except MissingArgumentError:
            raise tornado.web.HTTPError(404, "Error: No img") # FIXME!


class MagicHandler(ImageProcessingMixin, tornado.web.RequestHandler):

    def process_image(self, img):
        img.liquid_rescale(*self.proportions)
        self.respond_with_image(img)

    @tornado.web.asynchronous
    def get(self, proportions):
        self.proportions = [int(prop) for prop in proportions.split('x')]
        try:
            self.download_image(self.get_argument('img'))
        except MissingArgumentError:
            raise tornado.web.HTTPError(404, "Error: No img") # FIXME!


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/resize/(.*)", ResizeHandler),
    (r"/crop/(.*)", CropHandler),
    (r"/magic/(.*)", MagicHandler),
])


if __name__ == "__main__":
    define("port", default=5000, help="Can I haz port?", type=int)
    parse_command_line()
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()