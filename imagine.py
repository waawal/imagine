from wand.image import Image

import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado.options import define, parse_command_line


class ImageDownloaderMixin(object):

    def download_image(self, url):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(url, self.download_callback)

    def download_callback(self, response):
        if response.error:
            print("Error:", response.error)
            raise tornado.web.HTTPError(404, "Error: %s" % response.error)
            self.finish()
        else:
            self.process_image(Image(file=response.body))

    def process_image(self, img):
        raise NotImplementedError


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Imagine this!")


class ResizeHandler(ImageDownloaderMixin, tornado.web.RequestHandler):

    def process_image(self, img):
        img.transform(resize=self.proportions)

    @tornado.web.asynchronous
    def get(self, proportions):
        self.proportions = proportions
        self.write("Imagine this!")



class CropHandler(ImageDownloaderMixin, tornado.web.RequestHandler):

    def process_image(self, img):
        img.transform(crop=self.proportions)

    @tornado.web.asynchronous
    def get(self, proportions):
        self.proportions = proportions
        self.write("Imagine this!")


class MagicHandler(ImageDownloaderMixin, tornado.web.RequestHandler):

    def process_image(self, img):
        img.liquid_rescale(*self.proportions)

    @tornado.web.asynchronous
    def get(self, proportions):
        self.proportions = proportions.split('x')
        self.write("Imagine this!")


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