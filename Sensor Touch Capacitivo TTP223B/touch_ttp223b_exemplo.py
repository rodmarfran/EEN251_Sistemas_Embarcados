"""!
@file touch_ttp223b_exemplo.py
@author Rodrigo França
@brief Sensor Touch Capacitivo TTP223B com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do sensor touch capacitivo TTP223B
         e exibir no console se um toque foi detectado ou encerrado. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor.
         Referência: https://www.robocore.net/sensor-ambiente/sensor-touch-capacitivo-ttp223b/
@date 2023-03-17
"""

# Importa a classe Pin da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin

# Define o pino do Raspberry Pi Pico conectado ao módulo TTP223B
touch_pin = 15

# Variável global para armazenar o estado atual do sensor
touch_state = 0
# Variável global para armazenar o estado anterior do sensor
touch_last_state = 0

# Habilita o uso de interrupção para o sensor
enable_irq = True

# Configura o pino da saída digital do sensor
touch = Pin(touch_pin, Pin.IN)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do sensor
    def touch_callback(pin):
        # Atualiza a variável global touch_state com o valor do pino
        global touch_state
        touch_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado do TTP223B (borda de subida e descida)
    touch.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=touch_callback)

# Atualiza o estado atual e anterior da saída digital do sensor
touch_state = touch.value()
touch_last_state = touch.value()

# Imprime mensagem inicial
print("Toque no sensor TTP223B para testá-lo!")

# Verifica o estado inicial do sensor
if touch == 1:
    # Imprime que foi detectado um toque no TTP223B
    print("Toque detectado!")
else:
    # Imprime que não foi detectado um toque no TTP223B
    print("Toque não detectado!")

# Loop infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do sensor
        touch_state = touch.value()

    # Verifica se ocorreu uma borda de subida no sinal do sensor
    if touch_state == 1 and touch_last_state == 0:
        # Atualiza o estado anterior do sensor
        touch_last_state = 1
        # Imprime que foi detectado um toque no TTP223B
        print("Toque detectado!")

    # Verifica se ocorreu uma borda de descida no sinal do sensor
    elif touch_state == 0 and touch_last_state == 1:
        # Atualiza o estado anterior do sensor
        touch_last_state = 0
        # Imprime que o toque detectado no TTP223B foi encerrado
        print("Toque encerrado!")
