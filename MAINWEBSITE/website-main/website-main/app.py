from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from chtbot.app import infer_from_rag
import traceback

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'response': 'No data provided.'}), 400
            
        message = data.get('message', '')
        if not message:
            return jsonify({'response': 'Please provide a message.'}), 400
        
        response = infer_from_rag(message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'response': f'Sorry, there was an error processing your request. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 