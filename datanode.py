import json
import shutil
import sys
import os
from flask import Flask, render_template, request

import client

HOST = '127.0.0.1'
port = int(sys.argv[1])

app = Flask(__name__)


class DataNode:
    def __init__(self, file_name):
        self.file_name = file_name


@app.route('/read_message')
def read_message():
    data = request.data.decode('utf-8')
    file_name = f"node{data}.json"
    if os.path.isfile(file_name):
        size_file = os.path.getsize(file_name)
        print(size_file)
        if size_file > 24:
            obj = json.load(open(file_name, "r"))

            print(obj["messages"][0])
            res = obj["messages"][0]
            obj["messages"].pop(0)

            open(file_name, "w").write(
                json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
            )
            return res, 200
        else:
            client.client_1.uptd()
            print("Queue is empty")
            return "Queue is empty", 200
    else:
        client.client_1.uptd()
        print("Queue is empty")
        return "Queue is empty", 200


@app.route("/write_msg")
def write_msg():
    data = request.data
    data = json.loads(data)
    file_name = f"node{data[1]}.json"
    file_copy_name = f"node{data[1]}_copy.json"
    try:
        f = open(file_name, "x")
        f.close()
        f_c = open(file_copy_name, "x")
        f_c.close()

    except FileExistsError:
        pass

    size_file = os.path.getsize(file_name)
    print(size_file)
    if size_file == 0:
        with open(file_name, 'r+') as file:
            file.write("""{
        "messages": [

        ]
    }""")
    with open(file_name, 'r+') as file_:
        file_data = json.load(file_)
        file_data["messages"].append(data[0])
        file_.seek(0)
        json.dump(file_data, file_, indent=4)

    shutil.copy(file_name, file_copy_name)
    return "message was sent", 200


if(__name__ == '__main__'):
    app.run(host=HOST, port=port)