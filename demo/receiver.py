#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import base64

HOST = "127.0.0.1"
PORT = 8765


class Receiver(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path not in ("/collect", "/path/to/some/repo/with/dependency"):
            self.send_error(404)
            return
        if self.path == "/path/to/some/repo/with/dependency":
            body = b"OK\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)

        try:
            fields = parse_qs(body.decode("utf-8"))
            encoded = fields.get("data", [None])[0]

            if encoded is None:
                raise ValueError("missing data field")

            # Base64 is reversible encoding, not encryption.
            recovered = base64.b64decode(encoded).decode("utf-8")

            print("\n[DEMO] Received an HTTP POST")
            print(f"[DEMO] Encoded value: {encoded}")
            print(f"[DEMO] Recovered value: {recovered}")
            print("[DEMO] This demonstrates how an action with access to a")
            print("[DEMO] CI secret could transform and transmit its contents.")

            response = b"received\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        except Exception as exc:
            self.send_error(400, f"invalid demo payload: {exc}")

    def log_message(self, format, *args):
        # Keep the normal HTTP access log concise.
        print(f"[receiver] {args[0]}")


if __name__ == "__main__":
    print(f"[DEMO] Local receiver listening on http://{HOST}:{PORT}")
    print("[DEMO] This receiver accepts connections only from localhost.")

    server = HTTPServer((HOST, PORT), Receiver)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[DEMO] Receiver stopped.")
    finally:
        server.server_close()
