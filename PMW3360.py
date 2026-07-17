import time
import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice
import usb_hid
from adafruit_hid.mouse import Mouse

# Initialize USB HID Mouse
mouse = Mouse(usb_hid.devices)

# 1. Initialize SPI0 Pins
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)

# 2. Configure Chip Select (NCS) Pin
cs = digitalio.DigitalInOut(board.GP17)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

# 3. Create the SPI Device (PMW3360 Max SPI Speed is 2MHz)
pmw_sensor = SPIDevice(spi, cs, baudrate=2000000, polarity=1, phase=1)

# 4. Configure Mouse Buttons
left_button = digitalio.DigitalInOut(board.GP2)
left_button.direction = digitalio.Direction.INPUT
left_button.pull = digitalio.Pull.UP

right_button = digitalio.DigitalInOut(board.GP3)
right_button.direction = digitalio.Direction.INPUT
right_button.pull = digitalio.Pull.UP

# 5. Configure Mouse Encoder (Quadrature Encoder)
encoder_za = digitalio.DigitalInOut(board.GP7)
encoder_za.direction = digitalio.Direction.INPUT
encoder_za.pull = digitalio.Pull.UP

encoder_zb = digitalio.DigitalInOut(board.GP6)
encoder_zb.direction = digitalio.Direction.INPUT
encoder_zb.pull = digitalio.Pull.UP

def read_register(reg_address):
    # Mask the address to ensure the write bit is 0 for reading
    reg_address &= 0x7F
    
    # SPI buffer for outbound and inbound data
    out_buf = bytearray([reg_address, 0x00])
    in_buf = bytearray(2)
    
    with pmw_sensor as device:
        # NCS automatically drops low here
        device.write_readinto(out_buf, in_buf)
        # NCS goes high here
        
    return in_buf[1]

# 6. Read Product ID Register (0x00) to verify connection
print("Initializing PMW3360...")
time.sleep(0.1) # Wait for sensor to boot up

product_id = read_register(0x00)
print(f"Product ID: {hex(product_id)} (Expected: 0x42)")

if product_id == 0x42:
    print("Successfully connected to PMW3360!")
else:
    print("Connection failed. Check your wiring and level shifter.")
