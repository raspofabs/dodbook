import SimpleHTTPServer
import SocketServer

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("",PORT), Handler)
print "Serving at port", PORT
httpd.serve_forever()

