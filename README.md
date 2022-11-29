# ChristmasTree
The chrstmas tree is a piece of electronics art designed to bring the christmas spirit to everybody. This document serves as the technical documentation for anyone wanting to start hacking or simply interested in the technical details.
Fundamentally the hardware consists of an AVR ATtiny804 microcontroller controlling 24 SK6812 RGBW LEDs. There are 14 preprogrammed pictures to choose from. The 15th picture can be programmed by the user through a UART interface. A USB-UART bridge is implemented on-board. The user programmed picture is stored inside the EEPROM memory of the MCU, which makes the picture persistent through power cycles. The single button on the backside of the device cycles through the 15 pictures.
## Power
Power to the device is provided either by the USB port or by the battery integrated into the stand. It is charged by a dedicated IC when power is provided through the USB port. Note that the battery loads even when the device is turned off by the power switch. To prevent the device from drawing any current, the USB port must be disconnected. Also note that the resistor programmed charge current is chosen rather conservatively to prolong the life of the battery. The state of charge is indicated by two LEDs on the backside near the battery connector. The red LED indicates the charge being in progress while the green LED indicates the charge being done. The battery voltage is monitored by the MCU. If it falls under a threshold, the LEDs are turned off until a power source is connected to the USB port. This prevent an undervoltage condition while also further protecting the longevity of the battery.
## Programming
The device is preloaded with our own software, EEPROM and fuses. You can find the binaries in this repository. If you like to write your own software feel free to start hacking. You can always come back to our version. Just note that it is not possible for us to provide support for problems with your own software. Also we are not currently able to maintain our software in an open-source capacity.
A programming interface is provided through the USB-UART controller. To program the MCU flip the switch near the USB port to to UPDI and use `pymcuprog`/`pyupdi` ([src](https://github.com/microchip-pic-avr-tools/pymcuprog)).
We use platformio. Here is a sample environment as a starting point:

    [env:pymcuprog_upload]
    platform = atmelmegaavr
    board = ATtiny804
    board_build.f_cpu = 10000000
    board_fuses.OSCCFG = 0x02 ;20 MHz internal oscillator
    board_fuses.BODCFG = 0x44 ;BOD to 2.6V and enable BOD
    upload_protocol = custom
    upload_port = /dev/ttyUSB0
    upload_speed = 230400
    upload_flags =
        --tool
        uart
        --device
        $BOARD_MCU
        --uart
        $UPLOAD_PORT
        --clk
        $UPLOAD_SPEED
    upload_command = pymcuprog write --erase $UPLOAD_FLAGS --filename $SOURCE

## UART Interface
A UART interface provides additional functionality to the device. The interface runs at a baudrate of 9600. The UART - UPDI switch must be in the UART position for the interface to work. The protocol has the following basic structure:

`cmd [index data]`

The protocol has 5 commands:

| cmd | index | data | description |
| - | - | - | - |
| s | none | none | get status byte |
| t | none | none | toggle LEDs on/off |
| p | picture index | none | set the displayed picture to the one at the provided index |
| c | pixel index | rrrgggbbbwww | set the pixel at pixel index in custom picture to data |
| v | none | none | save current picture to EEPROM |

Between `cmd`, `index` and `data` spaces are allowed but are not necessary.

The status byte is used by the device to save important data to EEPROM. It is structured as follows:

`x | x | pic_dynamic | led_en | pic_index[3:0]`

To program a custom picture use the `c` command. The index must be provided as a two character decimal value. The data must be provided by 12 character array. Every color has 8 bit depth and must be provided in decimal format (between 0 and 255).

In the example folder you can find a python class as well as a simple example using this class.
## Hardware expansion headers
An expansion header is placed on the backside of the PCB. The connectivity is written in the silkscreen. Currently no functionality is implemented through this header but it can be used in custom software. Another expansion capability is the header after the last LED. Additional LEDs could be placed in the data path. Make sure to use the same model (SK6812 RGBW) to guarantee protocol compatibility. 