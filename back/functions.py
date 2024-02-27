import os
import cups
import usb.core

global currentPath
currentPath = ""


def get_printer_list():
    try:
        conn = cups.Connection()
        printers = conn.getPrinters()
        return {"status": "success", "printers": list(printers.keys())}
    except cups.IPPError as e:
        return {"status": "error", "message": f"Failed to retrieve printers: {e}"}


def get_usb_devices():
    global currentPath
    try:
        devices = usb.core.find(find_all=True)
        device_list = []
        for volume_dir in os.listdir("/Volumes/"):
            if volume_dir != "Macintosh HD":
                currentPath = f"/Volumes/{volume_dir}/"
                device_info = {
                    "deviceName": volume_dir,
                    "Path": get_flash_drive_path(currentPath),
                }
                device_list.append(device_info)
        if len(device_list) > 0:
            return {"status": "success", "devices": device_list, "path": currentPath}
        else:
            return {"status": "error", "message": "No USB devices found"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve USB devices: {e}"}


def get_flash_drive_path(current_Path):
    try:
        files = []
        folders = []
        for item in os.listdir(current_Path):
            item_path = os.path.join(current_Path, item)
            if os.path.isfile(item_path):
                if not item.startswith("."):
                    files.append(item)
            elif os.path.isdir(item_path):
                if not item.startswith("."):
                    folders.append(item)
        return {"files": files, "folders": folders}
    except Exception as e:
        return {"error": str(e)}


def get_folder_with_path(folderName):
    global currentPath
    if currentPath.endswith(folderName):
        pass
    else:
        currentPath = os.path.join(currentPath, folderName)
    try:
        files = []
        folders = []
        for item in os.listdir(currentPath):
            item_path = os.path.join(currentPath, item)
            if os.path.isfile(item_path):
                if not item.startswith("."):
                    files.append(item)
            elif os.path.isdir(item_path):
                if not item.startswith("."):
                    folders.append(item)
        return {
            "status": "success",
            "files": files,
            "folders": folders,
            "path": currentPath,
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve contents: {e}"}
