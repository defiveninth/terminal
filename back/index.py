from flask import Flask, jsonify
import usb.core
import os
import cups

app = Flask(__name__)

def get_printer_list():
    conn = cups.Connection()
    printers = conn.getPrinters()
    return printers


def get_usb_devices():
    devices = usb.core.find(find_all=True)
    device_list = []
    for device in devices:
        device_info = {
            "Device name:": os.listdir(f"/Volumes")[1],
            "Files:": get_flash_drive_path(device.idVendor),
        }
        device_list.append(device_info)
    if device_list:
        return jsonify({"status":"success","message":"Flash list successfully finded", "USBList":files})
    else:
        return jsonify({"status":"error","message":"Flash not find"})

def get_flash_drive_path(idVendor):
    vendor_id = hex(idVendor)

    if os.listdir(f"/System"):
        files = []
        for i in os.listdir(f"/Volumes/{os.listdir(f"/Volumes")[1]}"):
            if i.endswith(".docx"):
                files.append(i)
        return files
    else:
        return []

@app.route("/")
def index():
    return "Main page"

@app.route("/devices")
def devices():
    devices = get_usb_devices()
    return jsonify(devices)

@app.route("/printers")
def printers():
    return jsonify(get_printer_list())

if __name__ == "__main__":
    app.run(debug=True)