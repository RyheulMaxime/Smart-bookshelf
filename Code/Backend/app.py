from os import WIFSIGNALED
import time
from RPi import GPIO
import spidev
from smbus import SMBus
import subprocess  
import threading
import serial
from datetime import datetime, date
# from rpi_ws281x import *
# import argparse

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request, redirect
from repositories.DataRepository import DataRepository

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 21
GPIO.setup(PIR_PIN, GPIO.IN)

spi = spidev.SpiDev() 
spi.open(0, 1)   # Bus SPI0, slave op CE 1
spi.max_speed_hz = 1000000 # 100 kHz

# rfid = spidev.SpiDev() 
# rfid.open(0, 0)   # Bus SPI0, slave op CE 0
# rfid.max_speed_hz = 1000000 # 1000 kHz

i2c = SMBus()
RS = 17
E = 27
GPIO.setup(RS, GPIO.OUT) 
GPIO.setup(E, GPIO.OUT) 
GPIO.output(E,GPIO.HIGH)
i2c.open(1)

rfid_nieuw_book = 0
positie_nieuw_book = 0
list_ldr = [1,2,3,4,5]
status_ldr = []
previous_state = []
bool_ldr = 0
bool_nieuw_book = 0


# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)

# global operatoren:
idboek = 0

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


#  ldr **********************
def read_channel(ch):
        list_ch = [0x1, (8 |ch)<<4, 0x0] 
        list_bytes = spi.xfer(list_ch)
        waarde = ((list_bytes[1] & 3) << 8) | list_bytes[2]
        # print(f"Waarde : {waarde}")
        return waarde

def lees_ldr(i):
    waarde = read_channel(i)
    # print(waarde)
    time.sleep(0.5)
    return waarde


# bepaal kleur ledstrip
def bapaal_kleur(datum):
    inleverdatum = datetime.strptime(datum, '%Y-%m-%d')
    print(datum)
    # print(date.today())
    dagen_voor_inleveren = (inleverdatum - datetime.now()).days
    # print(dagen_voor_inleveren)
    if dagen_voor_inleveren > 21:
        kleur = "green"
    elif dagen_voor_inleveren > 14:
        kleur = "yellow"
    elif dagen_voor_inleveren > 7:
        kleur = "orange"
    else:
        kleur = "red"
    print(kleur)
    return kleur

def toon_led():
    ser = serial.Serial('/dev/serial0')   # open serial port
    posities = DataRepository.get_info_led()
    for positie in posities:
        if positie["kleur ledstrip"] == "red":
            ser.write(b'red')
        elif positie["kleur ledstrip"] == "green":
            ser.write(b'green')
        elif positie["kleur ledstrip"] == "yellow":
            ser.write(b'yellow')
        elif positie["kleur ledstrip"] == "orange":
            ser.write(b'orange')
        else:
            ser.write(b'white')
        
        time.sleep(2)

# lcd *******************
def init_LCD():
    send_instruction(0b00111000)
    send_instruction(0b00001100)
    send_instruction(0b00000001)

def send_character(value):
    GPIO.output(RS,GPIO.HIGH)
    i2c.write_byte(0x38, value)
    GPIO.output(E,GPIO.LOW)
    GPIO.output(E,GPIO.HIGH)
    time.sleep(0.01)
    
def send_instruction(value):
    GPIO.output(RS,GPIO.LOW)
    i2c.write_byte(0x38, value)
    GPIO.output(E,GPIO.LOW)
    GPIO.output(E,GPIO.HIGH)
    time.sleep(0.01)

def write_message(message):
    for char in message:
        send_character(ord(char))

def clear_LCD():
    send_instruction(0b00000001)

time.sleep(5)
init_LCD()
clear_LCD()
ips = str(subprocess.check_output(['hostname','--all-ip-addresses']).decode('utf-8'))
print(ips)
ips = ips.split(" ")
write_message(ips[0])  


# thread ****************************************

def lees_alle_ldr(chn):
    if GPIO.input(chn):
        print('Motion Detected')
        global status_ldr, bool_ldr, previous_state
        if bool_ldr != 1:
            DataRepository.toevoegen_waarde(6,1)
            if status_ldr != []:
                previous_state = status_ldr
            status_ldr = []
            for ldr in list_ldr:
                waarde = lees_ldr(ldr-1)
                DataRepository.toevoegen_waarde(ldr,waarde)
                status_ldr.append(waarde)

            if previous_state != []:    
                for i in range(0,5):
                    if previous_state[i] < (status_ldr[i] - 100):
                        DataRepository.uit_kast_nemen(i+1)

            print(status_ldr)
            
        else:
            print("pauze voor rfid")
        
        toon_led()


def lees_rfid():
    with serial.Serial('/dev/serial0', 9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=1) as port:
        while True:
            global status_ldr, bool_ldr

            # get rfid tag book
            rfid_input = port.readline().rstrip().decode()
            rfid_list = rfid_input.split(' ')
            rfid_tag = rfid_list[1]+ rfid_list[2] + rfid_list[3]+ rfid_list[4]
            print(rfid_tag)
            DataRepository.toevoegen_waarde(7,rfid_tag)
            
            bool_ldr = 1
            # print(rfid_list)
            time.sleep(10)
            current_status_ldr = []
            for ldr in list_ldr:
                waarde = lees_ldr(ldr-1)
                DataRepository.toevoegen_waarde(ldr,waarde)
                current_status_ldr.append(waarde)
            print(current_status_ldr) 

            # get position book with rfid tag
            positie_boek = 0
            for i in range(0,5):
                if current_status_ldr[i] - status_ldr[i] > 75:
                    print(i+1)
                    positie_boek = i+1
            
            bestaand = 0
            # check if rfid is asingned to book
            info_rfid = DataRepository.get_info_rfid()
            # print(info_rfid)
            for book in info_rfid:
                # print(book["rfid"])
                if book["rfid"] == rfid_tag:
                    bestaand = 1
                    # rfid tag is ocupied with book

                    # print(book["idboek"])
                    
                    # check if rfid was not positioned somwere else 
                    aanwezig = 0
                    info_positie = DataRepository.get_info_positie()
                    
                    for positie in info_positie:
                        if positie["idboek"] == book["idboek"]:
                            # change location book
                            DataRepository.indiennen_boek(book["idboek"])
                            DataRepository.set_position_book(book["idboek"],positie["kleur ledstrip"],positie_boek)
                            # print("ok")
                            aanwezig = 1
                            
                    if aanwezig == 0:
                        # place book on that position
                        kleur = bapaal_kleur(book["inleverdatum"]) 
                        DataRepository.set_position_book(book["idboek"],kleur,positie_boek)
                        
            # not a current book
            if bestaand == 0:
                global rfid_nieuw_book, positie_nieuw_book
                rfid_nieuw_book = rfid_tag
                positie_nieuw_book = positie_boek
                data = {"positie":positie_nieuw_book,"rfid":rfid_nieuw_book}
                print(data)
                # emit('B2F_check_book', {'info': ''}, broadcast=True)
                

            bool_ldr = 0
            
  


GPIO.add_event_detect(21, GPIO.RISING, lees_alle_ldr, bouncetime=200)

thread_rfid = threading.Timer(1, lees_rfid)
thread_rfid.start()




print("**** Program started ****")

# API ENDPOINTS

@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    data = DataRepository.read_status_positions()
    emit('B2F_status_positions', {'positions': data}, broadcast=True)

@socketio.on('F2B_check_nieuw_book')
def detect_nieuw_book():
    global rfid_nieuw_book, positie_nieuw_book
    if positie_nieuw_book != 0 and rfid_nieuw_book != 0:
        emit('B2F_check_book', {"positie":positie_nieuw_book}, broadcast=True)

@socketio.on('F2B_status_position')
def status_position():
    # Ophalen van de data
    data = DataRepository.read_status_positions()
    socketio.emit('B2F_status_positions', {'positions': data}, broadcast=True)
    
@socketio.on('F2B_idboek')
def set_id_book(id):
    global idboek
    print('get id boek')
    print(id)
    idboek = id

@socketio.on("F2B_infoboek")
def get_info_boek():
    # print("idboek")
    # print(idboek)
    data = DataRepository.read_info_boek(idboek)
    socketio.emit('B2F_info_boek', {'boek': data}, broadcast=True)

@socketio.on("F2B_Aanpassenboek")
def get_info_aanpassen():
    # print("idboek")
    # print(idboek)
    data = DataRepository.read_librarys()
    socketio.emit('B2F_Librarys', {'librarys': data}, broadcast=True)
    
    if idboek != 0:
        print("ok")
        data = DataRepository.read_info_boek(idboek)
        socketio.emit('B2F_Aanpassen_boek', {'boek': data}, broadcast=True)

@socketio.on("F2B_verleng_4")
def verleng_4_weeken():
    global idboek
    DataRepository.verleng_boek_4_weken(idboek)
    color = DataRepository.get_datum(idboek)
    print(color)
    kleur = bapaal_kleur(color["inleverdatum"])
    
    DataRepository.verander_kleur(idboek,kleur)
    idboek = 0

@socketio.on("F2B_verleng")
def verleng_boek(date):
    global idboek
    DataRepository.verleng_boek(idboek,date)
    kleur = bapaal_kleur(date)
    DataRepository.verander_kleur(idboek,kleur)
    idboek = 0
    
@socketio.on("F2B_indiennen")
def indiennen_boek():
    global idboek
    DataRepository.indiennen_boek_RFID(idboek)
    DataRepository.indiennen_boek(idboek)
    idboek = 0
    
@socketio.on("F2B_aanpassen")
def aanapssen_boek(json):
    global idboek, rfid_nieuw_book, positie_nieuw_book
    if idboek != 0:
        # print(json)
        data = DataRepository.read_librarys()
        for library in data:
            # print(library)
            if library["naam"] == json["library"]:
                idbib = library["idbibliotheek"]
                # print(idbib)
        DataRepository.aanpassen_boek(json["name"],json["author"], idbib ,json["indiennen"], idboek)
    else:
        data = DataRepository.read_librarys()
        for library in data:
            # print(library)
            if library["naam"] == json["library"]:
                idbib = library["idbibliotheek"]
        
        DataRepository.put_nieuw_book(json["name"],json["author"],rfid_nieuw_book,idbib,json["indiennen"])
        idboek = DataRepository.get_id_nieuw_book(json["name"],json["author"],rfid_nieuw_book,idbib,json["indiennen"])
        kleur = bapaal_kleur(json["indiennen"]) 
        print(idboek)
        DataRepository.set_position_book(idboek["idboek"],kleur,positie_nieuw_book)

        rfid_nieuw_book = 0
        positie_nieuw_book = 0
    idboek = 0

@socketio.on('F2B_previous_books')
def status_position():
    # Ophalen van de data
    data = DataRepository.read_previous_books()
    socketio.emit('B2F_previous_books', {'books': data}, broadcast=True)

@socketio.on('F2B_libraries')
def read_library():
    # Ophalen van de data
    data = DataRepository.read_librarys()
    socketio.emit('B2F_libraries', {'libraries': data}, broadcast=True)

@socketio.on('F2B_sutddown')
def sut_down():
    print("shut down")
    subprocess.call("echo W8w00rd | sudo -S shutdown -h now", shell=True)

# @socketio.on("F2B_shutdown")
# def shutdown():
#     ser.close()
#     subprocess.run(['echo "W8w00rd" | sudo -S -k reboot'])


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')