import time

from machine import Pin
from pid import PID
from dimmer import Dimmer
from read_temp import ds18b20_read_temp

# Configuración de pines y dispositivos
sensor_pin = 4

# Intervalo de tiempo entre acciones.
interval = 1000 # Un segundo

base_time = time.ticks_ms()
while True:
    try:
        # Lee la temperatura actual del sensor DS18B20.
        current_temp = ds18b20_read_temp(sensor_pin)
        print(f"Temperatura actual: {current_temp:.2f} °C")

        # Intervalo fijo para actualizar el PID
        base_time = time.ticks_add(base_time, 1000)  # Próximo en 1 segundo
        waiting_time = max(0, time.ticks_diff(base_time, time.ticks_ms()) / 1000.0)
        time.sleep(waiting_time)
        print(waiting_time)
    except KeyboardInterrupt:
        print("Programa finalizado por el usuario.")
        break
    except Exception as e:
        print(f"Error: {e}")