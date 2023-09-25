import time
import board
import touchio

touch_pad = board.A1  # Will not work for Circuit Playground Express!
# touch_pad = board.A1  # For Circuit Playground Express

touch = touchio.TouchIn(touch_pad)

print("hallo")
a = 0

while True:
    if touch.value:
        a+=1
        print(f"Touched! {a}")
    time.sleep(0.05)

