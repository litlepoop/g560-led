# Logitech G560 Gaming Speakers LED control

Allows you to control the LED lighting of your G560 Gaming Speakers programmatically.

## Requirements

- Python 3.5+
- PyUSB 1.2.1+
- **Root privileges**

Optional for selection using GUI:

 - TkInter (Package python3-tk) 

## Installation

```bash
git clone https://github.com/litlepoop/g560-led.git
cd g560-led
virtualenv ./env
env/bin/pip install -r requirements.txt
```

**Test**

```bash
sudo ./g560-led.py solid 00FF00
```

## Usage

```text
Usage:
    g560-led [help|--help|-h] - This help
    g560-led solid {color} - Solid color mode
    g560-led cycle [{rate} [{brightness}]] - Cycle through all colors
    g560-led breathe {color} [{rate} [{brightness}]] - Single color breathing
    g560-led gui - GUI Pop-Up for selecting color
    g560-led off - Turn lights off

Arguments:
    color: RRGGBB (RGB hex value)
    rate: 100-60000 (Value in milliseconds. Default: 10000ms)
    brightness: 0-100 (Percentage. Default: 100%)
```

Note that the G560 has four independent lights: currently this script will set all to the same color.
The GUI color picker is able to set each light individually.

Fork of [g560-led](https://github.com/claudiosanches/g560-led).
Inspired by and based on [g810-led](https://github.com/MatMoul/g810-led),
[g203-led](https://github.com/smasty/g203-led), [g403-led](https://github.com/stelcheck/g403-led), and [g560-led](https://github.com/mijoe/g560-led).
