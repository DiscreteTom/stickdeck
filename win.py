import bluetooth
import vgamepad
import protocol
import sys
import threading
import time

# parse command line arguments
if len(sys.argv) < 2:
  print('Usage: python3 win.py <mac> [port=1]')
  exit(1)
address = sys.argv[1]
if len(sys.argv) == 3:
  port = int(sys.argv[2])
else:
  port = 1

# globals
gamepad = vgamepad.VX360Gamepad()
sock = bluetooth.BluetoothSocket(
    bluetooth.RFCOMM)  # windows only support RFCOMM
state = protocol.State()  # state cache
protocol_len = len(state.encode())  # protocol byte length
# smallest power of 2 larger than protocol_len
recv_len = 2**((protocol_len - 1).bit_length())
buffer = bytes()

# connect & retry
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


# util function
def apply_btn(btn: int, value: int):
  if value == 0:
    gamepad.release_button(btn)
  else:
    gamepad.press_button(btn)


def run():
  global state
  global buffer

  while True:
    # recv more if buffer is not enough
    while len(buffer) < protocol_len:
      try:
        # we will call sock.close() on ctrl-c, so we need to handle the exception
        data = sock.recv(recv_len)
      except:
        sys.exit(0)
      if not data:
        sys.exit(0)  # gracefully exit thread when deck is down
      buffer += data

    new_state = state.decode(buffer[:protocol_len])
    buffer = buffer[protocol_len:]

    # joysticks
    if new_state.left_joystick_x != state.left_joystick_x or new_state.left_joystick_y != state.left_joystick_y:
      gamepad.left_joystick(
          new_state.left_joystick_x - 32768,  # [0, 65535] => [-32768, 32767]
          new_state.left_joystick_y - 32768)
    if new_state.right_joystick_x != state.right_joystick_x or new_state.right_joystick_y != state.right_joystick_y:
      gamepad.right_joystick(
          new_state.right_joystick_x - 32768,  # [0, 65535] => [-32768, 32767]
          new_state.right_joystick_y - 32768)

    # triggers
    if new_state.left_trigger != state.left_trigger:
      gamepad.left_trigger(new_state.left_trigger)
    if new_state.right_trigger != state.right_trigger:
      gamepad.right_trigger(new_state.right_trigger)

    # buttons
    if new_state.button_A != state.button_A:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_A, new_state.button_A)
    if new_state.button_B != state.button_B:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_B, new_state.button_B)
    if new_state.button_X != state.button_X:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_X, new_state.button_X)
    if new_state.button_Y != state.button_Y:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_Y, new_state.button_Y)
    if new_state.button_L_SHOULDER != state.button_L_SHOULDER:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
                new_state.button_L_SHOULDER)
    if new_state.button_R_SHOULDER != state.button_R_SHOULDER:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
                new_state.button_R_SHOULDER)
    if new_state.button_BACK != state.button_BACK:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_BACK, new_state.button_BACK)
    if new_state.button_START != state.button_START:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_START,
                new_state.button_START)
    if new_state.button_L_THUMB != state.button_L_THUMB:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
                new_state.button_L_THUMB)
    if new_state.button_R_THUMB != state.button_R_THUMB:
      apply_btn(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
                new_state.button_R_THUMB)

    # dpad
    if new_state.button_DPAD != state.button_DPAD:
      if new_state.button_DPAD & 0x01 == 0 and state.button_DPAD & 0x01 != 0:
        gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
      if new_state.button_DPAD & 0x01 != 0 and state.button_DPAD & 0x01 == 0:
        gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
      if new_state.button_DPAD & 0x02 == 0 and state.button_DPAD & 0x02 != 0:
        gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
      if new_state.button_DPAD & 0x02 != 0 and state.button_DPAD & 0x02 == 0:
        gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
      if new_state.button_DPAD & 0x04 == 0 and state.button_DPAD & 0x04 != 0:
        gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
      if new_state.button_DPAD & 0x04 != 0 and state.button_DPAD & 0x04 == 0:
        gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
      if new_state.button_DPAD & 0x08 == 0 and state.button_DPAD & 0x08 != 0:
        gamepad.release_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
      if new_state.button_DPAD & 0x08 != 0 and state.button_DPAD & 0x08 == 0:
        gamepad.press_button(vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)

    gamepad.update()
    state = new_state


# spawn a thread to run the receiver and control the gamepad
run_thread = threading.Thread(target=run)
run_thread.start()

# make the main thread sleep forever to recv ctrl-c
try:
  while True:
    time.sleep(1)
    # check if the thread is still running
    if not run_thread.is_alive():
      break
except KeyboardInterrupt:
  sock.close()
  sys.exit(0)