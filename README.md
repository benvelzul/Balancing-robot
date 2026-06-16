# Raspberry Pi Pico Self-Balancing Robot

An open-source, two-wheeled self-balancing robot built around the **Raspberry Pi Pico (RP2040)**. This project implements an inverted pendulum control system, fusing data from an IMU sensor to dynamically adjust DC motors using a high-frequency PID control loop.

---

## How It Works: The Inverted Pendulum

Balancing a two-wheeled robot is a classic control theory problem known as the **Inverted Pendulum**. Think of it like trying to balance a broomstick upright on the palm of your hand: if the broom tilts forward, you must move your hand forward to keep it from falling. 

The Raspberry Pi Pico handles this problem in a continuous, high-speed loop:
1. **Sense:** The MPU6050 sensor measures gravity and rotational acceleration to determine the robot's current tilt angle.
2. **Calculate:** The Pico compares the current angle to the target angle (usually `0°`, perfectly vertical) to compute the **Error**.
3. **Correct:** The error is fed into a **PID algorithm**, which calculates the exact motor speed and direction required to counteract the tilt.
4. **Act:** The Pico sends PWM signals to the motor driver, driving the wheels directly beneath the center of gravity to restore balance.

---

## Understanding PID Control

Instead of just kicking the motors into full gear whenever the robot tilts, a **PID (Proportional, Integral, Derivative)** loop calculates smooth, precise corrections. It relies on three distinct components:

### 1. Proportional (The Present)
* **Concept:** Reacts strictly to the *current* error. The further the robot tilts, the harder the motors push.
* **Limitation:** On its own, Proportional control causes the robot to violently overshoot the balance point back and forth until it crashes.

### 2. Derivative (The Future)
* **Concept:** Looks at the *speed* of the tilt (how fast the error is changing) and acts as a brake. 
* **Role:** It dampens the oscillations caused by the Proportional term, slowing the motors down as the robot approaches perfect verticality to prevent overshooting.

### 3. Integral (The Past)
* **Concept:** Accumulates small errors over *time*. 
* **Role:** If the robot is stuck tilting slightly at 1° or 2° (due to mechanical friction or an offset center of mass) and the P-term isn't strong enough to fix it, the Integral term winds up power over time until the robot is forced back to absolute zero.

---

## Hardware Configuration & Pinout

This project leverages the dual-core RP2040 on the Raspberry Pi Pico to separate sensor reading and motor driving tasks.

| Raspberry Pi Pico Pin | Component | Component Pin | Function |
| :--- | :--- | :--- | :--- |
| **3V3 (Pin 36)** | MPU6050 | VCC | 3.3V Power |
| **GND (Pin 38)** | MPU6050 / Driver | GND | Common Ground |
| **GP4 (Pin 6)** | MPU6050 | SDA | I2C Data |
| **GP5 (Pin 7)** | MPU6050 | SCL | I2C Clock |
| **GP14 (Pin 19)** | Motor Driver | PWM_A | Left Motor Speed (PWM) |
| **GP15 (Pin 20)** | Motor Driver | PWM_B | Right Motor Speed (PWM) |
| **GP16 (Pin 21)** | Motor Driver | IN1 | Left Motor Dir 1 |
| **GP17 (Pin 22)** | Motor Driver | IN2 | Left Motor Dir 2 |

> **Safety Notice:** Ensure your motor driver and Raspberry Pi Pico share a common ground (GND). Never power the Pico directly from raw motor batteries unless passing through a dedicated 5V/3.3V regulator.

---

## Tuning Guide

When adjusting the PID variables ($K_p$, $K_i$, $K_d$) in the code, follow this sequence:

1. **Set all gains to zero** ($K_p=0, K_i=0, K_d=0$).
2. **Increase $K_p$** until the robot stands up briefly and starts oscillating rhythmically back and forth.
3. **Increase $K_d$** to add damping. You will feel the robot become "stiff" and the oscillations will smooth out into a stable hover.
4. **Increase $K_i$** marginally if the robot balances well but slowly drifts across the floor over time.

---

## Contributing
Feel free to open issues or submit pull requests to help optimize the PID stability or add telemetry logging features!

---

## Project Status & Roadmap
- [x] Assemble 3D-printed chassis
- [/] Read stable angles from IMU using Complementary Filter
- [/] Tune PID constants (Currently stable for ~2 seconds, tends to drift)
- [ ] Implement Bluetooth remote control app
- [ ] Add wheel encoders for position holding

---

## CAD
I designed and fabricated a new, updated base intended to improve structural integrity. However, during the assembly phase, I ran into a clearance issue—the motors did not fit properly into the new mounts. As a result, I had to pivot and revert back to the previous design iteration.
<img width="1333" height="2000" alt="Untitled design (2)" src="https://github.com/user-attachments/assets/e3c236c2-41dc-45c8-b30a-3dbe9934bc36" />
Therefore I had to use the old version and then hotglue the components for a proof of concept. 
<img width="1333" height="2000" alt="Untitled design" src="https://github.com/user-attachments/assets/36cacd5d-492b-4f10-b27b-942b735172a5" />

