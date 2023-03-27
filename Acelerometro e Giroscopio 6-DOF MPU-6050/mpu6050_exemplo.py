"""!
@file mpu6050_exemplo.py
@brief Programa para ler o IMU MPU6050 usando o  e Raspberry Pi Pico.
@details Este programa utiliza a biblioteca upy_adafruit_mpu6050 para ler os valores do IMU MPU6050 via barramento I2C.
         A aceleração (X, Y e Z), rotação (X, Y e Z) e temperatura são exibidas no console a cada segundo.
         Referência: https://learn.adafruit.com/mpu6050-6-dof-accelerometer-and-gyro/python-and-circuitpython
@author Rodrigo França
@date 2023-03-28
"""

# Importa as classes Pin e I2C da biblioteca machine para controlar o hardware do Raspberry Pi Pico
from machine import Pin, I2C
# Importa a classe MPU6050 da biblioteca upy_adafruit_mpu6050.py
from upy_adafruit_mpu6050 import MPU6050
# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime

# Define os pinos do Raspberry Pi Pico conectados ao barramento I2C 0
i2c0_slc_pin = 9
i2c0_sda_pin = 8

# Inicializa o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
i2c0 = I2C(0, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=100000)

# Inicializa o IMU MPU6050
mpu6050 = MPU6050(i2c0)

# Loop infinito
while True:
    
    # Lê a aceleração (X, Y e Z), rotação (X, Y e Z) e temperatura do IMU
    (mpu6050_accel_x, mpu6050_accel_y, mpu6050_accel_z) = mpu6050.acceleration
    (mpu6050_gyro_x, mpu6050_gyro_y, mpu6050_gyro_z) = mpu6050.gyro
    mpu6050_temp = mpu6050.temperature
    
    # Exibe os valores lidos no console
    print("Aceleração X: {:.2f}, Y: {:.2f}, Z: {:.2f} m/s^2".format(mpu6050_accel_x, mpu6050_accel_y, mpu6050_accel_z))
    print("Rotação X: {:.2f}, Y: {:.2f}, Z: {:.2f} rad/s".format(mpu6050_gyro_x, mpu6050_gyro_y, mpu6050_gyro_z))
    print("Temperatura: {:.2f} C".format(mpu6050_temp))
    
    # Aguarda 1 segundo antes de ler novamente
    utime.sleep(1)
