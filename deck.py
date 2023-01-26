import bluetooth
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
import protocol
import xusb_button

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
client_sock = None


def encode_button(name: int, value: int) -> bytes:
  if value == 1:
    return protocol.encode(protocol.press_button, name)
  else:
    return protocol.encode(protocol.release_button, name)


def print_add(joy):
  print('Added', joy)


def print_remove(joy):
  print('Removed', joy)


def key_received(key: Key):
  if client_sock == None:
    return

  idle = False
  if key.keytype == Key.KeyTypes.BUTTON:
    # print(key)
    if key.number == 0:
      data = encode_button(xusb_button.XUSB_GAMEPAD_A, key.value)
    elif key.number == 1:
      data = encode_button(xusb_button.XUSB_GAMEPAD_B, key.value)
    elif key.number == 2:
      data = encode_button(xusb_button.XUSB_GAMEPAD_X, key.value)
    elif key.number == 3:
      data = encode_button(xusb_button.XUSB_GAMEPAD_Y, key.value)
    elif key.number == 4:
      data = encode_button(xusb_button.XUSB_GAMEPAD_LEFT_SHOULDER, key.value)
    elif key.number == 5:
      data = encode_button(xusb_button.XUSB_GAMEPAD_RIGHT_SHOULDER, key.value)
    elif key.number == 6:
      data = encode_button(xusb_button.XUSB_GAMEPAD_BACK, key.value)
    elif key.number == 7:
      data = encode_button(xusb_button.XUSB_GAMEPAD_START, key.value)
    # elif key.number == 8: # no this button on steam deck
    #   data = encode_button(xusb_button.XUSB_GAMEPAD_GUIDE, key.value)
    elif key.number == 9:
      data = encode_button(xusb_button.XUSB_GAMEPAD_LEFT_THUMB, key.value)
    elif key.number == 10:
      data = encode_button(xusb_button.XUSB_GAMEPAD_RIGHT_THUMB, key.value)
    else:
      idle = True
      # data = protocol.encode(protocol.idle)
  elif key.keytype == Key.KeyTypes.AXIS:
    # print(key.value)
    if key.number == 0:
      data = protocol.encode(protocol.left_joystick_x,
                             int((key.value + 1) / 2 *
                                 65535))  # [-1, 1] => [0, 65535]
    elif key.number == 1:
      data = protocol.encode(protocol.left_joystick_y,
                             int((-key.value + 1) / 2 *
                                 65535))  # reverse axis-Y value
    elif key.number == 2:
      data = protocol.encode(protocol.left_trigger,
                             int(key.value * 255))  # [0, 1] => [0, 255]
    elif key.number == 3:
      data = protocol.encode(protocol.right_joystick_x,
                             int((key.value + 1) / 2 * 65535))
    elif key.number == 4:
      data = protocol.encode(protocol.right_joystick_y,
                             int((-key.value + 1) / 2 * 65535))
    elif key.number == 5:
      data = protocol.encode(protocol.right_trigger, int(key.value * 255))
  else:
    idle = True
    # data = protocol.encode(protocol.idle)
  if not idle:
    # print(data)
    client_sock.send(data)


server_sock.bind(("", port))
server_sock.listen(1)

print('listening')

client_sock, address = server_sock.accept()
print("Accepted connection from ", address)

run_event_loop(print_add, print_remove, key_received)

client_sock.close()
server_sock.close()
