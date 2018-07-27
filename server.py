
import os
import uuid
import tasks

from flask import Flask, request, redirect
app = Flask(__name__)


@app.route("/")
def index():

    ###################################################################################################
    ## Execute custom workflow
    ###################################################################################################

    workflow = tasks.Load(tasks.Transform(tasks.Extract("./sample.csv")))

    res, err = workflow.execute()

    return err


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' in request.files:
        request.files['file'].save(os.path.join("./uploads/", "{}.csv".format(uuid.uuid4())))
            return redirect('/')

    return redirect('/')
