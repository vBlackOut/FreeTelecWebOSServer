import logging
from websocket_server import WebsocketServer
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import time

# def new_client(client, server):
# 	server.send_message_to_all("Hey all, a new client has joined us")

adbkey = '/home/pi/.android/adbkey'
with open(adbkey) as f:
    priv = f.read()
with open(adbkey + '.pub') as f:
     pub = f.read()
signer = PythonRSASigner(pub, priv)


cmd = {
    "mute": "input keyevent 164",
    "down": "input keyevent 20",
    "up": "input keyevent 19",
    "left": "input keyevent 21",
    "right": "input keyevent 22",
    "red": "input keyevent 183",
    "green": "input keyevent 184",
    "yellow": "input keyevent 185",
    "blue": "input keyevent 186",
    "home": "input keyevent 3",
    "rec": "input keyevent 130",
    "bwd": "input keyevent 275",
    "prev": ["input keyevent 88", "input keyevent 89"],
    "play": ["input keyevent 126", "input keyevent 85"],
    "fwd": "input keyevent 90",
    "next": ["input keyevent 87", "input keyevent 90"],
    "ok": ["input keyevent 66", "input keyevent 23"],
    "vol_inc": "input keyevent 24",
    "vol_dec": "input keyevent 25",
    "pause": "input keyevent 127",
    "prgm_inc": "input keyevent 166",
    "prgm_dec": "input keyevent 167",
    "0": "input keyevent {}".format(0+7),
    "1": "input keyevent {}".format(1+7),
    "2": "input keyevent {}".format(2+7),
    "3": "input keyevent {}".format(3+7),
    "4": "input keyevent {}".format(4+7),
    "5": "input keyevent {}".format(5+7),
    "6": "input keyevent {}".format(6+7),
    "7": "input keyevent {}".format(7+7),
    "8": "input keyevent {}".format(8+7),
    "9": "input keyevent {}".format(9+7)
}

# Connect
device1 = AdbDeviceTcp('SERVER_ADB', 5555, default_transport_timeout_s=9.)
device1.connect(rsa_keys=[signer], auth_timeout_s=2)

def message(client, server, message):
    list_commande = []
    for i in message:
        try:
            list_commande.append(cmd[i])
        except KeyError:
            break

    send_command = list_commande
    if isinstance(send_command, list):
        for i in send_command:
            print(device1.shell(i))
    else:
        print(device1.shell(send_command))

    print("chaine input : ", message)

server = WebsocketServer(9000, host='ADDRESS_HOST')
#server.set_fn_new_client(new_client)
server.set_fn_message_received(message)
server.run_forever()
