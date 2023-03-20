"""!
@file hcsr04_exemplo.py
@author Rodrigo França
@brief Script principal para medir a distância usando o módulo ultrassônico HC-SR04 e Raspberry Pi Pico
@details Este script demonstra como utilizar a biblioteca hcsr04.py para medir a distância usando um sensor ultrassônico HC-SR04 e um Raspberry Pi Pico rodando MicroPython.
         Referência: https://randomnerdtutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/
@date 2023-03-17
"""

# Importa a classe HCSR04 da biblioteca hcsr04.py
from hcsr04 import HCSR04
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define os pinos do Raspberry Pi Pico conectados ao módulo HC-SR04
trigger_pin = 16
echo_pin = 17

# Instancia o objeto HCSR04 com os pinos definidos
sensor = HCSR04(trigger_pin, echo_pin)

# Loop infinito para medir a distância continuamente
while True:
    # Obtém a distância medida pelo sensor HC-SR04
    distance_cm = sensor.get_distance_cm()
    
    # Imprime a distância formatada no console
    print("Distância: {:.2f} cm".format(distance_cm))

    # Aguarda 1 segundo antes de medir a distância novamente
    utime.sleep(1)
