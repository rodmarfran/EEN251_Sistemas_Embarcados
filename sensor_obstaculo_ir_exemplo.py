"""!
@file sensor_obstaculo_ir_exemplo.py
@author Rodrigo França
@brief Sensor de obstáculo infravermelho com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do sensor de obstáculo infravermelho
         e exibir no console se um obstáculo foi detectado ou removido. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor e possui um debounce do sensor.
         Referência: https://www.eletrogate.com/sensor-de-obstaculo-reflexivo-infravermelho
@date 2023-03-17
"""

# Importa a classe Pin da biblioteca machine para controlar os pinos do Raspberry Pi Pico
from machine import Pin
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define o pino do Raspberry Pi Pico conectado ao módulo sensor de obstáculo infravermelho
obstacle_pin = 15

# Tempo de debounce para o sensor de obstáculo infravermelho em ms
debounce_time_ms = 10

# Variável global para armazenar o estado atual do sensor de obstáculo infravermelho
obstacle_state = 0
# Variável global para armazenar o estado anterior do sensor de obstáculo infravermelho
obstacle_last_state = 0

# Habilita o uso de interrupção para o sensor de obstáculo infravermelho
enable_irq = True

# Configura o pino do sensor de obstáculo infravermelho como entrada
obstaculo = Pin(obstacle_pin, Pin.IN)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do sensor de obstáculo infravermelho
    def obstacle_callback(pin):
        # Atualiza a variável global obstacle_state com o valor do pino
        global obstacle_state
        obstacle_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado do sensor de obstáculo infravermelho (borda de subida e descida)
    obstacle.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=obstacle_callback)

# Atualiza o estado atual e anterior do sensor de obstáculo infravermelho
obstacle_state = obstacle.value()
obstacle_last_state = obstacle.value()

# Imprime mensagem inicial
print("Coloque um obstáculo na frente do sensor de obstáculo infravermelho para testá-lo!")

# Loop Infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do sensor de obstáculo infravermelho
        obstacle_state = obstacle.value()
        
    # Verifica se o estado do sensor de obstáculo infravermelho mudou
    if obstacle_state != obstacle_last_state:
        # Aguarda um período para fazer debounce do sensor de obstáculo infravermelho
        utime.sleep_ms(debounce_time_ms)
        # Verifica se a interrupção está desabilitada
        if not enable_irq:
            # Lê o estado do sensor de obstáculo infravermelho
            obstacle_state = obstacle.value()

    # Verifica se ocorreu uma borda de subida no sinal do sensor de obstáculo infravermelho
    if obstacle_state == 0 and obstacle_last_state == 1:
        # Atualiza o estado anterior do sensor de obstáculo infravermelho
        obstacle_last_state = 0
        # Imprime que foi detectado um obstáculo no sensor de obstáculo infravermelho
        print("Obstáculo detectado!")

    # Verifica se ocorreu uma borda de descida no sinal do sensor de obstáculo infravermelho
    elif obstacle_state == 1 and obstacle_last_state == 0:
        # Atualiza o estado anterior do sensor de obstáculo infravermelho
        obstacle_last_state = 1
        # Imprime que o obstáculo detectado pelo sensor de obstáculo infravermelho foi removido
        print("Obstáculo removido!")
