from flask import Flask, jsonify
import usb.core
import os

app = Flask(__name__)

def get_usb_devices():
    devices = usb.core.find(find_all=True)
    device_list = []
    for device in devices:
        device_info = {
            "Device name:": os.listdir(f"/Volumes")[1],
            "Files:": get_flash_drive_path(device.idVendor),
        }
        device_list.append(device_info)
    return device_list

def get_flash_drive_path(idVendor):
    vendor_id = hex(idVendor)

    if os.listdir(f"/System"):
        files = []
        for i in os.listdir(f"/Volumes/{os.listdir(f"/Volumes")[1]}"):
            if i.endswith(".docx"):
                files.append(i)
        return files
    else:
        return "Flash drive path not found"

@app.route("/")
def index():
    return "Main page"

@app.route("/devices")
def devices():
    devices = get_usb_devices()
    return jsonify(devices)

if __name__ == "__main__":
    app.run(debug=True)