import math
from machine import Pin, Timer
from time import sleep_us

class Dimmer:
    def __init__(self, zero_cross_pin, triac_pin):
        """
        Inicializa el dimmer.
        
        :param zero_cross_pin: Pin conectado a la detección de cruce por cero.
        :param triac_pin: Pin conectado al TRIAC.
        :param half_cycle_us: Duración de medio ciclo en microsegundos (8333 us para 60 Hz).
        :param default_intensity: Intensidad inicial (valor entre 0 y 100).
        """
        self.zero_cross_pin = Pin(zero_cross_pin, Pin.IN)
        self.triac_pin = Pin(triac_pin, Pin.OUT)
        self.half_cycle_us = 8333
        self.intensity = 0.06
        self.timer = Timer(0)

        # Configura la interrupción para detectar cruces por cero
        self.zero_cross_pin.irq(trigger=Pin.IRQ_RISING, handler=self._zero_cross_detected)

    def update_intensity(self, value):
        """Actualiza la intensidad del dimmer."""
        if 0 <= value <= 100:
            # Evita valores demasiado bajos para garantizar que el TRIAC se dispare
            self.intensity = max(value / 100, 0.06)  # Mínimo 6% de intensidad
        else:
            raise ValueError("La intensidad debe estar entre 0 y 100.")

    def _trigger_triac(self, timer):
        """Dispara el TRIAC después de un retraso calculado."""
        delay = (1 - math.sqrt(self.intensity)) * self.half_cycle_us
        sleep_us(int(delay))
        self.triac_pin.value(1)
        sleep_us(20)  # Pulso de 20 us para encender el TRIAC
        self.triac_pin.value(0)

    def _zero_cross_detected(self, pin):
        """Dispara el TRIAC en el momento calculado después del cruce por cero."""
        self.timer.init(period=1, mode=Timer.ONE_SHOT, callback=self._trigger_triac)