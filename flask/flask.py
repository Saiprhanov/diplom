from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def handle_data():
    data = request.json
    response = {'received': True, 'data': data}
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)