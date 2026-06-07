from machine import Pin, I2C
import time

# Initialize I2C (Adjust pins if you moved them to GP4/GP5)
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)

# Wake up ADXL345 sensor
i2c.writeto(0x53, b"\x2D\x08")

while True:
    try:
        # Request 6 bytes starting from register 0x32
        i2c.writeto(0x53, b"\x32")
        d = i2c.readfrom(0x53, 6)

        # Convert raw bytes into X, Y, Z integers
        x = (d[1] << 8 | d[0]) - 65536 if (d[1] << 8 | d[0]) > 32767 else (d[1] << 8 | d[0])
        y = (d[3] << 8 | d[2]) - 65536 if (d[3] << 8 | d[2]) > 32767 else (d[3] << 8 | d[2])
        z = (d[5] << 8 | d[4]) - 65536 if (d[5] << 8 | d[4]) > 32767 else (d[5] << 8 | d[4])

        # This exact format is required for the Thonny Plotter
        print(f"({x}, {y}, {z})")
        
    except OSError:
        # Prevents program from crashing if a wire loose-connects momentarily
        pass
        
    time.sleep_ms(50)
