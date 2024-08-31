#!env/bin/python

#
# Logitech G560 Gaming Speakers LED control
#

import sys
import usb.core
import usb.util
import re
import binascii

vendor_id = 0x046d # Logitech
product_id = 0x0a78 # G560 Gaming Speaker
default_rate = 10000
default_brightness = 100
dev = None
wIndex = None


def help():
    print("""Logitech G560 Gaming Speaker LED control

Usage:
\tg560-led [help|--help|-h] - This help
\tg560-led solid {color} - Solid color mode
\tg560-led cycle [{rate} [{brightness}]] - Cycle through all colors
\tg560-led breathe {color} [{rate} [{brightness}]] - Single color breathing
\tg560-led gui - GUI Pop-Up for selecting color
\tg560-led off - Turn lights off

Arguments:
\tcolor: RRGGBB (RGB hex value)
\trate: 100-60000 (Value in milliseconds. Default: 10000ms)
\tbrightness: 0-100 (Percentage. Default: 100%)""")


def main():
    if (len(sys.argv) < 2):
        help()
        sys.exit()

    args = sys.argv + [None] * (5 - len(sys.argv))
    mode = args[1]
    if (mode in ['--help', '-h', 'help']):
        help()
        sys.exit()
    elif mode == 'solid':
        set_led_solid(process_color(args[2]))
    elif mode == 'cycle':
        set_led_cycle(process_rate(args[2]), process_brightness(args[3]))
    elif mode == 'breathe':
        set_led_breathe(
            process_color(args[2]),
            process_rate(args[3]),
            process_brightness(args[4])
        )
    elif mode == 'gui':
        set_led_gui()
    elif mode == 'off':
        set_led_solid(process_color('000000'))
    else:
        print_error('Unknown mode.')


def print_error(msg):
    print('Error: ' + msg)
    sys.exit(1)


def process_color(color):
    if not color:
        print_error('No color specifed.')
    if color[0] == '#':
        color = color[1:]
    if not re.match('^[0-9a-fA-F]{6}$', color):
        print_error('Invalid color specified.')
    return color.lower()


def process_rate(rate):
    if not rate:
        rate = default_rate
    try:
        return '{:04x}'.format(max(100, min(65535, int(rate))))
    except ValueError:
        print_error('Invalid rate specified.')


def process_brightness(brightness):
    if not brightness:
        brightness = default_brightness
    try:
        return '{:02x}'.format(max(1, min(100, int(brightness))))
    except ValueError:
        print_error('Invalid brightness specified.')


def set_led_solid(color):
    return set_led('01', color + '0000000000')


def set_led_breathe(color, rate, brightness):
    return set_led('04', color + rate + '00' + brightness + '00')


def set_led_cycle(rate, brightness):
    return set_led('02', '0000000000' + rate + brightness)



def set_led_gui():
    try:
        import tkinter as tk
    except ImportError:
        print_error('TkInter missing - Please install package python3-tk')
    from tkinter.colorchooser import askcolor
    
    # Default values Color picker (Black)
    global color0
    color0 = '#000000'
    global color1
    color1 = '#000000'
    global color2
    color2 = '#000000'
    global color3
    color3 = '#000000'
    global color4
    color4 = '#000000'

    # Set all black
    set_led_solid(process_color('000000'))
    
    # Function to open the color picker and display the selected color
    def choose_color0():
        global color0
        color = askcolor(color0)[1]
        if color:
            color_label0.config(text=f"Color Left Ring: {color[1:]}", bg=color)
            color_label4.config(text=f"Color All: None", bg=colordef)
            set_led_single('01', color[1:] + '0000000000', '00')
            color0 = color
    def choose_color1():
        global color1
        color = askcolor(color1)[1]
        if color:
            color_label1.config(text=f"Color Right Ring: {color[1:]}", bg=color)
            color_label4.config(text=f"Color All: None", bg=colordef)
            set_led_single('01', color[1:] + '0000000000', '01')
            color1 = color
    def choose_color2():
        global color2
        color = askcolor(color2)[1]
        if color:
            color_label2.config(text=f"Color Left Back: {color[1:]}", bg=color)
            color_label4.config(text=f"Color All: None", bg=colordef)
            set_led_single('01', color[1:] + '0000000000', '02')
            color2 = color
    def choose_color3():
        global color3
        color = askcolor(color3)[1]
        if color:
            color_label3.config(text=f"Color Right Back: {color[1:]}", bg=color)
            color_label4.config(text=f"Color All: None", bg=colordef)
            set_led_single('01', color[1:] + '0000000000', '03')
            color3 = color
    def choose_color4():
        global color0
        global color1
        global color2
        global color3
        global color4
        color = askcolor(color4)[1]
        if color:
            color_label0.config(text=f"Color Left Ring: {color[1:]}", bg=color)
            color_label1.config(text=f"Color Right Ring: {color[1:]}", bg=color)
            color_label2.config(text=f"Color Left Back: {color[1:]}", bg=color)
            color_label3.config(text=f"Color Right Back: {color[1:]}", bg=color)
            color_label4.config(text=f"Color All: {color[1:]}", bg=color)
            set_led('01', color[1:] + '0000000000')
            color4 = color
            color3 = color
            color2 = color
            color1 = color
            color0 = color

    # Main Window
    parent = tk.Tk()
    parent.title("G560 - Color Picker")
    
    # Labels and Buttons
    color_label0 = tk.Label(parent, text="Color Left Ring: None", font=("Helvetica", 14), padx=10, pady=10)
    color_label0.pack()
    choose_button0 = tk.Button(parent, text="Choose Color", command=choose_color0)
    choose_button0.pack(pady=10)
    
    color_label1 = tk.Label(parent, text="Color Right Ring: None", font=("Helvetica", 14), padx=10, pady=10)
    color_label1.pack()
    choose_button1 = tk.Button(parent, text="Choose Color", command=choose_color1)
    choose_button1.pack(pady=10)
    
    color_label2 = tk.Label(parent, text="Color Left Back: None", font=("Helvetica", 14), padx=10, pady=10)
    color_label2.pack()
    choose_button2 = tk.Button(parent, text="Choose Color", command=choose_color2)
    choose_button2.pack(pady=10)
    
    color_label3 = tk.Label(parent, text="Color Right Back: None", font=("Helvetica", 14), padx=10, pady=10)
    color_label3.pack()
    choose_button3 = tk.Button(parent, text="Choose Color", command=choose_color3)
    choose_button3.pack(pady=10)
    
    color_label4 = tk.Label(parent, text="Color All: None", font=("Helvetica", 14), padx=10, pady=10)
    color_label4.pack()
    choose_button4 = tk.Button(parent, text="Choose Color", command=choose_color4)
    choose_button4.pack(pady=10)    
    
    # Get label default color 
    global colordef
    colordef = color_label0.cget("bg")
    
    # Start the Tkinter event loop
    parent.mainloop()


def set_led(mode, data):
    global device
    global wIndex

    prefix = '11ff043a'
    left_secondary = '00'
    right_secondary = '01'
    left_primary = '02'
    right_primary = '03'
    suffix = '000000000000'
 
    send_command(prefix + left_secondary + mode + data + suffix)
    send_command(prefix + right_secondary + mode + data + suffix)
    send_command(prefix + left_primary + mode + data + suffix)
    send_command(prefix + right_primary + mode + data + suffix)
    
    
def set_led_single(mode, data, pos):
    global device
    global wIndex

    prefix = '11ff043a'
    suffix = '000000000000'
    send_command(prefix + pos + mode + data + suffix)

    
def send_command(data):
    attach_device()
    device.ctrl_transfer(0x21, 0x09, 0x0211, wIndex, binascii.unhexlify(data))
    detach_device()


def attach_device():
    global device
    global wIndex

    device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    if device is None:
        print_error('No compatible devices found.')

    wIndex = 0x02
    if device.is_kernel_driver_active(wIndex) is True:
        device.detach_kernel_driver(wIndex)
        usb.util.claim_interface(device, wIndex)


def detach_device():
    global device
    global wIndex
    if wIndex is not None:
        usb.util.release_interface(device, wIndex)
        device.attach_kernel_driver(wIndex)
        device = None
        wIndex = None


if __name__ == '__main__':
    main()
