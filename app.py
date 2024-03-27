import binascii
from flask import Flask, request, jsonify, json, render_template
from parse import Parse, Variable

app = Flask(__name__)


#req_data = b'\t@\x19\x01\x141234\x9cA~\x9c\xe3D\x00\x00\x00\x00\x86\x0f\xc3\x82Z\xaf\xaa\xbf\xd6m\x83\xda\x90Z\x94\x1aH\xa6\x0c\x151\x1d\x10\xd8\xb9r?Y\x8c\xc6\xa5'
decoded_data = dict()
dec_data = []
postRequestData = dict()

#all the routes
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

#endpoint for signaling
@app.route('/server', methods=['GET', 'POST'])
def showRequest():
    if request.method==['POST']:
        postRequestData["req_data"] = request.data
        postRequestData["req_method"] = request.method

    
    return "200 OK"


@app.route('/showData', methods=['GET'])
def showData(): 

    req_data = postRequestData["req_data"]
    dec_data = [int(bytes) for bytes in req_data]
    decoded_data = Parse(dec_data)
    if isinstance(decoded_data, dict):
        return render_template("show_request.html", 
                            decoded_data=decoded_data,
                            request_data = req_data,
                            requestMethod = postRequestData["req_method"])
    else:
        return "Error: Decoded Data is not a dictionary"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
