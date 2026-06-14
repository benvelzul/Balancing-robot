from machine import Pin, I2C, PWM
import time
import math

# ==========================================
# 1. INITIALIZATION & HARDWARE SETUP
# ==========================================

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)

try:
    i2c.writeto(0x53, b"\x2D\x08")
except OSError:
    print("Failed to find ADXL345 sensor. Check wiring!")

# Motor Driver Pins
motor_l_0 = PWM(Pin(2, Pin.OUT))
motor_l_1 = PWM(Pin(3, Pin.OUT))
motor_l_0.freq(1000)
motor_l_1.freq(1000)

motor_r_0 = PWM(Pin(4, Pin.OUT))
motor_r_1 = PWM(Pin(5, Pin.OUT))
motor_r_0.freq(1000)
motor_r_1.freq(1000)

# ==========================================
# 2. PID VARIABLES & TUNING CONSTANTS
# ==========================================
KP = 15.0   
KI = 0.5    
KD = 1.2    

target_angle = 75
error_integral = 0.0
last_error = 0.0
last_time = time.ticks_ms()

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def get_angles():
    """Reads ADXL345 and returns (pitch, roll) in degrees."""
    try:
        i2c.writeto(0x53, b"\x32")
        d = i2c.readfrom(0x53, 6)

        x = (d[1] << 8 | d[0]) - 65536 if (d[1] << 8 | d[0]) > 32767 else (d[1] << 8 | d[0])
        y = (d[3] << 8 | d[2]) - 65536 if (d[3] << 8 | d[2]) > 32767 else (d[3] << 8 | d[2])
        z = (d[5] << 8 | d[4]) - 65536 if (d[5] << 8 | d[4]) > 32767 else (d[5] << 8 | d[4])

        # Prevent division by zero errors if sensor is perfectly flat
        if x == 0 and z == 0: x = 0.001
        if y == 0 and z == 0: y = 0.001

        # Calculate standard Pitch and Roll formulas
        pitch = math.atan2(x, math.sqrt(y*y + z*z)) * (180.0 / math.pi)
        roll = math.atan2(y, math.sqrt(x*x + z*z)) * (180.0 / math.pi)
        
        return pitch, roll
    except OSError:
        return 0.0, 0.0

def control_motors(speed):
    speed = max(min(speed, 65535), -65535)
    duty = int(abs(speed))
    
    if speed >= 0:
        motor_l_0.duty_u16(duty)
        motor_l_1.duty_u16(0)
        motor_r_0.duty_u16(duty)
        motor_r_1.duty_u16(0)
    else:
        motor_l_0.duty_u16(0)
        motor_l_1.duty_u16(duty)
        motor_r_0.duty_u16(0)
        motor_r_1.duty_u16(duty)

def stop_motors():
    motor_l_0.duty_u16(0)
    motor_l_1.duty_u16(0)
    motor_r_0.duty_u16(0)
    motor_r_1.duty_u16(0)

# ==========================================
# 4. MAIN CONTROL LOOP
# ==========================================

while True:
    # 1. Get current orientation values
    pitch, roll = get_angles()
    
    # -----------------------------------------------------------------
    # STEP 1: TEST YOUR ROBOT'S TILT
    # Physically tilt your robot forward and backward like it's falling.
    # Look at the terminal below. Decide which number changes drastically.
    # Replace 'pitch' with 'roll' below if Roll is your balancing axis!
    # -----------------------------------------------------------------
    current_angle = pitch 
    
    # Print format optimized for Thonny Plotter (View -> Plotter)
    print(f"Pitch:{pitch}, Roll:{roll}")

    # 2. Safety Cutoff
    if abs(current_angle) > 45:
        stop_motors()
        error_integral = 0 
        time.sleep_ms(100)
        continue

    # 3. Time Delta
    now = time.ticks_ms()
    dt = time.ticks_diff(now, last_time) / 1000.0  
    if dt <= 0: 
        dt = 0.001
    last_time = now

    # 4. PID Execution
    error = target_angle - current_angle
    error_integral += error * dt
    error_derivative = (error - last_error) / dt
    last_error = error

    pid_output = (KP * error) + (KI * error_integral) + (KD * error_derivative)
    motor_speed = pid_output * 1000 
    
    # Comment this out while testing angles if you don't want the motors 
    # jumping around in your hands yet!
    control_motors(motor_speed)
        
    time.sleep_ms(20)