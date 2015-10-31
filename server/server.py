# -*- coding: utf-8 -*-


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import json

from initializer import Initializer
from event_adviser import EventAdviser

class Server(HTTPServer):

    def __init__(self, handler_class):
        self.context = Initializer.get_context()

        http_cfg = self.context.get_http_cfg()
        HTTPServer.__init__(self, (http_cfg["host"], http_cfg["port"]), handler_class)


class HttpHandler(BaseHTTPRequestHandler):

        def do_POST(self):
            self.send_response(200)
            self.end_headers()
            len = int(self.headers['Content-Length'])
            postVars = self.rfile.read(len)
            postVars = postVars.decode('utf-8', 'ignore').encode('utf-8')
            music = json.loads(postVars)['musicRequest']

            top = self.server.context.get_artist_ranker().rank(music, 10)

            advisor = EventAdviser(self.server.context.get_se())
            events = {'eventsResponse': advisor.search(top)}
            json.dump(events, self.wfile)


if __name__ == '__main__':
    # 10.25.3.181
    serv = Server(HttpHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        serv.server_close()

