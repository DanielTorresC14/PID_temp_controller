import urequests
import utime as time

from machine import Pin
from read_temp import ds18b20_read_temp
from network import WLAN, STA_IF
from dimmer import Dimmer
from pid import  PID

def connect_wifi(ssid, password):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    print('connecting to ' + ssid)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('.', end='')
        utime.sleep(1)
    print('IP address', wlan.ifconfig()[0])
    
connect_wifi('Metallica', 'enter sandman')

url = "http://192.168.0.22:8080/data"

dimmer = Dimmer(zero_cross_pin=15, triac_pin=2)

pid = PID(Kp=52.6, Ki=28.6, Kd=0.96, setpoint=30, output_limits=(0, 100))

data = {}

interval = 1000
base_time = time.ticks_ms()
while True:
    try:
        # Lee la temeperatura actual y la almacena para ser enviada.
        current_temp = ds18b20_read_temp(4)
        data['temp'] = current_temp
        
        # Calcula la salida segun el setpoint.
        current_brightness = pid.compute(current_temp)
        data['brightness'] = current_brightness
        
        # Manda informacion al servidor.
        response = urequests.post(url, json=data)
        print("Respuesta del servidor:", response.json()['setpoint'])
        response.close()
        
        # Intervalo fijo para actualizar el PID
        base_time = time.ticks_add(base_time, interval)
        time.sleep(max(0, time.ticks_diff(base_time, time.ticks_ms()) / 1000.0))
    
    # Posibles Excepciones.
    except Exception as e:
        print("Error al enviar datos:", e)
        break
    except KeyboardInterrupt as e:
        print("Programa interrumpido por el usuario")
        break