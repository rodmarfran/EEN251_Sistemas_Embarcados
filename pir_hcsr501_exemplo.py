"""!
@file pir_hcsr501_exemplo.py
@author Rodrigo França
@brief PIR HC-SR501 Sensor com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do sensor de movimento PIR HC-SR501
         e exibir no console se o movimento foi detectado ou encerrado. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor.
         Referência: https://lastminuteengineers.com/pir-sensor-arduino-tutorial/
@date 2023-03-17
"""

# Importa a classe Pin da biblioteca machine para controlar os pinos do Raspberry Pi Pico
from machine import Pin

# Define o pino do Raspberry Pi Pico conectado ao módulo PIR HC-SR501
pir_pin = 15

# Variável global para armazenar o estado atual do PIR HC-SR501
pir_state = 0
# Variável global para armazenar o estado anterior do PIR HC-SR501
pir_last_state = 0

# Habilita o uso de interrupção para o PIR HC-SR501
enable_irq = True

# Configura o pino do PIR HC-SR501 como entrada
pir = Pin(pir_pin, Pin.IN)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do PIR HC-SR501
    def pir_callback(pin):
        # Atualiza a variável global pir_state com o valor do pino
        global pir_state
        pir_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado do PIR HC-SR501 (borda de subida e descida)
    pir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=pir_callback)

# Atualiza o estado atual e anterior do PIR HC-SR501
pir_state = pir.value()
pir_last_state = pir.value()

# Imprime mensagem inicial
print("Se aproxime do PIR HC-SR501 para testá-lo!")

# Loop Infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do PIR HC-SR501
        pir_state = pir.value()

    # Verifica se ocorreu uma borda de subida no sinal do PIR HC-SR501
    if pir_state == 1 and pir_last_state == 0:
        # Atualiza o estado anterior do PIR HC-SR501
        pir_last_state = 1
        # Imprime que foi detectado um movimento pelo PIR HC-SR501
        print("Movimento detectado!")

    # Verifica se ocorreu uma borda de descida no sinal do PIR HC-SR501
    elif pir_state == 0 and pir_last_state == 1:
        # Atualiza o estado anterior do PIR HC-SR501
        pir_last_state = 0
        # Imprime que o movimento detectado pelo PIR HC-SR501 foi encerrado
        print("Movimento encerrado!")
