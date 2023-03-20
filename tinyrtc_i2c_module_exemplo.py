"""!
@file tinyrtc_i2c_module_exemplo.py
@brief Exemplo de aplicação usando o módulo I2C Tiny RTC com um Raspberry Pi Pico
@details Este script demonstra como utilizar as bibliotecas ds1307.py e at24c32n.py para controlar o RTC e a EEPROM do módulo I2C Tiny RTC em um Raspberry Pi Pico rodando MicroPython.
         Referência: https://github.com/mcauser/micropython-tinyrtc-i2c
@author Rodrigo França
@date 2023-03-17
"""

# Importa a biblioteca machine para controlar o hardware do Raspberry Pi Pico
import machine
# Importa a biblioteca time para usar funções relacionadas ao tempo
import time

# Importa a biblioteca ds1307.py para controlar o RTC do módulo I2C Tiny RTC
import ds1307
# Importa a biblioteca at24c32n.py para controlar a EEPROM do módulo I2C Tiny RTC
import at24c32n

# Configura o barramento I2C
# Utiliza o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=100000)
# Utiliza o I2C1 com os pinos GPIO7 (SCL) e GPIO6 (SDA)
#i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6), freq=100000)

# Inicializa o RTC DS1307
ds = ds1307.DS1307(i2c)
# Inicializa a EEPROM AT24C32N
eeprom = at24c32n.AT24C32N(i2c)

# Habilita o oscilador do RTC
ds.halt(False)

# Opções do menu principal
options = (
    ('0', 'Imprime novamente as opções'),
    ('1', 'Imprime o horário atual do RTC'),
    ('2', 'Atualiza o horário interno do RTC com a hora do sistema'),
    ('3', 'Lê o conteúdo da EEPROM (11 bytes a partir do endereço 0)'),
    ('4', 'Escreve Hello World para a EEPROM (a partir do endereço 0)'),
    ('5', 'Limpa o conteúdo da EEPROM (11 bytes a partir do endereço 0')
)

# Imprime as opções do menu
for option in options:
    print("{}: {}".format(option[0], option[1]))

# Loop infinito
while True:

    # Lê o caractere digitado pelo console
    print()
    input_char = input('Selecione uma opção: ')
    print()
    
    # Verifica qual foi o caractere recebido e executa a ação apropriada
    
    #0: Imprime novamente as opções
    if input_char == '0':
        
        # Imprime as opções do menu
        for option in options:
            print("{}: {}".format(option[0], option[1]))
        
    #1: Imprime o horário atual do RTC
    elif input_char == '1':

        # Obtém a data e hora atual do RTC
        current_time_rtc = ds.datetime()

        # Imprime a data e hora atual formatada do RTC
        print("Data e hora atual do RTC: {:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(
            current_time_rtc[2], current_time_rtc[1], current_time_rtc[0],
            current_time_rtc[4], current_time_rtc[5], current_time_rtc[6]))
        
    #2: Atualiza o horário interno do RTC com a hora do sistema
    elif input_char == '2':

        # Formato do datetime do sistema: (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday)
        # Formato do datetime do RTC DS1307: (year, month, day, weekday, hour, minute, second)

        # Obtém a data e hora atual do sistema
        current_time_system = time.localtime()
        
        # Imprime a data e hora atual formatada do sistema
        print("Data e hora atual: {:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(
            current_time_system[2], current_time_system[1], current_time_system[0],
            current_time_system[3], current_time_system[4], current_time_system[5]))
        
        # Converte a data e hora atual para o formato do RTC
        new_time_rtc = (current_time[0], current_time[1], current_time[2], current_time[6], current_time[3], current_time[4], current_time[5])
        
        # Define a data e hora atual do RTC
        ds.datetime(new_time_rtc)
       
    #3: Lê o conteúdo da EEPROM (11 bytes a partir do endereço 0)   
    elif input_char == '3':
        
        # Lê 11 bytes da memória EEPROM a partir do endereço 0
        print(eeprom.read(0, 11))
        
    #4: Escreve Hello World para a EEPROM (a partir do endereço 0)
    elif input_char == '4':
        
        # Escreve "hello world" na memória EEPROM a partir do endereço 0
        eeprom.write(0, 'hello world')
        
    #5: Limpa o conteúdo da EEPROM (11 bytes a partir do endereço 0)
    elif input_char == '5':
        
        # Escreve 0xFF em 11 bytes da memória EEPROM a partir do endereço 0
        eeprom.write(0, b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
        
    # Caractere digitado não está associado a nenhuma opção
    else:
        print('Opção inválida')
