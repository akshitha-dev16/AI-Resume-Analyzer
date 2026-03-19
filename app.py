from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    return jsonify({"status": "success", "message": "Resume analyzed"})

if __name__ == '__main__':
    app.run(debug=True)