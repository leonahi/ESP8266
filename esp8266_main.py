import serial
import time

SSID = "Beetle"
PWD = "area asus bangalore"

IP = "api.thingspeak.com"
PORT = "80"
DEST_HOST = "api.thingspeak.com"
REQUEST_PAGE = "/update?key=OUCPBKR9ZISMGJHY&field1=30&headers=false"

HTTP_REQUEST = "GET " + REQUEST_PAGE + " HTTP/1.1\r\nHost: " + DEST_HOST + "\r\n" + "\r\n\r\n"


ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=2)

def sendCommand(cmd, ack, delay=1):
    print("Sending Command : {0}".format(cmd))
    ser.flushInput()
    cmd += '\r\n'
    ser.write(cmd)
    time.sleep(delay)
    while ser.inWaiting()!=0:
        ret = ser.readline().strip()
        print(ret)
        if ret == ack:
            print(ret)
            break
        time.sleep(.5)
        
def sendRequest(cmd, data, delay=1):
    REQUEST_PAGE = "/update?key=OUCPBKR9ZISMGJHY&field1={0}&headers=false".format(data)
    HTTP_REQUEST = "GET " + REQUEST_PAGE + " HTTP/1.1\r\nHost: " + DEST_HOST + "\r\n" + "\r\n\r\n"
    
    ser.flushInput()
    cmd += str(len(HTTP_REQUEST))
    cmd += '\r\n'
 
    ser.write(cmd)
    time.sleep(delay)
    while ser.inWaiting()!=0:
        ret = ser.readline().strip()
        print(ret)
        if ret == '>':
            print(ret)
            break
        time.sleep(.2)
    ser.write(HTTP_REQUEST)
    time.sleep(1)
    

def main():
    sendCommand('AT', 'OK', 1)
    
    # Reset esp8266
    sendCommand('AT+RST', 'ready', 1)
    
    # Get firmaware version
    sendCommand('AT+GMR', 'OK', 1)
    
    # Change Wifi mode = 1(station), 2(AP), 3(station and AP)
    sendCommand('AT+CWMODE=1', 'OK', 1)
    
    sendCommand('AT+CWJAP=' + '\"' + SSID + '\"' + ',' + '\"' + PWD + '\"', 'OK', 5)
    
    sendCommand('AT+CWJAP=?', 'OK', 2)
    
    sendCommand('AT+CIPSTATUS', 'OK', 1)
    
    sendCommand('AT+CIPSTART=\"TCP\",' + '\"' + IP + '\"' ',' + PORT, 1)
    
    sendCommand('AT+CIPSTATUS', 'OK', 1)
                
    sendRequest('AT+CIPSEND=', 10, 1)
    
    while ser.inWaiting()!=0:
        print(ser.readline())
        time.sleep(1)


if __name__ == "__main__":
    main()
