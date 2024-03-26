import binascii
from flask import Flask, request, jsonify, json, render_template

app = Flask(__name__)

data = dict()

def decode(req_data):
    hex_data = req_data
    
    if hex_data:
        b_data = binascii.unhexlify(hex_data)
        return b_data

    return "No hex_data"

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/server', methods=['GET', 'POST'])
def showRequest():
    def storeRequest():
        data["req_data"] = request_data
        data["req_header"] = req_header
        data["req_method"] = req_method
        data["req_bin_data"] = binary_data

    if (request.is_json):
        request_data = request.json
    else:
        request_data = request.data
    req_header = request.headers
    req_method = request.method
    binary_data = decode(request_data)

    storeRequest()

    return request_data



@app.route('/showData', methods=['GET'])
def showData():

    return render_template("show_request.html", 
                        request_data = data["req_data"],
                        req_header = data["req_header"],
                        req_method = data["req_method"],
                        binary_data = data['req_bin_data'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
