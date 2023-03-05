import asyncio
import tornado.web
import tornado.httpserver

from tornado.log import app_log
from tornado.options import define, options
from tornado.netutil import bind_sockets
from chatgpt import ChatGPTService
from defines import ErrorCode
from settings import DEBUG, PORT

define("port", default=PORT, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def json(self, body=None, errcode=None, errmsg=None):
        ret = {
            "body": body,
            "errcode": errcode or ErrorCode.SUCC,
            "errmsg": errmsg or ""
        }
        return self.write(ret)


class ChatGPTHandler(BaseHandler):
    def get(self):
        content = self.get_argument("content", "").strip()
        app_log.info(f"recv: {content}")
        if not content:
            return self.json(errcode=ErrorCode.ERROR, errmsg="content is null.")

        app_log.info(f"req chatgpt...")
        err, ret = ChatGPTService.fetch(content)
        app_log.info(f"chatgpt resp...")
        if err == ErrorCode.SUCC:
            self.json(ret, err)
        else:
            self.json(errcode=err, errmsg=ret)


def main():
    options.parse_command_line()
    application = tornado.web.Application(
        [(r"/chatgpt", ChatGPTHandler)],
        debug=DEBUG
    )
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    app_log.info(f"Listen on {options.port} ...")
    
    asyncio.run(asyncio.Event().wait())


def run_server():
    app_log.info(f"Listen on {options.port} ...")
    sockets = bind_sockets(options.port)
    tornado.process.fork_processes(0)

    options.parse_command_line()
    application = tornado.web.Application(
        [(r"/chatgpt", ChatGPTHandler)],
        debug=DEBUG
    )
    http_server = tornado.httpserver.HTTPServer(application)
 
    async def post_fork_main():
        http_server.add_sockets(sockets)
        await asyncio.Event().wait()

    asyncio.run(post_fork_main())


if __name__ == "__main__":
    run_server()

