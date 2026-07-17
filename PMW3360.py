import time
import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

# 1. Initialize SPI0 Pins
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)

# 2. Configure Chip Select (NCS) Pin
cs = digitalio.DigitalInOut(board.GP17)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True

# 3. Create the SPI Device (PMW3360 Max SPI Speed is 2MHz)
pmw_sensor = SPIDevice(spi, cs, baudrate=2000000, polarity=1, phase=1)

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

# 4. Read Product ID Register (0x00) to verify connection
print("Initializing PMW3360...")
time.sleep(0.1) # Wait for sensor to boot up

product_id = read_register(0x00)
print(f"Product ID: {hex(product_id)} (Expected: 0x42)")

if product_id == 0x42:
    print("Successfully connected to PMW3360!")
else:
    print("Connection failed. Check your wiring and level shifter.")

