#!/usr/bin/env python3

import json
import datetime
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

class WebhookHandler(BaseHTTPRequestHandler):
    # Suppress HTTP request logs
    def log_message(self, format, *args):
        # Do nothing to suppress the default logging
        pass
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        response = {
            'status': 'ok',
            'message': 'Webhook receiver is running. Send POST requests with JSON data.'
        }
        self.wfile.write(json.dumps(response).encode())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Get content length and read data
        content_length = int(self.headers['Content-Length']) if 'Content-Length' in self.headers else 0
        post_data = self.rfile.read(content_length)
        
        # Get client IP address
        client_ip = self.client_address[0]
        
        # Get current timestamp
        timestamp = datetime.datetime.now().isoformat()
        
        # Process the payload
        try:
            # Try to parse as JSON
            payload = json.loads(post_data.decode('utf-8'))
            
            # Create output with metadata
            output = {
                'source_ip': client_ip,
                'timestamp': timestamp,
                'endpoint': self.path,
                'payload': payload
            }
            
            # Print as JSON
            print(json.dumps(output, indent=2))
            
            # Send success response
            self._set_headers()
            response = {'status': 'success', 'message': 'Webhook received'}
            self.wfile.write(json.dumps(response).encode())
            
        except json.JSONDecodeError:
            # If not valid JSON, return error
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            error_response = {
                'status': 'error',
                'message': 'Invalid JSON payload'
            }
            self.wfile.write(json.dumps(error_response).encode())
            
            # Still log the attempt with raw data
            output = {
                'source_ip': client_ip,
                'timestamp': timestamp,
                'endpoint': self.path,
                'error': 'Invalid JSON payload',
                'raw_data': post_data.decode('utf-8', errors='replace')
            }
            print(json.dumps(output, indent=2))

def run(server_class=HTTPServer, handler_class=WebhookHandler, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting webhook receiver on port {port}...')
    print(f'Waiting for JSON webhooks. Press Ctrl+C to stop.')
    httpd.serve_forever()

if __name__ == "__main__":
    # Get port from command line argument, environment variable, or default to 8000
    port = 8000
    
    # First check command line arguments
    if len(sys.argv) >= 2:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(json.dumps({
                'status': 'error',
                'message': f'Invalid port number: {sys.argv[1]}'
            }, indent=2))
            sys.exit(1)
    # Then check environment variable
    elif 'WEBHOOK_PORT' in os.environ:
        try:
            port = int(os.environ['WEBHOOK_PORT'])
        except ValueError:
            print(json.dumps({
                'status': 'error',
                'message': f'Invalid port number in WEBHOOK_PORT environment variable: {os.environ["WEBHOOK_PORT"]}'
            }, indent=2))
            sys.exit(1)
    
    # Run the server with the determined port
    run(port=port)

