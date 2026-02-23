# homer_pico

MicroPython scripts on Raspberry Pi Pico (2) for HomeR's motion control.

## Usage

1. Download and navigate to the repository.

    ```console
    cd ~  # use $HOME as an example
    git clone https://github.com/linzhanguca/homer_pico.git
    cd homer_pico
    ```

2. Upload differential drive controller

    ```console
    rshell -p /dev/ttyACM0 --buffer-size 512 cp -r upython_scripts/drivetrain /pyboard/
    ```

3. Set up automatic communication using [`pico_messenger.py`](./upython_scripts/pico_messenger.py).

    ```console
    rshell -p /dev/ttyACM0 --buffer-size 512 cp upython_scripts/pico_messenger.py /pyboard/main.py
    ```

> [!NOTE]
> If you are completely new to Pico or MicroPython, please follow the official [guide](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/) to get familiar.
