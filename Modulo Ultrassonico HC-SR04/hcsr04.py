"""!
@file hcsr04.py
@brief Biblioteca para controlar o módulo ultrassônico HC-SR04 com Raspberry Pi Pico e MicroPython
@details Essa biblioteca fornece uma classe simples para medir distâncias usando o sensor ultrassônico 
         HC-SR04 e um Raspberry Pi Pico rodando MicroPython.
         Referência: https://randomnerdtutorials.com/micropython-hc-sr04-ultrasonic-esp32-esp8266/
@author Rodrigo França
@date 2023-03-17
"""

# Importa a classe Pin da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

## @brief Classe para controlar o módulo ultrassônico HC-SR04
class HCSR04:
    ## @brief Construtor da classe HCSR04
    #  @param trigger_pin Número do pino do Raspberry Pi Pico conectado ao pino TRIG do HC-SR04
    #  @param echo_pin Número do pino do Raspberry Pi Pico conectado ao pino ECHO do HC-SR04
    # @param timeout_us Tempo limite (em milissegundos) para aguardar a resposta do HC-SR04 (opcional, valor padrão: 20 ms)
    def __init__(self, trigger_pin, echo_pin, timeout_ms=20):
        
        ## Pino de trigger configurado como saída
        self.trigger = Pin(trigger_pin, Pin.OUT)
        ## Pino de echo configurado como entrada
        self.echo = Pin(echo_pin, Pin.IN)
        ## Tempo limite para aguardar a resposta do HC-SR04 (em milissegundos)
        self.timeout_ms = timeout_ms

    ## @brief Método para obter o tempo de trânsito do sinal ultrassônico gerado pelo sensor HC-SR04
    #  @return Tempo de trânsito do sinal ultrassônico em us
    def get_echo_time(self):
        
        # Garante que o pino de trigger está em nível baixo
        self.trigger.low()
        utime.sleep_us(2)

        # Envia um pulso de 10 microssegundos no pino de trigger
        self.trigger.high()
        utime.sleep_us(10)
        self.trigger.low()
        
        # Marca o tempo atual em milissegundos
        start_time_timeout_ms = utime.ticks_ms()
        
        # Aguarda o pino de echo mudar para nível alto
        while self.echo.value() == 0 and utime.ticks_diff(utime.ticks_ms(), start_time_timeout_ms) < self.timeout_ms:
            pass

        # Marca o tempo em que o pino de echo mudou para nível alto
        start_time_us = utime.ticks_us()

        # Aguarda o pino de echo mudar para nível baixo
        while self.echo.value() == 1 and utime.ticks_diff(utime.ticks_ms(), start_time_timeout_ms) < self.timeout_ms:
            pass
        
        # Verifica se o tempo limite da medição foi excedido
        if utime.ticks_diff(utime.ticks_ms(), start_time_timeout_ms) >= self.timeout_ms:
            # Retorna um valor inválido
            return 0

        # Marca o tempo em que o pino de echo mudou para nível baixo
        end_time_us = utime.ticks_us()

        # Calcula o tempo de trânsito do sinal ultrassônico
        elapsed_time_us = utime.ticks_diff(end_time_us, start_time_us)

        return elapsed_time_us
    
    ## @brief Método para obter a distância medida pelo sensor HC-SR04 em cm
    #  @return Distância em cm
    def get_distance_cm(self):
        
        # O sensor de ultrasom envia um sinal ultrasonico e detecta o sua reflexão. 
        # Por conta disso, o objeto está a metade da distancia total que o som viajou.
        # Para calcular a distância em cm:
        # (distancia) [cm] = (tempo até a reflexão ser detectada) [us] * (velocidade do som) [cm/µs] / 2
        # velocidade do som = 343 m/s = 34300 cm/s = 0.0343 cm/µs
        
        echo_time_us = self.get_echo_time();
        
        # Converte o tempo de trânsito em distância e retorna o valor
        distance_cm = echo_time_us * 0.0343 / 2
        return distance_cm

    ## @brief Método para obter a distância medida pelo sensor HC-SR04 em mm
    #  @return Distância em mm
    def get_distance_mm(self):
        
        # O sensor de ultrasom envia um sinal ultrasonico e detecta o sua reflexão. 
        # Por conta disso, o objeto está a metade da distancia total que o som viajou.
        # Para calcular a distância em mm:
        # (distancia) [mm] = (tempo até a reflexão ser detectada) [us] * (velocidade do som) [mm/µs] / 2
        # velocidade do som = 343 m/s = 3430000 mm/s = 3.43 cm/µs
        
        echo_time_us = self.get_echo_time();
        
        # Converte o tempo de trânsito em distância e retorna o valor
        distance_mm = echo_time_us * 3.43 / 2
        return distance_mm
