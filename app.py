from flask import Flask, request, jsonify, json, render_template

app = Flask(__name__)

data = dict()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/server', methods=['GET', 'POST'])
def showRequest():
    def storeRequest():
        data["req_data"] = request_data
        data["req_header"] = req_header
        data["req_method"] = req_method

    if (request.is_json):
        request_data = request.json
    else:
        request_data = request.data
    req_header = request.headers
    req_method = request.method

    storeRequest()

    return request_data



@app.route('/showData', methods=['GET'])
def showData():

    return render_template("show_request.html", 
                        request_data = data["req_data"],
                        req_header = data["req_header"],
                        req_method = data["req_method"])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
