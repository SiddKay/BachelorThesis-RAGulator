import uvicorn
import os
import signal
import sys
import threading
from dotenv import load_dotenv

load_dotenv()

# Event for coordinating shutdown
shutdown_event = threading.Event()


def run_server(module_path: str, host: str, port: int):
    """Run a uvicorn server with error handling"""
    try:
        config = uvicorn.Config(
            module_path, host=host, port=port, reload=True, log_level="info"
        )
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        print(f"Server error on port {port}: {e}")
        shutdown_event.set()


def run_main_app():
    run_server(
        "app.server:app",
        host=os.getenv("MAIN_HOST", "localhost"),
        port=int(os.getenv("MAIN_PORT", "8000")),
    )


def run_langserve():
    run_server(
        "langserver.server:app",
        host=os.getenv("LANGSERVE_HOST", "localhost"),
        port=int(os.getenv("LANGSERVE_PORT", "8001")),
    )


def handle_interrupt(signum, frame):
    print("\nInitiating graceful shutdown...")
    shutdown_event.set()


if __name__ == "__main__":
    # Register signal handler
    signal.signal(signal.SIGINT, handle_interrupt)

    # Create and start server threads
    main_thread = threading.Thread(target=run_main_app, daemon=True)
    langserve_thread = threading.Thread(target=run_langserve, daemon=True)

    main_thread.start()
    langserve_thread.start()

    # Keep main thread alive until shutdown is requested
    try:
        while not shutdown_event.is_set():
            shutdown_event.wait(1)
    except KeyboardInterrupt:
        print("\nShutdown initiated by user...")
    finally:
        print("Shutting down servers...")
        sys.exit(0)
