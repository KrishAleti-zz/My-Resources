from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
@app.route('/via_post', methods=['POST'])  # for calling the API from Postman/SOAPUI
def math_postman():
    if (request.method == 'POST'):
        operation = request.json['operation']
        num1 = int(request.json['num1'])
        num2 = int(request.json['num2'])
        if (operation == 'add'):
            r = num1 + num2
            result = 'the sum of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'subtract'):
            r = num1 - num2
            result = 'the difference of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        if (operation == 'multiply'):
            r = num1 * num2
            result = 'the product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
        return jsonify(result)
@app.route('/tester', methods=['POST'])  # for calling the API from Postman/SOAPUI
def math_tester():
    if (request.method == 'POST'):
        num0 = int(request.json['num0'])
        num1 = int(request.json['num1'])
        num2 = int(request.json['num2'])
        result = num0*num1*num2
        return jsonify(result)
if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
