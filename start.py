#!/usr/bin/env python3
# start.py
import sys
import subprocess
import os
import socket


def find_free_port(start_port=8080):
    """Find a free port starting from the given port."""
    port = start_port
    while port < start_port + 100:  # Try up to 100 ports
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
    return None


def main():
    print("🧠 LocalPDFGPT - Chat with Your PDF")
    print("=" * 40)
    print("Choose your interface:")
    print("1. 🖥️  Command Line Interface (CLI)")
    print("2. 🌐 Web Interface")
    print("3. 📊 Load and Index PDF (first time setup)")
    print("4. ❌ Exit")

    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                print("\n🚀 Starting CLI interface...")
                subprocess.run([sys.executable, "chat_cli.py"])
                break

            elif choice == "2":
                print("\n🌐 Starting web interface...")
                port = find_free_port(8080)
                if port:
                    print(
                        f"📱 Open your browser and go to: http://localhost:{port}")
                    print("⏳ Starting server... (this may take a few seconds)")
                else:
                    print("📱 Open your browser to the URL shown when the server starts")
                    print("⏳ Starting server... (this may take a few seconds)")

                # Add some delay and verification
                result = subprocess.run([sys.executable, "web_chat.py"])
                if result.returncode != 0:
                    print("\n❌ Web server failed to start. Please check:")
                    print("   1. Ollama is running: ollama serve")
                    print(
                        "   2. llama3.2:latest model is available: ollama pull llama3.2:latest")
                    print("   3. Vector database exists: run option 3 first")
                break

            elif choice == "3":
                print("\n📊 Loading and indexing PDF...")
                if os.path.exists("book.pdf"):
                    subprocess.run([sys.executable, "load_and_index.py"])
                    print("\n✅ PDF indexed successfully!")
                    print("Now you can use option 1 or 2 to start chatting.")
                else:
                    print("❌ Error: book.pdf not found!")
                    print(
                        "Please make sure you have a PDF file named 'book.pdf' in this directory.")

            elif choice == "4":
                print("\n👋 Goodbye!")
                sys.exit(0)

            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
