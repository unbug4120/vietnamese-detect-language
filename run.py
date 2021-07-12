from flask import (
    Flask, request, escape, jsonify, make_response
)

from underthesea import pos_tag
from google_trans_new import google_translator

app = Flask(__name__, static_url_path='',static_folder='ner-api/static')


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/v2/api', methods=['POST', 'GET'])
def underthesea_api():

    print(request)
    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({"error": "Missing JSON in request"}), 400)
        translator = google_translator()
        text = request.json.get('text')
        result = pos_tag(text)
        data = []
        for value in result:
            if value[1] == "Np" or value[1] == "V":
                if not value[0].isnumeric():
                    detector = translator.detect(value[0])
                    if detector[0] != "vi":
                        data.append(value[0])
        keywords = ' + '.join(data)
        print("Return: ", keywords)
        return make_response(jsonify({
            "results": keywords
        }), 200)

    default = {
        "message": "Method Not Allowed"
    }
    return make_response(jsonify(default), 405)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
