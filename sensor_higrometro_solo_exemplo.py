"""!
@file sensor_higrometro_solo_exemplo.py
@author Rodrigo França
@brief Sensor de Umidade do Solo (Higrômetro de Solo) com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do sensor higrômetro de solo
         e exibir no console se o solo está umido ou não. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor.
         Referência: https://www.eletrogate.com/modulo-sensor-de-umidade-de-solo/
@date 2023-03-17
"""

# Importa as classes Pin, ADC e Timer da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, ADC, Timer
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define o pino do Raspberry Pi Pico conectado à saída digital do sensor higrômetro de solo
hygrometer_digital_pin = 15

# Define o pino do Raspberry Pi Pico conectado à saída analógica do sensor higrômetro de solo
hygrometer_analog_pin = 26

# Tempo de debounce para o sensor higrômetro de solo em ms
debounce_time_ms = 10

# Variável global para armazenar o estado atual do sensor higrômetro de solo
hygrometer_state = 0
# Variável global para armazenar o estado anterior do sensor higrômetro de solo
hygrometer_last_state = 0

# Habilita o uso de interrupção para o sensor higrômetro de solo
enable_irq = True

# Configura o pino da saída digital do sensor higrômetro de solo como entrada
hygrometer_digital = Pin(hygrometer_digital_pin, Pin.IN)

# Instancia o objeto ADC para leitura da saída analógica do sensor higrômetro de solo
hygrometer_analog = ADC(Pin(hygrometer_analog_pin))

# Instancia um objeto Timer para criar um temporizador para leitura da saída analógica do sensor higrômetro de solo
timer = Timer()

# Função temporizada para leitura da saída analógica do sensor higrômetro de solo 
def hygrometer_analog_read(timer):
    # Lê o valor da entrada analógica do sensor higrômetro de solo como um valor positivo de 16 bits
    hygrometer_analog_value = hygrometer_analog.read_u16()
    # Converte o valor analógica na forma de um valor positivo de 16 bits para tensão (valor de um bit = 3.3/(2^16 - 1) = 3.3/65535)
    hygrometer_voltage = hygrometer_analog_value / 65535 * 3.3

    # Imprime o valor da tensão lida
    print("Tensão lida: {:.2f} V".format(hygrometer_voltage))
    
# Configurando o Timer para chamar a função hygrometer_analog_read em intervalos de tempo fixos (1Hz = 1s)
timer.init(freq=1, mode=Timer.PERIODIC, callback=hygrometer_analog_read)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do sensor higrômetro de solo
    def hygrometer_callback(pin):
        # Atualiza a variável global hygrometer_state com o valor do pino
        global hygrometer_state
        hygrometer_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado do sensor higrômetro de solo (borda de subida e descida)
    hygrometer_digital.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=hygrometer_callback)
    
# Atualiza o estado atual e anterior do sensor higrômetro de solo
hygrometer_state = hygrometer_digital.value()
hygrometer_last_state = hygrometer_digital.value()

# Imprime mensagem inicial
print("Coloque o sensor higrômetro de solo na terra para testá-lo!")

# Verifica o estado inicial do sensor higrômetro de solo
if hygrometer_state == 1:
    # Imprime que o solo está seco
    print("Solo seco!")
else:
    # Imprime que o solo está úmido
    print("Solo úmido!")

# Loop infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do sensor higrômetro de solo
        hygrometer_state = hygrometer_digital.value()
        
    # Verifica se o estado do sensor higrômetro de solo mudou
    if hygrometer_state != hygrometer_last_state:
        # Aguarda um período para fazer o debounce do sensor higrômetro de solo
        utime.sleep_ms(debounce_time_ms)
        # Verifica se a interrupção está desabilitada
        if not enable_irq:
            # Lê o estado do sensor higrômetro de solo
            hygrometer_state = hygrometer_digital.value()

    # Verifica se ocorreu uma borda de subida no sinal do sensor higrômetro de solo
    if hygrometer_state == 1 and hygrometer_last_state == 0:
        # Atualiza o estado anterior do sensor higrômetro de solo
        hygrometer_last_state = 1
        # Imprime que foi detectado solo seco pelo sensor higrômetro de solo
        print("Solo seco!")

    # Verifica se ocorreu uma borda de descida no sinal do sensor higrômetro de solo
    elif hygrometer_state == 0 and hygrometer_last_state == 1:
        # Atualiza o estado anterior do sensor higrômetro de solo
        hygrometer_last_state = 0
        # Imprime que foi detectado solo úmido pelo sensor higrômetro de solo
        print("Solo úmido!")
