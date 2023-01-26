import bluetooth
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
import protocol

port = 1

# globals
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_sock = None
state = protocol.State()


def print_add(joy):
  print('Added', joy)


def print_remove(joy):
  print('Removed', joy)


def key_received(key: Key):
  if client_sock == None:
    return

  if key.keytype == Key.KeyTypes.BUTTON:
    # print(key)
    if key.number == 0:
      state.button_A = key.value
    elif key.number == 1:
      state.button_B = key.value
    elif key.number == 2:
      state.button_X = key.value
    elif key.number == 3:
      state.button_Y = key.value
    elif key.number == 4:
      state.button_L_SHOULDER = key.value
    elif key.number == 5:
      state.button_R_SHOULDER = key.value
    elif key.number == 6:
      state.button_BACK = key.value
    elif key.number == 7:
      state.button_START = key.value
    # elif key.number == 8: # no this button on steam deck
    #   pass
    elif key.number == 9:
      state.button_L_THUMB = key.value
    elif key.number == 10:
      state.button_R_THUMB = key.value
  elif key.keytype == Key.KeyTypes.AXIS:
    if key.number == 0:
      state.left_joystick_x = int(
          (key.value + 1) / 2 * 65535)  # [-1, 1] => [0, 65535]
    elif key.number == 1:
      state.left_joystick_y = int(
          (-key.value + 1) / 2 * 65535)  # reverse axis-Y value
    elif key.number == 2:
      state.left_trigger = int(key.value * 255)  # [0, 1] => [0, 255]
    elif key.number == 3:
      state.right_joystick_x = int(
          (key.value + 1) / 2 * 65535)  # [-1, 1] => [0, 65535]
    elif key.number == 4:
      state.right_joystick_y = int(
          (-key.value + 1) / 2 * 65535)  # reverse axis-Y value
    elif key.number == 5:
      state.right_trigger = int(key.value * 255)  # [0, 1] => [0, 255]
  elif key.keytype == Key.KeyTypes.HAT:
    state.button_DPAD = key.value
  client_sock.send(state.encode())


# listen
server_sock.bind(("", port))
server_sock.listen(1)
print(f'listening at {bluetooth.read_local_bdaddr()[0]} with port {port}')

# get client
client_sock, address = server_sock.accept()
print("Accepted connection from ", address)

# currently set_packet_timeout is not working
# https://github.com/pybluez/pybluez/issues/465
# bluetooth.set_packet_timeout(
#     address[0],
#     17)  # drop packets if they are older than 17 ms to ensure 60 fps

# main loop
run_event_loop(print_add, print_remove, key_received)

client_sock.close()
server_sock.close()
