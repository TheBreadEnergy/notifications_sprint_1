from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from src.app import create_app

http_server = WSGIServer(("0.0.0.0", 5556), create_app())
http_server.serve_forever()
