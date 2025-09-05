# Contador en TM1638 
from TM1638 import TM1638
import machine
import time

STB = machine.Pin(15)
CLK = machine.Pin(2)
DIO = machine.Pin(4)

tm = TM1638(stb=STB, clk=CLK, dio=DIO)

contador = 0
direccion = 1
MAX_NUM = 99999999

while True:
    tm.number(contador)
    time.sleep(0.2)
    keys = tm.keys()
    if keys & 0x01:         # Si el primer botón está presionado, resetea
        contador = 0
    elif keys:
        direccion *= -1     # Cualquier otro botón cambia dirección
    contador += direccion
    if contador < 0:
        contador = MAX_NUM
    elif contador > MAX_NUM:

        contador = 0
