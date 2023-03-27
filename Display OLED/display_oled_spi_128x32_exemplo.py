"""!
@file display_oled_spi_128x32_exemplo.py
@brief Programa para escrever em um display OLED SPI de 128x32 usando o Raspberry Pi Pico e MicroPython.
@details Este programa utiliza a biblioteca ssd1306 para escrever em um display OLED de 128x32 via comunicação SPI.
         Referência: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
@author Rodrigo França
@date 2023-03-17
"""

# Importa as classes Pin e SPI da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, SPI
# Importa a classe SSD1306_SPI da biblioteca ssd1306.py
from ssd1306 import SSD1306_SPI

# Define os pinos do Raspberry Pi Pico conectados ao barramento SPI 0
spi0_sck_pin = 2
spi0_mosi_pin = 3
spi0_miso_pin = 4

# Define os pinos do Raspberry Pi Pico conectados ao display OLED SPI
display_dc = 0  # Data/command
display_rst = 1 # Reset
display_cs = 5  # Chip select, alguns modulos não tem esse pino

# Inicializa o SPI0 com os pinos GPIO2 (SCK), GPIO3 (MOSI) e GPIO4 (MISO)
spi0 = SPI(0, baudrate=1000000, polarity=1, phase=0, sck=Pin(spi0_sck_pin), mosi=Pin(spi0_mosi_pin), miso=Pin(spi0_miso_pin))

# Inicializa o display OLED SPI de 128x32
display = SSD1306_SPI(128, 32, spi0, Pin(display_dc), Pin(display_rst), Pin(display_cs))

# Limpa o display
display.fill(0)
display.show()

# Desenha o logo do MicroPython e imprime um texto
display.fill(0)                        # preenche toda a tela com cor = 0
display.fill_rect(0, 0, 32, 32, 1)     # desenha um retângulo sólido de 0,0 a 32,32, cor = 1
display.fill_rect(2, 2, 28, 28, 0)     # desenha um retângulo sólido de 2,2 a 28,28, cor = 0
display.vline(9, 8, 22, 1)             # desenha uma linha vertical x = 9 , y = 8, altura = 22, cor = 1
display.vline(16, 2, 22, 1)            # desenha uma linha vertical x = 16, y = 2, altura = 22, cor = 1
display.vline(23, 8, 22, 1)            # desenha uma linha vertical x = 23, y = 8, altura = 22, cor = 1
display.fill_rect(26, 24, 2, 4, 1)     # desenha um retângulo sólido de 26,24 a 2,4, cor = 1
display.text('MicroPython', 40, 0, 1)  # desenha algum texto em x = 40, y = 0 , cor = 1
display.text('SSD1306', 40, 12, 1)     # desenha algum texto em x = 40, y = 12, cor = 1
display.text('OLED 128x64', 40, 24, 1) # desenha algum texto em x = 40, y = 24, cor = 1
display.show()                         # escreve o conteúdo do FrameBuffer na memória do display

# Atualiza o display
display.show()

