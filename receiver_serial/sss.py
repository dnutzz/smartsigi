import os,sys,datetime,time
import serial
import requests
import json
import random

RECBUFFER_SIZE = 1024*4
SS_BACKEND = 'http://127.0.0.1:5000/api/addSnapshot'
POST_HEAD = {
              'Accept': 'application/json',
              'Accept-encoding': 'gzip, deflate',
              'Content-Type': 'application/json'  
            }


# configure the serial connections (the parameters differs on the device you are connecting to)
def open_serial():
  ser = serial.Serial(
      port='/dev/ttyS0',
      baudrate=115200,
      stopbits=serial.STOPBITS_ONE,
      parity=serial.PARITY_NONE,
      bytesize=serial.EIGHTBITS,
      timeout=1
  )
  print("port is open" if ser.isOpen() else "port is closed")
  return ser
  
def writeLog(str):
  with open("sss_log.txt", "a+") as w:
    w.write(datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + " error: " + str + "\n")

# read serial input and create dict with data
def read_dict():
  # busy wait read serial until newline
  inp_str = ''   
  while('\r\n' not in inp_str and len(inp_str) < RECBUFFER_SIZE):
    while(not ser.inWaiting()):
      time.sleep(0.1)      
    inp = ser.read(ser.inWaiting())
    inp_str+=inp.decode()
  indict = dict()
  # decode into string and strip newline
  inp_str = inp_str.rstrip()
  # loop trough string delimited by ;
  for item in inp_str.split(';'):
    # skip "PKT" and empty items
    if(item != 'PKT' and item != ''):
      k,v=item.split('=')
      # add to dictionary
      indict[k] = v
  return(indict)

# convert temp/100 to float    
def tempFloat(str):
  return int(str)/100.0
        
# main loop
def main(ser):
  while 1 :
    input_dict = read_dict()
    if(input_dict):
      request_dict = dict()
      request_dict['temp'] = tempFloat(input_dict.pop('TEMP'))
      request_dict['label_id'] = input_dict.pop('SRC')
      request_dict['debug'] = input_dict
      response = requests.post(SS_BACKEND, headers=POST_HEAD, data=json.dumps(request_dict))
        
if __name__ == '__main__':
  try:
    ser = open_serial()
    main(ser)
  except KeyboardInterrupt:
    print("KeyboardInterrupt\nexiting...")
    ser.close()
    sys.exit(0)
  except SystemExit:
    print("SystemExit\nexiting...")
    ser.close()
    os._exit(0)
