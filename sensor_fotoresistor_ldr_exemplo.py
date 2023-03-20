"""!
@file sensor_fotoresistor_ldr_exemplo.py
@author Rodrigo França
@brief Sensor Fotoresistor LDR com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do sensor fotoresistor LDR
         e exibir no console se o ambiente está claro ou escuro. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor.
         Referência: https://blogmasterwalkershop.com.br/arduino/como-usar-com-arduino-modulo-fotoresistor-sensor-ldr/
@date 2023-03-17
"""

# Importa as classes Pin, ADC e Timer da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, ADC, Timer
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define o pino do Raspberry Pi Pico conectado à saída digital do sensor fotoresistor LDR
ldr_digital_pin = 15

# Define o pino do Raspberry Pi Pico conectado à saída analógica do sensor fotoresistor LDR
ldr_analog_pin = 26

# Tempo de debounce para o sensor fotoresistor LDR em ms
debounce_time_ms = 10

# Variável global para armazenar o estado atual do sensor fotoresistor LDR
ldr_state = 0
# Variável global para armazenar o estado anterior do sensor fotoresistor LDR
ldr_last_state = 0

# Habilita o uso de interrupção para o sensor fotoresistor LDR
enable_irq = True

# Configura o pino da saída digital do sensor fotoresistor LDR como entrada
ldr_digital = Pin(ldr_digital_pin, Pin.IN)

# Instancia o objeto ADC para leitura da saída analógica do sensor fotoresistor LDR
ldr_analog = ADC(Pin(ldr_analog_pin))

# Instancia um objeto Timer para criar um temporizador para leitura da saída analógica do sensor fotoresistor LDR
timer = Timer()

# Função temporizada para leitura da saída analógica do sensor fotoresistor LDR 
def ldr_analog_read(timer):
    # Lê o valor da entrada analógica do sensor fotoresistor LDR como um valor positivo de 16 bits
    ldr_analog_value = ldr_analog.read_u16()
    # Converte o valor analógica na forma de um valor positivo de 16 bits para tensão (valor de um bit = 3.3/(2^16 - 1) = 3.3/65535)
    ldr_voltage = ldr_analog_value / 65535 * 3.3

    # Imprime o valor da tensão lida
    print("Tensão lida: {:.2f} V".format(ldr_voltage))
    
# Configurando o Timer para chamar a função ldr_analog_read em intervalos de tempo fixos (1Hz = 1s)
timer.init(freq=1, mode=Timer.PERIODIC, callback=ldr_analog_read)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do sensor fotoresistor LDR
    def ldr_callback(pin):
        # Atualiza a variável global ldr_state com o valor do pino
        global ldr_state
        ldr_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado do sensor fotoresistor LDR (borda de subida e descida)
    ldr_digital.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=ldr_callback)
    
# Atualiza o estado atual e anterior do sensor fotoresistor LDR
ldr_state = ldr_digital.value()
ldr_last_state = ldr_digital.value()

# Imprime mensagem inicial
print("Coloque o sensor fotoresistor LDR na luz para testá-lo!")

# Loop infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do sensor fotoresistor LDR
        ldr_state = ldr_digital.value()
        
    # Verifica se o estado do sensor fotoresistor LDR mudou
    if ldr_state != ldr_last_state:
        # Aguarda um período para fazer o debounce do sensor fotoresistor LDR
        utime.sleep_ms(debounce_time_ms)
        # Verifica se a interrupção está desabilitada
        if not enable_irq:
            # Lê o estado do sensor fotoresistor LDR
            ldr_state = ldr_digital.value()

    # Verifica se ocorreu uma borda de subida no sinal do sensor fotoresistor LDR
    if ldr_state == 1 and ldr_last_state == 0:
        # Atualiza o estado anterior do sensor fotoresistor LDR
        ldr_last_state = 1
        # Imprime que foi detectado um ambiente escuro pelo sensor fotoresistor LDR
        print("Ambiente escuro!")

    # Verifica se ocorreu uma borda de descida no sinal do sensor fotoresistor LDR
    elif ldr_state == 0 and ldr_last_state == 1:
        # Atualiza o estado anterior do sensor fotoresistor LDR
        ldr_last_state = 0
        # Imprime que o ambiente detectado pelo sensor fotoresistor LDR ficou claro
        print("Ambiente claro!")
