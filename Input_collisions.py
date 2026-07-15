def on_device_input(self, value):
    """Handle incoming device value, overriding local keyboard highlights."""
    self.last_device_input = value  # Track for debugging
    if 0 <= value <= 14:
        self.tip_touch(value)
    else:
        self.tip_touch(16)
