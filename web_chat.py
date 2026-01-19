# web_chat.py
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from chat_engine import ChatEngine
import markdown
import os
import socket
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize chat engine with error handling
try:
    chat_engine = ChatEngine(model_name="llama3.2:latest")
    print("✅ Chat engine initialized successfully")
except Exception as e:
    print(f"❌ Error initializing chat engine: {e}")
    print("Make sure Ollama is running and llama3.2:latest model is available")
    chat_engine = None


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if chat_engine is None:
            return jsonify({'error': 'Chat engine not initialized. Please check Ollama and model availability.'}), 500

        data = request.get_json()
        query = data.get('message', '')

        if not query.strip():
            return jsonify({'error': 'Empty message'}), 400

        # Get response from chat engine
        response = chat_engine.get_response(query)

        # Convert markdown to HTML for formatting
        html_response = markdown.markdown(
            response, extensions=['fenced_code', 'tables', 'nl2br'])

        return jsonify({
            'response': response,
            'html_response': html_response,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        if chat_engine is None:
            return jsonify({'error': 'Chat engine not initialized'}), 500

        history = chat_engine.get_chat_history()
        # Convert responses to HTML for each entry
        for entry in history:
            entry['html_response'] = markdown.markdown(
                entry['response'],
                extensions=['fenced_code', 'tables', 'nl2br']
            )
        return jsonify({'history': history})
    except Exception as e:
        print(f"Error in history endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    try:
        chat_engine.clear_chat_history()
        return jsonify({'message': 'Chat history cleared successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/export', methods=['POST'])
def export_history():
    try:
        filename = chat_engine.export_chat_history()
        return send_file(filename, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    if chat_engine is None:
        return jsonify({
            'status': 'error',
            'message': 'Chat engine not initialized',
            'chat_entries': 0
        })

    return jsonify({
        'status': 'online',
        'model': chat_engine.model_name,
        'chat_entries': len(chat_engine.chat_history)
    })


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')

    # Find a free port
    port = find_free_port(8080)
    if port is None:
        print("❌ Error: Could not find a free port between 8080-8179")
        exit(1)

    print("🌐 Starting web chat interface...")
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("💾 Chat history is automatically saved")
    print("🔄 Press Ctrl+C to stop the server")

    app.run(debug=True, host='0.0.0.0', port=port)
