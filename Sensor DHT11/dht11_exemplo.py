"""!
@file dht11_exemplo.py
@brief Programa para leitura de dados de um sensor DHT11 usando o Raspberry Pi Pico.
@details Este programa utiliza a biblioteca dht para ler os valores do sensor DHT11.
         A temperatura e a umidade são exibidas no console a cada dois segundos.
         Referência: https://docs.micropython.org/en/latest/esp8266/tutorial/dht.html
@author Rodrigo França
@date 2023-03-17
"""

# Importa as classe Pin da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin
# Importa a classe DHT11 da biblioteca dht.py
from dht import DHT11
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define os pinos do Raspberry Pi Pico conectados ao sensor DHT11
dht11_pin = 2

# Criando um objeto DHT11 com pino do sensor como entrada sem pull-up
dht11_sensor = DHT11(Pin(dht11_pin, Pin.IN))

# Criando um objeto DHT11 com pino do sensor como entrada com pull-up
#dht11_sensor = DHT11(Pin(dht11_pin, Pin.IN, Pin.PULL_UP))

# Loop infinito
while True:
    
    # Tenta realizar uma medição com o sensor
    try:
        
        # Fazendo a leitura do sensor
        dht11_sensor.measure()
        
        # Obtendo a temperatura e a umidade
        dht11_temp = dht11_sensor.temperature()
        dht11_humid = dht11_sensor.humidity()
        
        # Imprimindo os valores obtidos no console
        print("Temperatura: {:.1f}°C".format(dht11_temp))
        print("Umidade: {:.1f}%".format(dht11_humid))
        
    # Erro de sistema durante a medição do sensor
    except OSError as e:
        
        # Tratando possíveis erros na leitura do sensor
        print("Erro ao ler dados do sensor:", e)

    # Aguardando 2 segundos antes de realizar uma nova leitura
    utime.sleep(2)
