from flask import Flask
import os

def show_files_in_directory(directory):
    files = []
    filess = os.listdir(directory)
    for file in filess:
        if file.endswith(".png"):
            files.append(file)
    return files

app = Flask(__name__)

@app.route("/")
def index():
	directory_path = '../../../'
	return show_files_in_directory(directory_path)
if __name__ == '__main__':
    app.run(debug=True)