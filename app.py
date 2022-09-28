# importing in modules
import os
import shutil
from flask import Flask, request, render_template, redirect, url_for
from flask import send_from_directory, Response, send_file
from flask import session, request, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from flask_session import Session
from werkzeug.utils import secure_filename
import sys
from datetime import datetime
from time import sleep
import subprocess
from uuid import uuid4
import csv
import json

# Setting Variables
app = Flask(__name__, static_folder="static/", template_folder="templates/")
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
socketio = SocketIO(app, logger=False, engineio_logger=False)
Session(app)
app.secret_key = "secret key"
ALLOWED_EXTENSIONS = set(['txt'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()

# Parsing the filename and returning data back


def allowed_file(filename):
    print(filename.rsplit('.', 1)[1].lower())
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route that acts different based on if its a Get or Post request


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            print(file)
            UPLOAD_FOLDER = os.path.join(path, 'upload', session['number'])
            if not os.path.isdir(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = secure_filename(file.filename)
            save_location = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_location)
            socketio.emit('uploadcomplete')
    else:
        session['number'] = str(uuid4())
    return render_template('index.html', async_mode=socketio.async_mode), 200


# A Websocket to remove that tmp and upload folder after the code is finished.
@socketio.event
def killdata():
    shutil.rmtree('./upload/' + str(session['number']))

# The websocket that starts your own code


@socketio.event
def runTool():

    # Creating the upload folder
    UPLOAD_FOLDER = os.path.join(path, 'upload', session['number'])
    uploadedfile = os.path.join(UPLOAD_FOLDER, os.listdir(UPLOAD_FOLDER)[0])
    print(uploadedfile)
    try:
        os.environ["PYTHONUNBUFFERED"] = "1"
        emit('clearoutput')
        print("starting clearoutput2")
        # starting realtime pipe to websocket
        # ADD YOUR PYTHON SCRIPT FILE IN THE <ADD FILE HERE> SECTION IN LINE 70
        with subprocess.Popen(["python", "demo.py", "--file", uploadedfile], stdout=subprocess.PIPE, shell=False, bufsize=1, universal_newlines=True) as process:
            for linestdout in process.stdout:
                linestdout = linestdout.rstrip()
                try:
                    emit('logTool', {"loginfo": linestdout + "<br>"})
                    print(linestdout)
                except Exception as e:
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    filename = exception_traceback.tb_frame.f_code.co_filename
                    line_number = exception_traceback.tb_lineno
                    exceptstring = str(exception_type).replace(
                        "<", "").replace(">", "")
                    reason = "ERROR: " + str(exception_object) + "<br>\
                    Exception type: " + str(exceptstring) + "<br>\
                    File name: " + str(filename) + "<br>\
                    Line number: " + str(line_number) + "<br>"
                    emit('logTool', {"loginfo": str(reason) + "<br>"})
                    print(str(reason))
        # Letting the front end know the subprocess command is complete
        emit('runToolComplete')

    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        exceptstring = str(exception_type).replace("<", "").replace(">", "")
        reason = "ERROR: " + str(exception_object) + "<br>\
        Exception type: " + str(exceptstring) + "<br>\
        File name: " + str(filename) + "<br>\
        Line number: " + str(line_number) + "<br>"

        emit('logTool', {"loginfo": str(reason) + "<br>"})


# A disconnection socket, may or may not be used
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT"), threaded=True)
    socketio.run(
        app,
        host="0.0.0.0",
        port=os.environ.get("PORT"),
        threaded=True)
