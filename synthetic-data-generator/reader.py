import os
import csv
import socket
import time

os.environ['SOCK_LISTENER_HOST']
os.environ['SOCK_LISTENER_PORT']
os.environ['SLEEP_TIME']

with open("UDP_107_108.csv", 'r') as file:
  csvreader = csv.reader(file)
  send_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  for row in csvreader:
    row[0]=row[0].replace('"', '')
    aux = row[0].split(";")
    # if(aux[2]!="Y"):
    #     result = f"0;{aux[7]};{aux[6]};{aux[1]};{aux[2]};{aux[3]};{aux[4]};{aux[5]};0"
    #     send_server_socket.sendto(bytes(result, "utf-8"),(os.getenv("SOCK_LISTENER_HOST"),int(os.getenv("SOCK_LISTENER_PORT"))))
    #     print(result)
    #     time.sleep(0.2)
    if(aux[0] == "107"):
      # result = f"{Id_mensaje};{timestamp};T{Tag_id};{X};{Y};{Z};{HPL};{VPL};{SingularMatrix}"
      result = f"{aux[0]};{aux[1]};T{aux[3]};{aux[4]};{aux[5]};{aux[6]};{aux[7]};{aux[8]};{aux[9]}"
      print(result)
    else:
      result = f"{aux[0]};{aux[1]};T{aux[2]};{aux[3]}"
    send_server_socket.sendto(bytes(result, "utf-8"),(os.getenv("SOCK_LISTENER_HOST"),int(os.getenv("SOCK_LISTENER_PORT"))))
    time.sleep(float(os.getenv("SLEEP_TIME")))