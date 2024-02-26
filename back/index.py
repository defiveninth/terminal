from flask import Flask, jsonify
import usb.core
import os
import cups

app = Flask(__name__)

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
    for device in devices:
        device_info = {
            "deviceName": device.product,
            "files": get_flash_drive_path(device.idVendor)
        }
        device_list.append(device_info)
    if len(device_list) > 0:
        return {"status": "success", "devices": device_list}
    else:
        return {"status": "error", "message": f"Failed to retrieve USB devices"}

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
    return jsonify(get_usb_devices())

@app.route("/printers")
def printers():
    return jsonify(get_printer_list())

if __name__ == "__main__":
    app.run(debug=True)
