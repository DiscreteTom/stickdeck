class State:

  def __init__(self):
    self.left_joystick_x = 0  # [-32768, 32767], 2 bytes
    self.left_joystick_y = 0
    self.left_trigger = 0  # [0, 255], 1 byte
    self.right_joystick_x = 0
    self.right_joystick_y = 0
    self.right_trigger = 0
    self.button_A = 0  # 0 or 1
    self.button_B = 0
    self.button_X = 0
    self.button_Y = 0
    self.button_L_SHOULDER = 0
    self.button_R_SHOULDER = 0
    self.button_L_THUMB = 0
    self.button_R_THUMB = 0
    self.button_BACK = 0
    self.button_START = 0
    self.button_DPAD = 0  # pyjoystick.HatValues, [0, 12]

  def encode(self) -> bytes:
    return bytes([
        self.left_joystick_x >> 8,
        self.left_joystick_x & 0xff,
        self.left_joystick_y >> 8,
        self.left_joystick_y & 0xff,
        self.left_trigger,
        self.right_joystick_x >> 8,
        self.right_joystick_x & 0xff,
        self.right_joystick_y >> 8,
        self.right_joystick_y & 0xff,
        self.right_trigger,
        self.button_A << 0 | self.button_B << 1 | self.button_X << 2
        | self.button_Y << 3 | self.button_L_SHOULDER << 4
        | self.button_R_SHOULDER << 5 | self.button_L_THUMB << 6
        | self.button_R_THUMB << 7,
        self.button_BACK << 0 | self.button_START << 1,
        self.button_DPAD,
    ])

  def decode(self, data: bytes) -> 'State':
    ret = State()
    ret.left_joystick_x = data[0] << 8 + data[1]
    ret.left_joystick_y = data[2] << 8 + data[3]
    ret.left_trigger = data[4]
    ret.right_joystick_x = data[5] << 8 + data[6]
    ret.right_joystick_y = data[7] << 8 + data[8]
    ret.right_trigger = data[9]
    ret.button_A = data[10] & 0x01
    ret.button_B = data[10] & 0x02
    ret.button_X = data[10] & 0x04
    ret.button_Y = data[10] & 0x08
    ret.button_L_SHOULDER = data[10] & 0x10
    ret.button_R_SHOULDER = data[10] & 0x20
    ret.button_L_THUMB = data[10] & 0x40
    ret.button_R_THUMB = data[10] & 0x80
    ret.button_BACK = data[11] & 0x01
    ret.button_START = data[11] & 0x02
    ret.button_DPAD = data[12]
    return ret