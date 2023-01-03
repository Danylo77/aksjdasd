import json
import os
import requests
from flask import Flask, render_template, request, flash
import client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jadsjasid'


class MainNode:
    def __init__(self, port):
        self.port = port
        self.ports = [5002]

    def add_port(self, port):
        self.ports.append(port)

    def del_port(self, port):
        self.ports.remove(port)


main_node = MainNode(5000)



@app.route('/')
def index2():
    return render_template('index.html')


@app.route('/msg', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg_to_write_web = request.form['message']
        client.client_1.write(msg_to_write_web)
        print(request.form['message'])
    elif request.method == 'GET':
        msg_to_read_web = str(client.client_1.read())
        flash(msg_to_read_web[9:-2])
    index2()
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        msg_add_node = request.form['message']
        print(msg_add_node)
        main_node.add_port(int(msg_add_node))
    return render_template('index.html')


@app.route('/del', methods=['POST'])
def del_port():
    if request.method == 'POST':
        msg_add_node = request.form['message']
        print(msg_add_node)
        main_node.del_port(int(msg_add_node))
        os.remove(f"node{msg_add_node}.json")
        client.client_1.uptd()
        index2()
    return render_template('index.html')


@app.route('/get_stats', methods=['GET', 'POST'])
def get_stats():
    arr = []
    min_port = 0
    min = 1000
    max_port = 0
    max = 0

    for i in main_node.ports:
        if not os.path.isfile(f"node{i}.json"):
            min_port = i
            break
        f = open(f"node{i}.json")
        ob = json.load(f)
        if min > len(ob["messages"]):
            min = len(ob["messages"])
            min_port = i
        f.close()

    arr.append(min_port)
    status_max = False
    for i in main_node.ports:
        if os.path.isfile(f"node{i}.json"):
            f = open(f"node{i}.json")
            ob = json.load(f)
            if max < len(ob["messages"]):
                max = len(ob["messages"])
                status_max = True
                max_port = i
            f.close()

    if not status_max:
        max_port = min_port

    arr.append(max_port)
    print(arr)
    return arr, 200


if __name__ == ("__main__"):
    app.run(port=5000)
