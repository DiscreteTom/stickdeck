# actions, one byte
idle = 0
press_button = 1
release_button = 2
left_trigger = 3
right_trigger = 4
left_joystick_x = 5
left_joystick_y = 6
right_joystick_x = 7
right_joystick_y = 8
left_trigger = 9
right_trigger = 10


def encode(action: int, value=0) -> bytes:
  '''
  action: 1 byte
  value_: 2 byte
  '''
  return bytes([action, value // 256, value % 256])


def decode(data: bytes) -> (int, int):
  '''
  data: 3 byte
  '''
  return data[0], data[1] * 256 + data[2]