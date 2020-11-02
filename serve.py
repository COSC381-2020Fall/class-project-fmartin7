from http.server import BaseHTTPRequestHandler, HTTPServer

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # Handle the GET request from the browser
    # self: the instance of the class HTTPServer_RequestHandler
    # self: is teh web server instance
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers();

        # Dynamically generates a webpage
        self.wfile.write(b"<!DOCTYPE html>");
        self.wfile.write(b"<html lang='en'>");
        self.wfile.write(b"<head>");
        self.wfile.write(b"<title>Hello Title</title>");
        self.wfile.write(b"</head>");
        self.wfile.write(b"<body>");
        self.wfile.write(b"Hello World");
        self.wfile.write(b"</body>");
        self.wfile.write(b"</html>");

port = 8080

server_address = ("0.0.0.0", port)
httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
httpd.serve_forever()