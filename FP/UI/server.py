from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import re

# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):

    # POST method
    def do_POST(self):
        if self.path == '/download':
            content_length = int(self.headers['Content-Length'])

            post_data = self.rfile.read(content_length).decode('utf-8')
            print(post_data)


            match = re.search(r'name="nama_file"\r\n\r\n(.*?)\r\n', post_data, re.DOTALL)
            if match:
                nama_file = match.group(1)
                response_message = f'Thank you for submitting the form! You entered: {nama_file}'
            else:
                response_message = 'Invalid form data!'

            # Send the response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response_message.encode('utf-8'))

            return

def run():
    print('Starting the server...')

    host = 'localhost'
    port = 8000

    server = HTTPServer((host, port), RequestHandler)
    print(f'Server running on {host}:{port}')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopping the server...')
        server.shutdown()

if __name__ == '__main__':
    run()
