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

# Configuración de antirrebote
DEBOUNCE_MS = 200
last_state = 0
last_time = [0] * 8   # un tiempo por cada botón

while True:
    tm.number(contador)
    time.sleep(0.05)  # refresco rápido

    keys = tm.keys()
    now = time.ticks_ms()

    for i in range(8):  # recorrer cada botón
        mask = 1 << i
        pressed_now = keys & mask
        pressed_before = last_state & mask

        # flanco de subida con antirrebote por botón
        if pressed_now and not pressed_before:
            if time.ticks_diff(now, last_time[i]) > DEBOUNCE_MS:
                # --- acción según botón ---
                if i == 0:
                    contador = 0           # Botón 0 = reset
                else:
                    direccion *= -1        # Otros botones = cambia dirección
                # -------------------------
                last_time[i] = now

    last_state = keys

    # Actualizar contador
    contador += direccion
    if contador < 0:
        contador = MAX_NUM
    elif contador > MAX_NUM:
        contador = 0
