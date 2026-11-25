"""
ClassroomPortal Production Server Launcher
Uses Waitress multi-threaded production WSGI server.
Runs natively across Windows, Linux, and macOS without compilation.
"""
import os
import sys
from app import app
from waitress import serve

def run():
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    threads = int(os.environ.get('THREADS', 6))

    print("=" * 65)
    print("ClassroomPortal Production Server Starting (Waitress WSGI)")
    print("=" * 65)
    print(f"  Bound Address : http://{host}:{port}")
    print(f"  Worker Threads: {threads}")
    print(f"  Security Mode : Strict IDOR Gatekeeper Active")
    print(f"  Environment   : Production")
    print("=" * 65)
    print("Server is listening for connections. Press Ctrl+C to terminate.")

    serve(app, host=host, port=port, threads=threads)

if __name__ == '__main__':
    run()
