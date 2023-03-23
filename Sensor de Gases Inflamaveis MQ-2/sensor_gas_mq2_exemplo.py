"""!
@file sensor_gas_mq2_exemplo.py
@author Rodrigo França
@brief Sensor de Gases Inflamáveis MQ-2 com Raspberry Pi Pico
@details Este programa utiliza a Raspberry Pi Pico para ler o estado do sensor de gases inflamáveis MQ-2
         e exibir no console se foi detectado gás inflamável ou não. O código permite o uso de interrupções
         para lidar com as mudanças de estado do sensor (saída digital),  possui um debounce do sensor e 
		 realiza também medição da saída analógica do sensor.
         Referência: https://blog.eletrogate.com/sistema-anti-incendia-sensor-de-gases-inflamaveis-com-arduino/
@date 2023-03-17
"""

# Importa as classes Pin, ADC e Timer da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, ADC, Timer
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define o pino do Raspberry Pi Pico conectado à saída digital do sensor de gases inflamáveis MQ-2
gas_digital_pin = 15

# Define o pino do Raspberry Pi Pico conectado à saída analógica do sensor de gases inflamáveis MQ-2
gas_analog_pin = 26

# Tempo de debounce para o sensor em ms
debounce_time_ms = 10

# Variável global para armazenar o estado atual do sensor
gas_state = 0
# Variável global para armazenar o estado anterior do sensor
gas_last_state = 0

# Habilita o uso de interrupção para o sensor
enable_irq = True

# Configura o pino da saída digital do sensor
gas_digital = Pin(gas_digital_pin, Pin.IN)

# Instancia o objeto ADC para leitura da saída analógica do sensor
gas_analog = ADC(Pin(gas_analog_pin))

# Instancia um objeto Timer para criar um temporizador para leitura da saída analógica do sensor
timer = Timer()

# Função temporizada para leitura da saída analógica do sensor
def gas_analog_read(timer):
    # Lê o valor da entrada analógica do sensor como um valor positivo de 16 bits
    gas_analog_value = gas_analog.read_u16()
    # Converte o valor analógica na forma de um valor positivo de 16 bits para tensão (valor de um bit = 3.3/(2^16 - 1) = 3.3/65535)
    gas_voltage = gas_analog_value / 65535 * 3.3

    # Imprime o valor da tensão lida
    print("Tensão lida: {:.2f} V".format(gas_voltage))
    
# Configurando o Timer para chamar a função gas_analog_read em intervalos de tempo fixos (1Hz = 1s)
timer.init(freq=1, mode=Timer.PERIODIC, callback=gas_analog_read)

# Verifica se a interrupção está habilitada
if enable_irq:
    # Função de callback para a interrupção do sensor
    def gas_callback(pin):
        # Atualiza a variável global gas_state com o valor do pino
        global gas_state
        gas_state = pin.value()

    # Adiciona a interrupção para detectar a mudança no estado da saída digital do sensor (borda de subida e descida)
    gas_digital.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=gas_callback)
    
# Atualiza o estado atual e anterior da saída digital do sensor
gas_state = gas_digital.value()
gas_last_state = gas_digital.value()

# Imprime mensagem inicial
print("Coloque o sensor de gases inflamáveis MQ-2 na presença de gases para testá-lo!")

# Verifica o estado inicial do sensor
if gas_state == 1:
    # Imprime que foi detectado gases inflamáveis
    print("Detectado de gases inflamáveis!")
else:
    # Imprime que não foi detectado gases inflamáveis
    print("Não detectado gases inflamáveis!")

# Loop infinito
while True:
    # Verifica se a interrupção está desabilitada
    if not enable_irq:
        # Lê o estado do sensor
        gas_state = gas_digital.value()
        
    # Verifica se o estado do sensor mudou
    if gas_state != gas_last_state:
        # Aguarda um período para fazer o debounce
        utime.sleep_ms(debounce_time_ms)
        # Verifica se a interrupção está desabilitada
        if not enable_irq:
            # Lê o estado do sensor
            gas_state = gas_digital.value()

    # Verifica se ocorreu uma borda de subida no sinal do sensor
    if gas_state == 1 and gas_last_state == 0:
        # Atualiza o estado anterior do sensor
        gas_last_state = 1
        # Imprime que foram detectados gases inflamáveis pelo sensor
        print("Detectado de gases inflamáveis!")

    # Verifica se ocorreu uma borda de descida no sinal do sensor
    elif gas_state == 0 and gas_last_state == 1:
        # Atualiza o estado anterior do sensor
        gas_last_state = 0
        # Imprime que não foram detectados gases inflamáveis pelo sensor
        print("Não detectado gases inflamáveis!")
