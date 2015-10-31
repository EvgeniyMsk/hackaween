# -*- coding: utf-8 -*-


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import json

from initializer import Initializer
from event_adviser import EventAdviser

class Server(HTTPServer):

    def __init__(self, server_address, handler_class):
        HTTPServer.__init__(self, server_address, handler_class)
        self.context = Initializer.get_context()


class HttpHandler(BaseHTTPRequestHandler):

        # def do_GET(self):
        #     self.send_response(200)
        #     self.send_header('content-type','text/html')
        #     self.end_headers()
        #     self.wfile.write("Sanyok pidor")

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
    serv = Server(("127.0.0.1", 1025), HttpHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        serv.server_close()

