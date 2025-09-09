# Vúmetro con TM1638 y ESP32: botón incrementa nivel, LEDs y display sincronizados

import machine
import time
from TM1638 import TM1638

STB = machine.Pin(15)
CLK = machine.Pin(2)
DIO = machine.Pin(4)

tm = TM1638(stb=STB, clk=CLK, dio=DIO)

nivel = 0
MAX_NIVEL = 9

while True:
    keys = tm.keys()
    if keys & 0x01:  # Botón 1: subir nivel
        nivel += 1
        if nivel > MAX_NIVEL:
            nivel = 0
        while tm.keys() & 0x01:
            time.sleep(0.05)
    if keys & 0x02:  # Botón 2: bajar nivel
        nivel -= 1
        if nivel < 0:
            nivel = MAX_NIVEL
        while tm.keys() & 0x02:
            time.sleep(0.05)

    if nivel == MAX_NIVEL:
        # Parpadeo de LEDs en nivel 9 y luego reinicia a 0
        for _ in range(5):
            tm.leds(0xFF)
            tm.show(f"Nivel {nivel}")
            time.sleep(0.2)
            tm.leds(0x00)
            tm.show(f"Nivel {nivel}")
            time.sleep(0.2)
        nivel = 0  # Reinicia después del parpadeo
        tm.leds(0)
        tm.show(f"Nivel {nivel}")
    else:
        tm.leds((1 << nivel) - 1)
        tm.show(f"Nivel {nivel}")

    time.sleep(0.05)