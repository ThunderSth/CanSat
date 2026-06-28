import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.D25)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

print(switch.value)

storage.remount("/", readonly=switch.value)