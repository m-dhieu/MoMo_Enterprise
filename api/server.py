#--------------------------------------------------------------------------------
# Script Name: server.py
# Description: Implements a REST API using Python's built-in http.server.
#              Provides CRUD endpoints for mobile money SMS transactions'
#              Secured by Basic Authentication.
# Author: Janviere Munezero
# Date:   2025-09-28
# Usage:  python3 server.py
#--------------------------------------------------------------------------------

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
from urllib.parse import urlparse

# Path to the JSON file that stores transaction data
DATA_FILE = 'data/processed/transactions.json'

# Authentication credentials 
USERNAME = 'admin'
PASSWORD = 'password'

def load_transactions():
    # Load the list of transactions from the JSON file.
    # If the file is missing or error occurs, returns empty list.
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []

def save_transactions(transactions):
    # Save the updated list of transactions back to the JSON file.
    with open(DATA_FILE, 'w') as f:
        json.dump(transactions, f, indent=4)

# Load transactions into memory for fast access during runtime.
transactions = load_transactions()

class AuthHandlerMixin:
    # Mixin class providing authentication support.

    def do_AUTHHEAD(self):
        # Respond with 401 and Authentication prompt.
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMoAPI"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def authenticate(self):
        # Check request for valid Authentication credentials.
        # Return True if authenticated, else respond 401 and return False.
        auth_header = self.headers.get('Authorization')
        if auth_header is None or not auth_header.startswith('Basic '):
            self.do_AUTHHEAD()
            self.wfile.write(b'{"error":"Authentication required"}')
            return False
        encoded = auth_header.split(' ')[1]
        try:
            decoded = base64.b64decode(encoded).decode()
            user, pwd = decoded.split(':')
        except Exception:
            self.do_AUTHHEAD()
            self.wfile.write(b'{"error":"Invalid authentication header format"}')
            return False
        if user == USERNAME and pwd == PASSWORD:
            return True
        else:
            self.do_AUTHHEAD()
            self.wfile.write(b'{"error":"Invalid credentials"}')
            return False

class TransactionHandler(AuthHandlerMixin, BaseHTTPRequestHandler):
    # Request handler for implementing RESTful transaction endpoints with Basic Authentication.

    def send_json_response(self, code, data):
        # Send JSON response with HTTP status code and data object.
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def parse_path(self):
        # Parse the URL path into components.
        # Returns list of path parts for routing.
        parsed = urlparse(self.path)
        path_parts = parsed.path.strip('/').split('/')
        return path_parts

    def get_transaction_by_id(self, tid):
        # Return transaction dict with matching TransactionID, or None if not found.
        for tx in transactions:
            if tx.get('TransactionID') == tid:
                return tx
        return None

    def do_GET(self):
        # Handle GET requests:
        # 'GET /transactions' returns list of all transactions.
        # 'GET /transactions/{id}' returns specific transaction by ID.
        if not self.authenticate():
            return
        path_parts = self.parse_path()
        if len(path_parts) == 1 and path_parts[0] == 'transactions':
            self.send_json_response(200, transactions)
        elif len(path_parts) == 2 and path_parts[0] == 'transactions':
            try:
                tid = int(path_parts[1])
            except ValueError:
                self.send_json_response(400, {"error": "Invalid transaction ID"})
                return
            tx = self.get_transaction_by_id(tid)
            if tx is not None:
                self.send_json_response(200, tx)
            else:
                self.send_json_response(404, {"error": "Transaction not found"})
        else:
            self.send_json_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        # Handle POST requests:
        # 'POST /transactions with JSON body' creates new transaction.
        if not self.authenticate():
            return
        path_parts = self.parse_path()
        if len(path_parts) == 1 and path_parts[0] == 'transactions':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                new_tx = json.loads(post_data)
                # Automatically assign new TransactionID if missing.
                new_tx['TransactionID'] = max((tx['TransactionID'] for tx in transactions), default=0) + 1
                transactions.append(new_tx)
                save_transactions(transactions)
                self.send_json_response(201, new_tx)
            except Exception as e:
                self.send_json_response(400, {"error": "Invalid JSON data", "details": str(e)})
        else:
            self.send_json_response(404, {"error": "Endpoint not found"})

    def do_PUT(self):
        # Handle PUT requests:
        # 'PUT /transactions/{id} with JSON body' updates existing transaction.
        if not self.authenticate():
            return
        path_parts = self.parse_path()
        if len(path_parts) == 2 and path_parts[0] == 'transactions':
            try:
                tid = int(path_parts[1])
            except ValueError:
                self.send_json_response(400, {"error": "Invalid transaction ID"})
                return
            idx = next((i for i, tx in enumerate(transactions) if tx.get('TransactionID') == tid), None)
            if idx is None:
                self.send_json_response(404, {"error": "Transaction not found"})
                return
            content_length = int(self.headers.get('Content-Length', 0))
            put_data = self.rfile.read(content_length)
            try:
                updated_tx = json.loads(put_data)
                updated_tx['TransactionID'] = tid  # keep ID consistent
                transactions[idx] = updated_tx
                save_transactions(transactions)
                self.send_json_response(200, updated_tx)
            except Exception as e:
                self.send_json_response(400, {"error": "Invalid JSON data", "details": str(e)})
        else:
            self.send_json_response(404, {"error": "Endpoint not found"})

    def do_DELETE(self):
        # Handle DELETE requests:
        # 'DELETE /transactions/{id}' deletes a transaction.
        if not self.authenticate():
            return
        path_parts = self.parse_path()
        if len(path_parts) == 2 and path_parts[0] == 'transactions':
            try:
                tid = int(path_parts[1])
            except ValueError:
                self.send_json_response(400, {"error": "Invalid transaction ID"})
                return
            idx = next((i for i, tx in enumerate(transactions) if tx.get('TransactionID') == tid), None)
            if idx is None:
                self.send_json_response(404, {"error": "Transaction not found"})
                return
            deleted_tx = transactions.pop(idx)
            save_transactions(transactions)
            self.send_json_response(200, {"message": "Transaction deleted", "transaction": deleted_tx})
        else:
            self.send_json_response(404, {"error": "Endpoint not found"})

def run(server_class=HTTPServer, handler_class=TransactionHandler, port=8080):
    # Set up and run the server on specified port.
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server started at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
