"""!
@file display_oled_i2c_exemplo.py
@brief Programa para escrever em um display OLED I2C de 128x64 usando o Raspberry Pi Pico e MicroPython.
@details Este programa utiliza a biblioteca ssd1306 para escrever em um display OLED de 128x64 via barramento I2C.
         Referência: https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html
@author Rodrigo França
@date 17/03/2023
"""

import machine
import ssd1306

# Inicializa o display OLED I2C
# Utiliza o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=100000)
# Utiliza o I2C1 com os pinos GPIO7 (SCL) e GPIO6 (SDA)
#i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6), freq=100000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

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

# Escreve na última linha do display
display.text("Hello World!", 16, 54)

# Atualiza o display
display.show()

