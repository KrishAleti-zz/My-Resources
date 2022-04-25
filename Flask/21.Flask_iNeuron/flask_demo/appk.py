# install flask - pip install flask

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/test', methods=['POST'])  # for calling the API from Postman/SOAPUI
def math_test():
    if (request.method == 'POST'):
        num0 = int(request.json['num0'])
        num1 = int(request.json['num1'])
        num2 = int(request.json['num2'])
        result = num0*num1*num2
        return jsonify(result)
if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
