from flask import Flask, request, jsonify
from service.convert_service import convert_yt_to_text

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Configura Flask para que no use ASCII para JSON


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/convert', methods=['POST'])
def convert():
    return jsonify(convert_yt_to_text(request.json['url'])), 200

if __name__ == '__main__':
    app.run(debug=True)