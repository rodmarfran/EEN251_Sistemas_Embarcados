"""!
@file dht11_exemplo.py
@brief Programa para leitura de dados de um sensor DHT11 usando o Raspberry Pi Pico e MicroPython.
@details Este programa utiliza a biblioteca dht para ler os valores do sensor DHT11.
         A temperatura e a umidade são exibidas no console a cada dois segundos.
         Referência: https://docs.micropython.org/en/latest/esp8266/tutorial/dht.html
@autor Rodrigo França
@data 17/03/2023
"""

import machine
import utime
import dht

# Configuração do sensor DHT11
# Configurando o pino do sensor DHT11 como entrada
dht_pin = machine.Pin(2, machine.Pin.IN)
# Configurando o pino do sensor DHT11 como entrada com resistência pull-up
#dht_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

# Criando um objeto DHT11 com o pino configurado acima
dht_sensor = dht.DHT11(dht_pin)

# Leitura de dados do sensor DHT11
while True:
    try:
        # Fazendo a leitura do sensor
        dht_sensor.measure()
        # Obtendo a temperatura e a umidade
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        # Imprimindo os valores obtidos no console
        print("Temperatura: {:.1f}°C".format(temp))
        print("Umidade: {:.1f}%".format(hum))
    except OSError as e:
        # Tratando possíveis erros na leitura do sensor
        print("Erro ao ler dados do sensor:", e)

    # Aguardando 2 segundos antes de realizar uma nova leitura
    utime.sleep(2)
