import logging
from http.server import SimpleHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle favicon.ico request
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            logging.info(f"Received request for path: {self.path}, responded with: HTTP 204")
            return

        # Handle root request
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Welcome to the server!")
            logging.info(f"Received request for path: {self.path}, responded with: HTTP 200")
            return

        try:
            # Extract the HTTP response code from the path
            response_code = int(self.path[1:])
            if 100 <= response_code < 600:
                self.send_response(response_code)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"HTTP {response_code}".encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f"HTTP {response_code}".encode())
        except ValueError:
            # Failover for unexpected requests
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Unexpected request")
            logging.info(f"Received unexpected request for path: {self.path}, responded with: HTTP 400")
        
        logging.info(f"Received request for path: {self.path}, responded with: HTTP {response_code}")

if __name__ == '__main__':
    server_address = ('127.0.0.1', 65535)  # Listen on localhost, port 65535
    httpd = HTTPServer(server_address, CustomHandler)
    print(f"Server started at http://{server_address[0]}:{server_address[1]}/")
    httpd.serve_forever()
