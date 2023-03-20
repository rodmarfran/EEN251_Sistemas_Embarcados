"""!
@file touch_ttp223b_exemplo.py
@author Rodrigo França
@brief Sensor Touch Capacitivo TTP223B com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do Sensor Touch Capacitivo TTP223B
         e exibir no console se um toque foi detectado ou encerrado. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor.
         Referência: https://www.robocore.net/sensor-ambiente/sensor-touch-capacitivo-ttp223b/
@date 2023-03-17
"""

# Importa a classe Pin da biblioteca machine para controlar os pinos do Raspberry Pi Pico
from machine import Pin

# Define o pino do Raspberry Pi Pico conectado ao módulo TTP223B
touch_pin = 15

# Variável global para armazenar o estado atual do TTP223B
touch_state = 0
# Variável global para armazenar o estado anterior do TTP223B
touch_last_state = 0

# Habilita o uso de interrupção para o TTP223B
enable_irq = True

# Configura o pino do TTP223B como entrada
touch = Pin(touch_pin, Pin.IN)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do TTP223B
    def touch_callback(pin):
        # Atualiza a variável global touch_state com o valor do pino
        global touch_state
        touch_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado do TTP223B (borda de subida e descida)
    touch.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=touch_callback)

# Atualiza o estado atual e anterior do TTP223B
touch_state = touch.value()
touch_last_state = touch.value()

# Imprime mensagem inicial
print("Toque no sensor TTP223B para testá-lo!")

# Loop Infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do TTP223B
        touch_state = touch.value()

    # Verifica se ocorreu uma borda de subida no sinal do TTP223B
    if touch_state == 1 and touch_last_state == 0:
        # Atualiza o estado anterior do TTP223B
        touch_last_state = 1
        # Imprime que foi detectado um toque no TTP223B
        print("Toque detectado!")

    # Verifica se ocorreu uma borda de descida no sinal do TTP223B
    elif touch_state == 0 and touch_last_state == 1:
        # Atualiza o estado anterior do TTP223B
        touch_last_state = 0
        # Imprime que o toque detectado no TTP223B foi encerrado
        print("Toque encerrado!")
