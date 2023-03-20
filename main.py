"""!
@file main.py
@brief Programa para fazer um LED piscar em um intervalo de tempo fixo usando o Raspberry Pi Pico e MicroPython.
@details Este programa usa a biblioteca 'machine.Timer`'para configurar um timer que faz um LED piscar em um intervalo de tempo fixo.
         Referência: https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/5
@autor Rodrigo França
"""

import machine

# Configurando o LED e o Timer
led = machine.Pin(25, machine.Pin.OUT)
timer = machine.Timer()

# Função para fazer o LED piscar
def blink(timer):
    led.toggle()

# Configurando o Timer para chamar a função blink em intervalos de tempo fixos
timer.init(freq=2.5, mode=machine.Timer.PERIODIC, callback=blink)
