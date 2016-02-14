from server.server import web, handlers, settings, ioloop
from server.config import SERVER_PORT

application = web.Application(handlers, **settings)
application.listen(SERVER_PORT, address="0.0.0.0")
ioloop.IOLoop.current().start()
