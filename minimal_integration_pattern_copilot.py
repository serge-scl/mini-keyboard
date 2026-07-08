# Add after creating the main UI, before mainloop:
self.start_device_listener()

def start_device_listener(self):
    """Start listening for external device input (serial/socket)."""
    # Example: serial input on a separate thread
    import threading
    import serial  # or socket, depending on your device
    
    def listen_device():
        try:
            # Adjust port and baudrate to match your device
            ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
            while True:
                line = ser.readline()
                if line:
                    try:
                        value = int(line.decode().strip())
                        # Schedule GUI update on the main thread
                        self.window0.after(0, self.on_device_input, value)
                    except (ValueError, UnicodeDecodeError):
                        pass
        except Exception as e:
            print(f"Device listener error: {e}")
    
    thread = threading.Thread(target=listen_device, daemon=True)
    thread.start()

def on_device_input(self, value):
    """Handle incoming device value (0–15)."""
    if 0 <= value <= 14:
        self.tip_touch(value)  # Highlight pyramid cell
    else:
        self.tip_touch(16)  # Clear highlighting
