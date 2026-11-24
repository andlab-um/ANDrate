"""Run the local ANDrate service and open its browser interface."""
import argparse
import sys
import threading
import webbrowser
from werkzeug.serving import make_server
from app import app, BASE_DIR

def main():
    parser = argparse.ArgumentParser(description="Start ANDrate locally")
    parser.add_argument("--port", type=int, default=9005)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Port must be between 1 and 65535")
    try:
        server = make_server("127.0.0.1", args.port, app, threaded=True)
    except (OSError, SystemExit):
        print("Cannot start ANDrate. Close the existing instance, or use --port 9006.", file=sys.stderr)
        return 1
    url = f"http://127.0.0.1:{args.port}"
    print(f"ANDrate: {url}\nFiles: {BASE_DIR}\nKeep this window open. Press Ctrl+C to stop.", flush=True)
    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nANDrate stopped.")
    finally:
        server.server_close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
