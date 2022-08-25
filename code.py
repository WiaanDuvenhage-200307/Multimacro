
import board
import digitalio
import usb_hid
import analogio
import rotaryio
from adafruit_hid.keyboard import Keyboard
import time
from adafruit_hid.keycode import Keycode

kbd = Keyboard(usb_hid.devices)

x_axis = analogio.AnalogIn(board.GP27)
y_axis = analogio.AnalogIn(board.GP26)

tilt = digitalio.DigitalInOut(board.GP0)
tilt.switch_to_input(pull=digitalio.Pull.UP)

rotary = digitalio.DigitalInOut(board.GP15)
rotary.direction = digitalio.Direction.INPUT
rotary.pull = digitalio.Pull.UP

select = digitalio.DigitalInOut(board.GP16)
select.direction = digitalio.Direction.INPUT
select.switch_to_input(pull=digitalio.Pull.UP)


button1 = digitalio.DigitalInOut(board.GP1)
button1.switch_to_input(pull=digitalio.Pull.UP)
button2 = digitalio.DigitalInOut(board.GP2)
button2.switch_to_input(pull=digitalio.Pull.UP)
button3 = digitalio.DigitalInOut(board.GP3)
button3.switch_to_input(pull=digitalio.Pull.UP)

pot_min = 0.00
pot_max = 3.29
step = (pot_max - pot_min) /20.0

def get_value(pots):
    return (pots.value * 3.3) / 65536

def steps(axis):
    return round((axis - pot_min) / step)

# Rotary Encoder
encoder = rotaryio.IncrementalEncoder(board.GP14, board.GP13)
last_position = 0

rSteps = 0

while True:


    # Tilt Sensor Code
    if not tilt.value:
        print("Tilt Activated")
        kbd.press(Keycode.K)
    else:
        kbd.release_all()
    time.sleep(0.1)

    # Rotary Code
    position = encoder.position
    if last_position is None or position != last_position:
        pos = position-last_position
        print(pos)
        if pos > -1:
            kbd.send(Keycode.A)
            rSteps = rSteps + 1
            if rSteps > 9:
                kbd.send(Keycode.D)
                kbd.send(Keycode.S)
                rSteps = 0
                print("a")
        if pos < 1:
            # rSteps = 0
            kbd.send(Keycode.D)
            rSteps = rSteps + 1
            if rSteps > 19:
                kbd.send(Keycode.W)
    last_position = position

    # time.sleep(0.1)

    # Joystick Code
    x = get_value(x_axis)
    y = get_value(y_axis)
    if steps(x) > 16.0:
        kbd.press(Keycode.A)
    else:
        kbd.release(Keycode.A)

    if steps(x) < 9.0:
        kbd.press(Keycode.D)
    else:
        kbd.release(Keycode.D)

    # Combo Code
    # Combo1
    if not button1.value:
        kbd.send(Keycode.D, Keycode.J)
        time.sleep(0.3)
        kbd.send(Keycode.D, Keycode.J)
        time.sleep(0.3)
        kbd.send(Keycode.D, Keycode.J)
        time.sleep(0.3)
    else:
        kbd.release_all()
    # Combo2
    if not button2.value:
        kbd.send(Keycode.S, Keycode.J)
        time.sleep(0.3)
        kbd.send(Keycode.W, Keycode.J)
        time.sleep(0.3)
        kbd.send(Keycode.SPACE)
        time.sleep(0.3)
        kbd.send(Keycode.W, Keycode.K)
        time.sleep(0.3)
        kbd.send(Keycode.J)
    else:
        kbd.release_all()
    # Combo3
    if not button3.value:
        kbd.send(Keycode.W, Keycode.K)
        time.sleep(0.3)
        kbd.send(Keycode.SPACE)
        time.sleep(0.5)
        kbd.send(Keycode.S, Keycode.J)
        time.sleep(0.3)
    else:
        kbd.release_all()
        








