import ssl
import json
import time
from threading import Thread
import threading
import websocket
import socket
from group_code import group_code

socket.setdefaulttimeout(20)


# 单点：wss://***/websocket
# 群发：wss://***/websocket


class WebSocketClient(object):

    conns = {}

    def __init__(self):
        self.p2p_ws_address = "wss://***/websocket"
        self.group_ws_address = "wss://***/websocket"
        self.own_address = "ws://10.203.29.217:8085/spring_websocket/websocket/"
        # self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE},
        #                               sockopt=socket.setdefaulttimeout(20))

    def p2p_client(self, num):
        ws = websocket.create_connection(self.own_address,
                                         sslopt={"cert_reqs": ssl.CERT_NONE},
                                         sockopt=socket.setdefaulttimeout(20))
        # print(self.p2p_ws_address)
        registry_data = {
            "command": "REGISTER",
            "userInfo": {
                "accessToken": "user",
                "channelCode": "pol4s"}
        }

        registry_data['userInfo']['accessToken'] = "user{}".format(num)

        self.conns["user{}".format(num)] = ws

        registry_data = json.dumps(registry_data)

        ws.send(registry_data)

    def recv_msg(self):
        while True:
            for conn in self.conns:
                msg = self.conns[conn].recv()
                if msg is not None:
                    print("{} --> response: {}".format(conn, msg))
                    print("{} response: {}".format(threading.currentThread().getName(), msg))

                else:
                    time.sleep(0.5)

    def group_client(self, num):
        print(self.group_ws_address)
        # self.ws.connect(self.group_ws_address)
        ws = websocket.create_connection(self.group_ws_address,
                                         sslopt={"cert_reqs": ssl.CERT_NONE},
                                         sockopt=socket.setdefaulttimeout(20))
        registry_data = {
            "command": "REGISTER",
            "userInfo": {
                "accessToken": "user01",
                "channelCode": "***",
                "groupCode": ["239FA44E0AC449C59D5B06D81DF8DA9D"]
            }
        }

        registry_data['userInfo']['groupCode'] = group_code

        registry_data['userInfo']['accessToken'] = "user{}".format(num)

        registry_data = json.dumps(registry_data)

        ws.send(registry_data)

        print("Server response: {}".format(ws.recv()))

        self.recv_msg()

    def multi_p2p_client(self):
        for i in range(1, 20):
            self.p2p_client(i)
        time.sleep(30)

    def multi_group_client(self):
        for i in range(1, 101):
            td_socket = Thread(target=self.group_client, args=(i,),
                               name="client_{}".format(i))
            td_socket.start()


if __name__ == '__main__':
    ws_client = WebSocketClient()
    """
    # 群发：
    # 点对点：
    """
    ws_client.multi_p2p_client()
    # ws_client.group_client(1)




