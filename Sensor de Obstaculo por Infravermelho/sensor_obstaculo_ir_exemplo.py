
"""!
@file sensor_obstaculo_ir_exemplo.py
@brief Sensor de Obstáculo por Infravermelho com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do sensor de obstáculo infravermelho
         e exibir no console se um obstáculo foi detectado ou removido. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor e possui um debounce do sensor.
         Referência: https://www.eletrogate.com/sensor-de-obstaculo-reflexivo-infravermelho
@author Rodrigo França
@date 2023-03-17
"""

# Importa a classe Pin da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define o pino do Raspberry Pi Pico conectado ao módulo sensor de obstáculo infravermelho
obstacle_pin = 15

# Tempo de debounce para o sensor em ms
debounce_time_ms = 10

# Variável global para armazenar o estado atual do sensor
obstacle_state = 0
# Variável global para armazenar o estado anterior do sensor
obstacle_last_state = 0

# Habilita o uso de interrupção para o sensor
enable_irq = True

# Configura o pino da saída digital do sensor
obstacle = Pin(obstacle_pin, Pin.IN)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do sensor
    def obstacle_callback(pin):
        # Atualiza a variável global obstacle_state com o valor do pino
        global obstacle_state
        obstacle_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado do sensor de obstáculo infravermelho (borda de subida e descida)
    obstacle.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=obstacle_callback)

# Atualiza o estado atual e anterior da saída digital do sensor
obstacle_state = obstacle.value()
obstacle_last_state = obstacle.value()

# Imprime mensagem inicial
print("Coloque um obstáculo na frente do sensor de obstáculo infravermelho para testá-lo!")

# Verifica o estado inicial do sensor
if obstacle == 1:
    # Imprime que não foi detectado um obstáculo no sensor de obstáculo infravermelho
    print("Obstáculo não detectado!")
else:
    # Imprime que foi detectado um obstáculo no sensor de obstáculo infravermelho
    print("Obstáculo detectado!")

# Loop infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do sensor
        obstacle_state = obstacle.value()
        
    # Verifica se o estado do sensor mudou
    if obstacle_state != obstacle_last_state:
        # Aguarda um período para fazer o debounce
        utime.sleep_ms(debounce_time_ms)
        # Verifica se a interrupção está desabilitada
        if not enable_irq:
            # Lê o estado do sensor
            obstacle_state = obstacle.value()

    # Verifica se ocorreu uma borda de subida no sinal do sensor
    if obstacle_state == 1 and obstacle_last_state == 0:
        # Atualiza o estado anterior do sensor
        obstacle_last_state = 0
        # Imprime que o obstáculo detectado pelo sensor de obstáculo infravermelho foi removido
        print("Obstáculo removido!")

    # Verifica se ocorreu uma borda de descida no sinal do sensor
    elif obstacle_state == 0 and obstacle_last_state == 1:
        # Atualiza o estado anterior do sensor
        obstacle_last_state = 1
        # Imprime que foi detectado um obstáculo no sensor de obstáculo infravermelho
        print("Obstáculo detectado!")
