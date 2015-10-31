# -*- coding: utf-8 -*-


from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

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
            tmp = postVars[9700:9810]
            postVars = postVars.decode('utf-8', 'ignore').encode('utf-8')
            music = json.loads(postVars)['musicRequest']
            top = self._get_top_artists(music, 5)

            advisor = EventAdviser(self.server.context.get_se())
            events = {'eventsResponse': advisor.search(top)}
            json.dump(events, self.wfile)

        def _get_top_artists(self, music, top_count):
            # artists = map(lambda x: x["artist"], music)
            # uniq_artists = {}
            # for artist in artists:
            #     if artist in uniq_artists:
            #         uniq_artists[artist] += 1
            #     else:
            #         uniq_artists[artist] = 1
            #
            # sorted_artists = sorted(uniq_artists, key=uniq_artists.get, reverse=True)
            # return sorted_artists[:top_count]
            return music

if __name__ == '__main__':
    serv = Server(("10.25.3.181", 1025), HttpHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        serv.server_close()

