import serial

serial_port = serial.Serial(port='COM3', baudrate=9600)

while True:
    serial_code = serial_port.read(2)
    print(serial_code)
