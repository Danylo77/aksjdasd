import requests
import json
from flask import Flask

HOST = 'http://127.0.0.1:'
app = Flask(__name__)


class Client:

    def __init__(self, address: str):
        self.address = address
        self.max_node = None
        self.min_node = None
        self.number_of_tries = 3
        self.current_try_number = 0

    def uptd(self):
        temp = requests.get(self.address + '/get_stats').content
        temp = temp.decode('utf-8')
        print(temp)
        temp = temp.replace("[", "")
        temp = temp.replace("]", "")
        temp = temp.replace("\"", "")
        temp = temp.replace("\n", "")
        temp = temp.split(",")
        self.min_node = temp[0]
        self.max_node = temp[1]

        print(self.min_node)
        print(self.max_node)

        self.current_try_number = (self.current_try_number + 1) % self.number_of_tries

    def read(self):
        self.__update_stats_()
        return json.loads(requests.get(HOST + self.max_node + '/read_message', data=self.max_node).text)

    def write(self, message):
        self.__update_stats_()
        res = requests.get(f"{HOST}{self.min_node}/write_msg", data=json.dumps(({"msg": message}, self.min_node)))
        return res.content.decode("utf-8"), res.status_code

    def __update_stats_(self):
        if self.current_try_number == 0:
            temp = requests.get(self.address + '/get_stats').content
            temp = temp.decode('utf-8')
            print(temp)
            temp = temp.replace("[", "")
            temp = temp.replace("]", "")
            temp = temp.replace("\"", "")
            temp = temp.replace("\n", "")
            temp = temp.split(",")
            self.min_node = temp[0]
            self.max_node = temp[1]

            print(self.min_node)
            print(self.max_node)

        self.current_try_number = (self.current_try_number + 1) % self.number_of_tries


client_1 = Client("http://127.0.0.1:5000")

if __name__ == ("__main__"):
    app.run(port=5001)