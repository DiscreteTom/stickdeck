# Deprecated

See [stickdeck-rs](https://github.com/DiscreteTom/stickdeck-rs) instead.

# Stick Deck

Turn your Steam Deck as a bluetooth joystick(gamepad) on PC.

![demo](img/demo.gif)

> [!NOTE]
> This solution doesn't implement HID (Human Interface Device), so you have to run a receiver program on your PC.

## Prerequisites

For both PC and Steam Deck:

- Python 3.x
- PyBlueZ

> [!WARNING]
> Install PyBlueZ by using its source code, **_DON'T_** just `pip install pybluez`, you should `git clone git@github.com:pybluez/pybluez.git` then `python setup.py install`.

> [!NOTE]
> For PC when installing PyBlueZ, you might need to install Windows C++ SDK. Just follow the tips from the pybluez.

Additional requirements for PC:

- `pip install vgamepad`, this will install a virtual gamepad driver on your PC.

Additional requirements for Steam Deck:

- `pip install pyjoystick`

> [!NOTE]
> During the installations above, you might need to install some additional softwares. Just follow those error messages and install them manually.

## Run the Sender on Steam Deck

First, set your bluetooth visible: Settings - Bluetooth - Configure - Visible

> [!NOTE]
> Or you can use `bluetoothctl` and `discoverable on`.

```bash
python deck.py
```

Then, [switch to Gamepad layout mode from desktop mode with a long press on the right pause button (3 strokes)](https://github.com/ValveSoftware/steam-for-linux/issues/8904).

## Run the Receiver on PC

```bash
python win.py <address> [port=1]
```

> [!NOTE]
> You can debug the joystick by running `joy.cpl` utility on Windows.

## Access from SteamDeck's Desktop

You can create a shell script on the desktop with some contents like:

```bash
#!/bin/bash
konsole -e "/bin/bash -c 'python deck.py'"
```

Then, `chmod +x <script>.sh` makes it executable, then you can start the StickDeck from the desktop!
