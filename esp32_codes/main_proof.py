import utime as time

from machine import Pin, UART
from pid import PID
from dimmer import Dimmer
from read_temp import ds18b20_read_temp

# Configuración de pines y dispositivos
sensor_pin = 4
dimmer = Dimmer(zero_cross_pin=15, triac_pin=2)

# Configuración del PID
pid = PID(Kp=52.6, Ki=28.6, Kd=0.96, setpoint=30, output_limits=(0, 100))  # Límite de 0% a 100%

# Intervalo de tiempo entre acciones.
interval = 1000  # Un segundo.

base_time = time.ticks_ms()
while True:
    try:
        # Lee la temperatura actual del sensor DS18B20
        current_temp = ds18b20_read_temp(sensor_pin)

        # Calcula la salida del PID
        output = pid.compute(current_temp)

        # Actualiza la intensidad del dimmer
        dimmer.update_intensity(output)

        # Intervalo fijo para actualizar el PID
        base_time = time.ticks_add(base_time, interval)
        time.sleep(max(0, time.ticks_diff(base_time, time.ticks_ms()) / 1000.0))

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)