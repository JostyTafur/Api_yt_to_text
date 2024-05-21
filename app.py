from flask import Flask, request, jsonify
from service.convert_service import convert_yt_to_text, convert_audio_to_text

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False  # Configura Flask para que no use ASCII para JSON


    @app.route('/')
    def home():
        return 'Hello, World!'

    @app.route('/convert', methods=['POST'])
    def convert():
        try:
            url = request.json['url']
            if url is None:
                return jsonify({"error": "URL is required"}), 400
            
            result = convert_yt_to_text(url)
            return jsonify(result), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/whisper', methods=['POST'])
    def whisper():
        try:
            file = request.files['file']
            if file is None:
                return jsonify({"error": "File is required"}), 400
            result = convert_audio_to_text(file)
            return jsonify(result), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()