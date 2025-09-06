
from TM1638 import TM1638
import machine
import time
import urandom

STB = machine.Pin(15)
CLK = machine.Pin(2)
DIO = machine.Pin(4)

tm = TM1638(stb=STB, clk=CLK, dio=DIO)

def juego():
    aciertos = 0
    errores = 0
    tiempos = []
    rondas = 10
    ronda_actual = 0

    while ronda_actual < rondas:
        boton_led = urandom.getrandbits(3)
        tm.leds(1 << boton_led)
        tm.number(boton_led + 1)
        inicio = time.ticks_ms()
        respondido = False
        while not respondido:
            keys = tm.keys()
            if keys:
                fin = time.ticks_ms()
                tiempo_respuesta = time.ticks_diff(fin, inicio)
                if keys & (1 << boton_led):
                    aciertos += 1
                else:
                    errores += 1
                tiempos.append(tiempo_respuesta)
                tm.leds(0)
                tm.number(0)
                respondido = True
            time.sleep(0.05)
        ronda_actual += 1
        time.sleep(0.5)

    # Visualización dinámica de resultados con scroll
    texto_score = f"SCORE {aciertos}   "
    texto_error = f"ERROR {errores}   "
    promedio = sum(tiempos) // len(tiempos) if tiempos else 0
    texto_tiempo = f"TIEMPO {promedio}ms   "

    for _ in range(3):
        tm.scroll(texto_score, delay=200)
        tm.scroll(texto_error, delay=200)
        tm.scroll(texto_tiempo, delay=200)
    tm.number(0)

while True:
    juego()
    tm.show("RESTART")
    while True:
        keys = tm.keys()
        if keys & 0x80:  # Último botón (botón 8)
            break
        time.sleep(0.1)
    tm.number(0)