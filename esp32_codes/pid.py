import time

class PID:
    def __init__(self, Kp, Ki, Kd, setpoint, output_limits=(0, 100)):
        """
        Inicializa el controlador PID.
        
        :param Kp: Ganancia proporcional.
        :param Ki: Ganancia integral.
        :param Kd: Ganancia derivativa.
        :param setpoint: Valor deseado del sistema.
        :param output_limits: Tupla con los límites de la salida (mín, máx).
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.output_limits = output_limits

        self.last_error = 0
        self.integral = 0
        self.last_time = time.ticks_ms()

    def compute(self, feedback):
        """
        Calcula la salida del PID.
        
        :param feedback: Valor actual del sistema (retroalimentación).
        :return: Valor de salida del PID (control).
        """
        current_time = time.ticks_ms()
        dt = time.ticks_diff(current_time, self.last_time) / 1000  # Tiempo en segundos
        if dt <= 0:
            dt = 1e-3  # Evita divisiones por cero

        # Cálculo del error
        error = self.setpoint - feedback

        # Componente proporcional
        P = self.Kp * error

        # Componente integral
        #self.integral += error * dt
        self.integral = max(min(self.integral, self.output_limits[1]), self.output_limits[0])
        I = self.Ki * self.integral

        # Componente derivativo
        derivative = (error - self.last_error) / dt
        D = self.Kd * derivative

        # Salida total
        output = P + I + D

        # Limita la salida a los valores permitidos
        output = max(self.output_limits[0], min(output, self.output_limits[1]))

        # Guarda valores para el siguiente ciclo
        self.last_error = error
        self.last_time = current_time

        return output