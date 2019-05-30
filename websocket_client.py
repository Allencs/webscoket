import ssl
import json
import time
from threading import Thread
import threading
import websocket
import socket
from group_code import group_code

socket.setdefaulttimeout(20)


# 单点：wss://10.203.109.106:8443/websocket
# 群发：wss://10.203.109.143/websocket


class WebSocketClient(object):
    def __init__(self):
        self.p2p_ws_address = "wss://10.203.109.106:8443/websocket"
        self.group_ws_address = "wss://10.203.109.143/websocket"
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE},
                                      sockopt=socket.setdefaulttimeout(20))

    def p2p_client(self, num):
        self.ws.connect(self.p2p_ws_address)
        print(self.p2p_ws_address)
        registry_data = {
            "command": "REGISTER",
            "userInfo": {
                "accessToken": "user",
                "channelCode": "pol4s"}
        }

        registry_data['userInfo']['accessToken'] = "user{}".format(num)

        registry_data = json.dumps(registry_data)

        self.ws.send(registry_data)

        self.recv_msg()

    def recv_msg(self):
        while True:
            msg = self.ws.recv()
            if msg is not None:
                # print("Server response: {}".format(msg))
                print("{} response: {}".format(threading.currentThread().getName(), msg))

            else:
                time.sleep(0.5)

    def group_client(self, num):
        self.ws.connect(self.group_ws_address)
        print(self.group_ws_address)
        registry_data = {
            "command": "REGISTER",
            "userInfo": {
                "accessToken": "user01",
                "channelCode": "pol4s",
                "groupCode": ["239FA44E0AC449C59D5B06D81DF8DA9D"]
            }
        }

        registry_data['userInfo']['groupCode'] = group_code

        registry_data['userInfo']['accessToken'] = "user{}".format(num)

        registry_data = json.dumps(registry_data)

        self.ws.send(registry_data)

        print("Server response: {}".format(self.ws.recv()))

    def multi_p2p_client(self):
        for i in range(1, 101):
            td_socket = Thread(target=self.p2p_client, args=(i,),
                               name="client_{}".format(i))
            td_socket.start()

    def multi_group_client(self):
        for i in range(1, 101):
            td_socket = Thread(target=self.group_client, args=(i,),
                               name="client_{}".format(i))
            td_socket.start()


if __name__ == '__main__':
    ws_client = WebSocketClient()
    """
    # 群发：wss://10.203.109.143/websocket
    # 点对点：wss://10.203.109.106:8443/websocket
    """
    # ws_client.p2p_client(1)
    ws_client.group_client(1)




