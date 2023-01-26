import bluetooth
import vgamepad
import protocol
import sys

if len(sys.argv) < 2:
  print('Usage: python3 win.py <mac> [port=1]')
  exit(1)

address = sys.argv[1]

if len(sys.argv) == 3:
  port = int(sys.argv[2])
else:
  port = 1

gamepad = vgamepad.VX360Gamepad()
sock = bluetooth.BluetoothSocket(
    bluetooth.RFCOMM)  # windows only support RFCOMM

retry = 3
while retry > 0:
  try:
    sock.connect((address, port))
    break
  except Exception as e:
    retry -= 1
    if retry == 0:
      raise e
    print('retry')

print('connected')

# state cache
left_joystick_value = [0, 0]
right_joystick_value = [0, 0]

while True:
  data = sock.recv(3)
  action, value = protocol.decode(data)

  # print(action, value)

  if action == protocol.idle:
    pass
  # button
  elif action == protocol.press_button:
    gamepad.press_button(value)
  elif action == protocol.release_button:
    gamepad.release_button(value)
  elif action == protocol.left_trigger:
    gamepad.left_trigger(value)
  elif action == protocol.right_trigger:
    gamepad.right_trigger(value)
  # joystick
  elif action == protocol.left_joystick_x:
    left_joystick_value[0] = value - 32768  # [0, 65535] => [-32768, 32767]
    gamepad.left_joystick(*left_joystick_value)
  elif action == protocol.left_joystick_y:
    left_joystick_value[1] = value - 32768
    gamepad.left_joystick(*left_joystick_value)
  elif action == protocol.right_joystick_x:
    right_joystick_value[0] = value - 32768
    gamepad.right_joystick(*right_joystick_value)
  elif action == protocol.right_joystick_y:
    right_joystick_value[1] = value - 32768
    gamepad.right_joystick(*right_joystick_value)

  gamepad.update()