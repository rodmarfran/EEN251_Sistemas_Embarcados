"""!
@file bmp280_exemplo.py
@brief Programa para ler o sensor BMP280 usando o Raspberry Pi Pico e MicroPython.
@details Este programa utiliza a biblioteca bmp280 para ler os valores do sensor BMP280 via barramento I2C.
         A temperatura e a pressão são exibidas no console a cada segundo.
         Referência: https://github.com/dafvid/micropython-bmp280
@autor Rodrigo França
@data 17/03/2023
"""

import machine
import utime
import bmp280

# Inicializa o sensor BMP280
# Utiliza o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=100000)
# Utiliza o I2C1 com os pinos GPIO7 (SCL) e GPIO6 (SDA)
#i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6), freq=100000)
bmp = bmp280.BMP280(i2c)

# Loop principal
while True:
    # Lê a temperatura e a pressão do sensor
    temp = bmp.temperature
    press = bmp.pressure
    
    # Exibe os valores lidos no console
    print("Temperatura: {:.2f} C".format(temp))
    print("Pressão: {:.2f} Pa".format(press))
    
    # Aguarda 1 segundo antes de ler novamente
    utime.sleep(1)
