from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/krish_function')
def url_test1():
    test1 = request.args.get('val1')
    test2 = request.args.get('val2')
    test3 = int(test1) + int(test2)
    return '''<h3>my result is : {}</h3>'''.format(test3)  # http://127.0.0.1:5000/krish_function?val1=4&val2=6

@app.route('/url_function')
def url_data():
    test = request.args.get('val1')
    test1 = request.args.get('val2')
    test3 = int(test) - int(test1)
    return '''result: {}'''.format(test3)   # http://127.0.0.1:5000/url_function?val1=4&val2=6

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
