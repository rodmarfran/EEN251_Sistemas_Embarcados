"""!
@file display_oled_spi_exemplo.py
@brief Programa para escrever em um display OLED SPI de 128x32 usando o Raspberry Pi Pico e MicroPython.
@details Este programa utiliza a biblioteca ssd1306 para escrever em um display OLED de 128x32 via comunicação SPI.
         Referência: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
@author Rodrigo França
@date 17/03/2023
"""

import machine
import ssd1306

# Configuração do display OLED SPI
# Utiliza o SPI0 com os pinos GPIO2 (SCK), GPIO3 (MOSI) e GPIO4 (MISO)
spi = machine.SPI(0, baudrate=1000000, polarity=1, phase=0, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4))
cs = machine.Pin(5)  # Chip select, alguns modulos não tem esse pino
# Utiliza o SPI0 com os pinos GPIO10 (SCK), GPIO11 (MOSI) e GPIO12 (MISO)
#spi = machine.SPI(1, baudrate=1000000, polarity=1, phase=0, sck=machine.Pin(10), mosi=machine.Pin(11), miso=machine.Pin(12))
#cs = machine.Pin(13)  # Chip select, alguns modulos não tem esse pino
dc = machine.Pin(0)  # Data/command
rst = machine.Pin(1) # Reset
display = ssd1306.SSD1306_SPI(128, 32, spi, dc, rst, cs)

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

