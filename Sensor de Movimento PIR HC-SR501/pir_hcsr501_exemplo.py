"""!
@file pir_hcsr501_exemplo.py
@brief Sensor de Movimento PIR HC-SR501 com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do sensor de movimento PIR HC-SR501
         e exibir no console se o movimento foi detectado ou encerrado. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor.
         Referência: https://lastminuteengineers.com/pir-sensor-arduino-tutorial/
@author Rodrigo França
@date 2023-03-17
"""

# Importa a classe Pin da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin

# Define o pino do Raspberry Pi Pico conectado ao módulo PIR HC-SR501
pir_pin = 15

# Variável global para armazenar o estado atual do sensor
pir_state = 0
# Variável global para armazenar o estado anterior do sensor
pir_last_state = 0

# Habilita o uso de interrupção para o sensor
enable_irq = True

# Configura o pino da saída digital do sensor
pir = Pin(pir_pin, Pin.IN)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do sensor
    def pir_callback(pin):
        # Atualiza a variável global pir_state com o valor do pino
        global pir_state
        pir_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado do PIR HC-SR501 (borda de subida e descida)
    pir.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=pir_callback)

# Atualiza o estado atual e anterior da saída digital do sensor
pir_state = pir.value()
pir_last_state = pir.value()

# Imprime mensagem inicial
print("Se aproxime do PIR HC-SR501 para testá-lo!")

# Verifica o estado inicial do sensor
if pir == 1:
    # Imprime que foi detectado um movimento pelo PIR HC-SR501
    print("Movimento detectado!")
else:
    # Imprime que não foi detectado um movimento pelo PIR HC-SR501
    print("Movimento não detectado!")

# Loop infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do sensor
        pir_state = pir.value()

    # Verifica se ocorreu uma borda de subida no sinal do sensor
    if pir_state == 1 and pir_last_state == 0:
        # Atualiza o estado anterior do sensor
        pir_last_state = 1
        # Imprime que foi detectado um movimento pelo PIR HC-SR501
        print("Movimento detectado!")

    # Verifica se ocorreu uma borda de descida no sinal do sensor
    elif pir_state == 0 and pir_last_state == 1:
        # Atualiza o estado anterior do sensor
        pir_last_state = 0
        # Imprime que o movimento detectado pelo PIR HC-SR501 foi encerrado
        print("Movimento encerrado!")
