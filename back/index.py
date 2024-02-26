from flask import Flask, jsonify
import usb.core
import os
import cups
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
global indexUSB
indexUSB = 0
def get_printer_list():
    try:
        conn = cups.Connection()
        printers = conn.getPrinters()
        return {"status": "success", "printers": list(printers.keys())}
    except cups.IPPError as e:
        return {"status": "error", "message": f"Failed to retrieve printers: {e}"}

def get_usb_devices():
    devices = usb.core.find(find_all=True)
    device_list = []
    volume_dirs = os.listdir(f"/Volumes/")[indexUSB]
    if volume_dirs != "Macintosh HD":
        device_info = {
            "deviceName": volume_dirs,
            "files": get_flash_drive_path(volume_dirs)
        }
        device_list.append(device_info)
    if len(device_list) > 0:
        return {"status": "success", "devices": device_list}
    else:
        return {"status": "error", "message": f"Failed to retrieve USB devices"}

def get_flash_drive_path(volume_dir):
    if os.path.isdir(f"/Volumes/{volume_dir}/DCIM/100CANON"):
        files = os.listdir(f"/Volumes/{volume_dir}/DCIM/100CANON")
        return files
    else:
        return []

@app.route("/")
def index():
    return "Main page"

@app.route("/devices")
def devices():
    return jsonify(get_usb_devices())

@app.route("/printers")
def printers():
    return jsonify(get_printer_list())

if __name__ == "__main__":
    app.run(debug=True)
