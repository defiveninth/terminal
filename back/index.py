from flask import Flask, jsonify,request
import usb.core
import os
import cups
from flask_cors import CORS
from functions import get_usb_devices, get_flash_drive_path, get_printer_list, get_folder_with_path, get_folder_with_path_back

app = Flask(__name__)
CORS(app)
global indexUSB
indexUSB = 1

@app.route("/")
def index():
    return "Main page"

@app.route("/devices")
def devices():
    return jsonify(get_usb_devices())

@app.route("/devices/folder/<folderName>", methods=['get'])
def devicesGoFolder(folderName):
    return jsonify(get_folder_with_path(folderName))

@app.route("/devices/back", methods=['get'])
def devicesGoBackFolder():
    return jsonify(get_folder_with_path_back())

@app.route("/printers")
def printers():
    return jsonify(get_printer_list())

if __name__ == "__main__":
    app.run(port=1234, debug=True)
