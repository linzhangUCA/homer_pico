# homer_pico

MicroPython scripts on Raspberry Pi Pico (2) for HomeR's motion control.

## Usage
0. Install dependencies and grant user permission to access Pico
  ```console
  sudo apt install python3-pip
  pip install rshell
  sudo usermod -aG dialout $USER
  ```

  > [!TIP]
  > Reboot computer to gain access.

1. Download and dive into the repository.

  ```console
  cd ~  # use $HOME as an example
  git clone https://github.com/linzhanguca/homer_pico.git
  cd homer_pico
  ```

2. Upload motion and perception controller 

  ```console
  rshell -p /dev/ttyACM0 --buffer-size 512 cp -r upython_scripts/drivetrain /pyboard/
  rshell -p /dev/ttyACM0 --buffer-size 512 cp -r upython_scripts/perception /pyboard/
  ```

3. Set up automatic communication using [`pico_messenger.py`](./upython_scripts/pico_messenger.py).

  ```console
  rshell -p /dev/ttyACM0 --buffer-size 512 cp upython_scripts/pico_messenger.py /pyboard/main.py
  ```

  > [!TIP]
  > A hard reset (unplug Pico then plug it back) is required to activate `main.py`.

> [!NOTE]
> If you are completely new to Pico or MicroPython, please follow the official [guide](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/) to get started.

## Test

Run [`computer_messenger.py`](/tests/computer_messenger.py) on a desktop/laptop/SBC to test USB communication.

```console
cd ~/homer_pico/
python3 tests/computer_messenger.py
```
