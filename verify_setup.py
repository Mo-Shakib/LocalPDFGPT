#!/usr/bin/env python3
# verify_setup.py
import sys
import os
import importlib


def check_imports():
    """Check if all required packages are installed."""
    required_packages = [
        'flask',
        'flask_cors',
        'markdown',
        'langchain',
        'langchain_community',
        'chromadb'
    ]

    print("🔍 Checking required packages...")
    missing_packages = []

    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT FOUND")
            missing_packages.append(package)

    return missing_packages


def check_files():
    """Check if all required files exist."""
    required_files = [
        'chat_engine.py',
        'chat_cli.py',
        'web_chat.py',
        'load_and_index.py',
        'start.py',
        'templates/index.html',
        'requirements.txt'
    ]

    print("\n📁 Checking required files...")
    missing_files = []

    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - NOT FOUND")
            missing_files.append(file)

    return missing_files


def check_database():
    """Check if vector database exists."""
    print("\n🗄️ Checking vector database...")
    if os.path.exists('db') and os.path.isdir('db'):
        db_files = os.listdir('db')
        if db_files:
            print(f"  ✅ Vector database found with {len(db_files)} files")
            return True
        else:
            print("  ⚠️ Database directory exists but is empty")
            return False
    else:
        print("  ⚠️ Vector database not found - run 'python load_and_index.py' first")
        return False


def main():
    print("🧠 LocalPDFGPT Setup Verification")
    print("=" * 40)

    # Check imports
    missing_packages = check_imports()

    # Check files
    missing_files = check_files()

    # Check database
    db_exists = check_database()

    # Summary
    print("\n📋 Summary:")
    if missing_packages:
        print(f"  ❌ Missing packages: {', '.join(missing_packages)}")
        print(f"     Run: pip install {' '.join(missing_packages)}")
    else:
        print("  ✅ All required packages installed")

    if missing_files:
        print(f"  ❌ Missing files: {', '.join(missing_files)}")
    else:
        print("  ✅ All required files present")

    if not db_exists:
        print("  ⚠️ Vector database not ready")
        print("     Run: python load_and_index.py")
    else:
        print("  ✅ Vector database ready")

    # Overall status
    if not missing_packages and not missing_files:
        if db_exists:
            print("\n🎉 Setup is complete! You can now:")
            print("   - Run 'python start.py' to choose interface")
            print("   - Run 'python chat_cli.py' for CLI")
            print("   - Run 'python web_chat.py' for web interface")
        else:
            print("\n⚠️ Setup is almost complete!")
            print("   - First run 'python load_and_index.py' to index your PDF")
            print("   - Then you can start chatting!")
    else:
        print("\n❌ Setup incomplete - please fix the issues above")


if __name__ == "__main__":
    main()
