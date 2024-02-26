from flask import Flask
import usb.core
import os

app = Flask(__name__)


def get_usb_devices():
    devices = usb.core.find(find_all=True)
    device_list = []
    for device in devices:
        device_info = {
            "Device vendor:": hex(device.idVendor),
            "Path:": get_flash_drive_path(device.idVendor)
        }
        device_list.append(device_info)
    return device_list

def get_flash_drive_path(idVendor):
    vendor_id = hex(idVendor)

    usb_mount_path = "/System/"

    for root, dirs, files in os.walk(usb_mount_path):
        for directory in dirs:
            if directory.startswith(vendor_id):
                return os.path.join(root, directory)

    return "Flash drive path not found"

@app.route("/")
def index():
    return "Main page"

@app.route("/devices")
def devices():
    devices = get_usb_devices()
    return str(devices)

if __name__ == "__main__":
    app.run(debug=True)