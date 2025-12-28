"""
Here Server - Main Entry Point
Run this file to start the server or access management tools.
"""
import subprocess
import sys


def show_menu():
    """Display the main menu and handle user selection."""
    while True:
        print("\n" + "=" * 40)
        print("       HERE SERVER")
        print("=" * 40)
        print("1. Start Server")
        print("2. Exit")
        print("=" * 40)

        choice = input("Select an option: ").strip()

        if choice == "1":
            start_server()
        elif choice == "2":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")


def start_server():
    """Start the FastAPI server using uvicorn."""
    print("\nStarting Here Server...")
    print("Server will be available at: http://localhost:8847")
    print("API docs at: http://localhost:8847/docs")
    print("Press Ctrl+C to stop the server.\n")

    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "src.api.server:app",
            "--host", "0.0.0.0",
            "--port", "8847",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    show_menu()
