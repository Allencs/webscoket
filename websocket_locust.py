from locust import Locust, events, TaskSequence, seq_task, TaskSet, task
import websocket
import time
import ssl
import json
import traceback
import socket


###############################################
# 测试项目：WebSocket4.0
# 作者：allen
# 业务功能：维持WebSocket连接数、接收推送消息
###############################################

"""
url:
    # 群发：***
    # 点对点：***
"""


def on_locust_error(locust_instance, exception, tb):
    print("%r, %s, %s" % (locust_instance, exception, "".join(traceback.format_tb(tb))))


def on_hatch_complete(user_count):
    print("HaHa, Locust have generate %d users" % user_count)


# def on_request_success(request_type, name, response_time, response_length):
#     print('Type: %s, Name: %s, Time: %fms, Response Length: %d' %
#           (request_type, name, response_time, response_length))


class WebSocketClient(object):
    def __init__(self):
        self.create_connection = None
        self.send_msg = None
        # self.host = host
        self.ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE},
                                      sockopt=socket.setdefaulttimeout(120))

    def connect(self, url):
        start_time = time.time()
        try:
            self.create_connection = self.ws.connect(url)
        except websocket.WebSocketException as error:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="WebSocket",
                                        name='Connect',
                                        response_time=total_time,
                                        exception=error)
            return -1
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="WebSocket",
                                        name='Connect',
                                        response_time=total_time,
                                        response_length=0)

    def registry(self, msg):
        start_time2 = time.time()
        try:
            self.send_msg = self.ws.send(msg)
        except websocket.WebSocketException as error:
            total_time2 = int((time.time() - start_time2) * 1000)
            events.request_failure.fire(request_type="WebSocket",
                                        name='Registry',
                                        response_time=total_time2,
                                        exception=error)
        else:  # 等待WebSocket返回消息，并将等待时间计入响应时间内
            while True:
                if self.ws.recv() == "SUCCESS":
                    total_time2 = int((time.time() - start_time2) * 1000)
                    events.request_success.fire(request_type="WebSocket",
                                                name='Registry',
                                                response_time=total_time2,
                                                response_length=0)
                    break

        return self.send_msg

    def recv(self):
        start_time3 = time.time()
        try:
            recv_message = self.ws.recv()
            msg_length = len(recv_message)
        except websocket.WebSocketException as error:
            total_time3 = int((time.time() - start_time3) * 1000)
            events.request_failure.fire(request_type="WebSocket",
                                        name='RecvMsg',
                                        response_time=total_time3,
                                        exception=error)
        else:  # 等待WebSocket返回消息，并将等待时间计入响应时间内
            while True:
                if self.ws.recv() is not None:
                    total_time3 = int((time.time() - start_time3) * 1000)
                    events.request_success.fire(request_type="WebSocket",
                                                name='RecvMsg',
                                                response_time=total_time3,
                                                response_length=msg_length)
                    break

            return recv_message

    def close_ws(self):
        return self.ws.close()


class WebSocketLocust(Locust):
    def __init__(self):
        super(WebSocketLocust, self).__init__()
        self.client = WebSocketClient()


class RetainConnection(TaskSequence):

    @seq_task(1)
    class SubTaskSet(TaskSequence):
        status = None

        @seq_task(1)
        def connect(self):
            
            info = self.client.connect("wss://***/websocket")
            if info == -1:
                self.status = -1

        @seq_task(2)
        def abort(self):  # 退出直接等待
            if self.status is not None:
                self.interrupt()
            pass

        @seq_task(3)
        def registry(self):
            msg = {
                "command": "REGISTER",
                "userInfo": {
                    "accessToken": "user01",
                    "channelCode": "pol4s",
                    "groupCode": ["239FA44E0AC449C59D5B06D81DF8DA9D", "BDE2C0F487BB4F528B76D10C3D7421C4",
                                  "B9817CAC457643ED9D07ABBDABE529D4", "C25B8467F71D46CBA92B1D8276118CC4",
                                  "3E2A8991E1A3430DA3719188DF8F2881", "CDB7F6D0B4E742DE9B89D96092818F32",
                                  "48371DE0C12349DAAF8E16366FDE0012", "BF7613DA95A847228CB4BFFA2D6E248D",
                                  "2D2ED1CFB65A43E7AFE59377EAD05F32", "76E3EF0810984F1D94FDA116263BB5A7",
                                  "FF23BCEB512A4F10B97802332D61562A", "9E006C7F3DCC483FAFB3C706FDA7E364",
                                  "6148075524FA4A2C970956C2AFD31F36", "5CF9AABA43F145319575C463181CE805",
                                  "CE81EF32EB424FAB93054A7A06A48695", "D512152BEE1145628A3F4325E2CF2A58",
                                  "16AE6FCC4B714C11AD7F4F8698B030DC", "C60AD8212646488295ADED92AC589051",
                                  "41356B33C6B5471E92CA388D3AFADB15", "503BA340F6EB45AD918BD5E0E809BD73",
                                  "F972400741F94ED0A6C7B3092B36BE13", "2683D269C24C4BEF97944AC30535DC66",
                                  "1D9FEE54135E4EE4B3C45041E087AD52", "4C1EFE46DD7146F88793B10C56366AA1",
                                  "5B8D8AC2E4A5499BBAC43E75A94330FD", "4691F530822448F18936CAD1A35B692A",
                                  "744D77B399E5459C9C773D6FAE1FBAD8", "93F0EF2C3605423C858743A28D95A7A6",
                                  "3757847E5FCE40EEA542097902969C06", "EA415DCCF79D45A1886E77FF9EE18D4B",
                                  "A1DA3B02EC5242E091E45804E15CCFA0", "2C686BC9270D4A70AEFCE4955A897699",
                                  "605DC69B12A14BEDA1DEC57224EEB04B", "2E13F0CB3D574C27A315A23636384B83",
                                  "D65C8C0E516341F78829D478052EF7E3", "793825D0A4F14E80B08939EC853027CB",
                                  "A25511993A4A43B8805CA907F0F31FA0", "C7081E701A0D4806972444B88022147B",
                                  "115D063FC4AA4923B1D5598C3C59CF9A", "AE999E0965034848966AC6613404409C",
                                  "9440A695B89440AF9922537698747E3C", "E718EA5D3D774890A7261C5D1B1D11DF",
                                  "90153F99C7A240DEB85F950D0990054C", "F3959BA5775C418CABCCE3DDFBF1B42E",
                                  "0A9B3FB7122840C896135399E9E4490F", "E2D60CC0A6CA41D08D25D37BA7894F34",
                                  "91CC47948767493796C16EB9A591AA99", "2DD23E200079423F8F1DE8BE22AAEFD6",
                                  "BDA0F11C52D449C58372759F4D3CA7E1", "D300A12EC8FA49C4B08780DFB51EF5D2",
                                  "AAA14D12C9C04588AA3A9F6B642F908D", "9EBE44BBB93F4F4BAB62269E5906CF26",
                                  "44A235BAC143457FBB4BE3C174B4BB18", "FCE87C6A29934BE4A08B6054B3A945D4",
                                  "B857F944DF354FE5A0A7CC114286215B", "EAE190349DF04B0188E895D392E7EB71",
                                  "7F469AEE1332415F8A378D9BCF8A47E7", "3B8DEE1D0864458691D1A010A9359F93",
                                  "0323D516D9E040CDAD4B954B1AA5E23E", "67912E98D2A04303BC7B023C34C7D5B6",
                                  "05A866448E77452DBBBBBF3438379D70", "AB17D074C6AA44BC9F49F549EDF4AC85",
                                  "B819320C0C364E7682545699F40B7C10", "933714B735CE4661AB58D3459C3770EB",
                                  "47B6D708BCA8465A947DB3E4C0CBDC18", "A3F8014B2A224DDEAC6FAFB060FA94D7",
                                  "9488886911394CB4AD6D453932703A8A", "1DDA2743719A42B392EFB33AEF00FC85",
                                  "AC2D83EE99464F688879A97AF332E0DF", "281E3E32B03F4F30A36AFB7405C1F8B3",
                                  "2335DA5294FC41BFB5E74C6E6CDBD127", "84016C13DCFE4F4CADD2871BF029281B",
                                  "463CBF263678406CAB5917463A29F6FD", "1D026CE6AC0F46DBA204CD75D915A907",
                                  "BD0F5B88F24443AAB522FFDB3CFC3A1A", "FC8E49B5281B42D8B0754A0BB9798A18",
                                  "07340E2F8BF44A2191EB3B5F00E0028A", "F40D14DA72BB4B81B30FFC23DA5CC5A4",
                                  "3072FD7781484043A8C3EC083EC7EB98", "A1D56E856B5A41BA8E450B74A226C764",
                                  "01A728385E924B838F6BBB2B86E0326B", "A83E888DC9DB4748905EB8BE5985D92C",
                                  "3C401886D0D04DC3AAE7640FB8516717"]
                }
            }
            # msg = {
            #     "command": "REGISTER",
            #     "userInfo": {
            #         "accessToken": "user1",
            #         "channelCode": "***"
            #     }
            # }
            submit_data = json.dumps(msg)
            self.client.registry(submit_data)
            time.sleep(1800)

    @seq_task(2)
    def wait_to_stop(self):
        time.sleep(1800)


class RecvPushedMsg(TaskSet):
    status = None

    def on_start(self):
        self.connect()
        self.registry()

    def connect(self):
        info = self.client.connect("wss://***/websocket")
        if info == -1:
            self.status = -1

    def registry(self):
        msg = {
            "command": "REGISTER",
            "userInfo": {
                "accessToken": "518b16713b81a444b4e01fb44d532dfc",
                "channelCode": "pol4s",
                "groupCode": ["239FA44E0AC449C59D5B06D81DF8DA9D"]
            }
        }
        submit_data = json.dumps(msg)
        self.client.registry(submit_data)

    @task
    def recv_msg(self):
        self.client.recv()


events.locust_error += on_locust_error
events.hatch_complete += on_hatch_complete
# events.request_success += on_request_success


class MyWebSocketLocust(WebSocketLocust):
    task_set = RetainConnection
    min_wait = 200
    max_wait = 500

