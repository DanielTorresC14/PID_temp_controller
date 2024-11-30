from utime import sleep, sleep_ms
from onewire import OneWire
from ds18x20 import DS18X20
from machine import Pin
    
def ds18b20_read_temp(sensor_pin):
    """Lee la temperatura de un sensor ds18b20."""
    ds_bus = OneWire(Pin(sensor_pin))
    ds_sensor = DS18X20(ds_bus)
    roms = ds_sensor.scan()
    ds_sensor.convert_temp()
    sleep_ms(750)
    rom = roms[0]
    temp = ds_sensor.read_temp(rom)
    return temp