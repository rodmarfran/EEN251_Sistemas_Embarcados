"""!
@file bmp280_exemplo.py
@brief Programa para ler o sensor BMP280 usando o  e Raspberry Pi Pico.
@details Este programa utiliza a biblioteca bmp280 para ler os valores do sensor BMP280 via barramento I2C.
         A temperatura e a pressão são exibidas no console a cada segundo.
         Referência: https://github.com/dafvid/micropython-bmp280
@author Rodrigo França
@date 2023-03-17
"""

# Importa as classes Pin e I2C da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, I2C
# Importa a classe BMP280 da biblioteca bmp280.py
from bmp280 import BMP280
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define os pinos do Raspberry Pi Pico conectados ao barramento I2C 0
i2c0_slc_pin = 9
i2c0_sda_pin = 8

# Inicializa o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
i2c0 = I2C(0, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=100000)

# Inicializa o sensor BMP280
bmp280 = BMP280(i2c0)

# Loop infinito
while True:
    
    # Lê a temperatura e a pressão do sensor
    bmp280_temp = bmp280.temperature
    bmp280_press = bmp280.pressure
    
    # Exibe os valores lidos no console
    print("Temperatura: {:.2f} C".format(bmp280_temp))
    print("Pressão: {:.2f} Pa".format(bmp280_press))
    
    # Aguarda 1 segundo antes de ler novamente
    utime.sleep(1)
