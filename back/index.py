from flask import Flask
import usb.core

app = Flask(__name__)


def get_memory(idVendorKey):
    listUSB = []
    dev = usb.core.find(idVendor=idVendorKey)

    if dev is None:
        return "Device not found"

    interface = 0
    endpoint = dev[0][(0, 0)][0]

    try:
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        return data
    except usb.core.USBError as e:
        return ("Ошибка чтения данных:", e)


def get_usb_devices():
    devices = usb.core.find(find_all=True)
    device_list = []
    if len(device_list)>0:
        for device in devices:
            device_list.append({
                "Device vendor: ": hex(device.idVendor),
                "Files: ":get_memory(hex(device.idVendor))
                })
        return device_list
    else:
        return "Devices not found"


@app.route("/")
def index():
    devices = get_usb_devices()
    return str(devices)

if __name__ == "__main__":
    app.run(debug=True)