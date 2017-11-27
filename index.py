import vex, sys, timer

#region config
line_tracker_1 = vex.LineTracker(1)
line_tracker_2 = vex.LineTracker(2)
right_wheel    = vex.Motor(1)
left_wheel     = vex.Motor(2, True)
claw_tower     = vex.Motor(3)
claw_open      = vex.Motor(4)
ultrasonic     = vex.UltrasonicSensor(1, vex.UNIT_CM)
joystick       = vex.Joystick()
green_light    = vex.DigitalOutput(10)
yellow_light   = vex.DigitalOutput(11)
red_light      = vex.DigitalOutput(12)
#endregion config

mode = 0

# main thread

joystick.set_deadband(10)

no_strafe = 50 / 50

is_fast = True

while True:
    green_light.on()
    if joystick.b7down():
        mode = 0
    elif joystick.b7left():
        mode = 1
    elif joystick.b7up():
        mode = 2
    elif joystick.b7right():
        left_wheel.off()
        right_wheel.off()
        claw_open.off()
        claw_tower.off()
        red_light.on()
        yellow_light.on()
        sys.sleep(999999)
    else:
        red_light.off()
        yellow_light.off()
        
    # manual mode
    if mode == 0:
        if joystick.b5up():
            if is_fast:
                is_fast = False
            else:
                is_fast = True
            
        
        if is_fast:
            #use the right knob to drive
            left_wheel.run(((joystick.axis2() * -1) + joystick.axis4()))
            right_wheel.run((joystick.axis2() * -1) - joystick.axis4())
        else:
            #use the right knob to drive
            left_wheel.run(((joystick.axis2() * -1) + joystick.axis4()) * 0.5)
            right_wheel.run((joystick.axis2() * -1) - joystick.axis4() * 0.5)
        
        #use button 8u, r, d, and l to operate The Claw
        if joystick.b6up():
            claw_tower.run(25)
        elif joystick.b6down():
            claw_tower.run(-25)
        elif joystick.b8left():
            claw_open.run(-50)
        elif joystick.b8right():
            claw_open.run(50)
        else:
            claw_tower.off()
            claw_open.off()

    # line tracker
    elif mode == 1:
        is1onwhite = line_tracker_1.raw_value() < 600 #less than 600 = white
        is2onwhite = line_tracker_2.raw_value() < 600

        left_speed = 25
        right_speed = 25
        bonus = 7

        if is1onwhite and is2onwhite:
            left_wheel.run(left_speed)
            right_wheel.run(right_speed)
        elif is1onwhite:
            left_wheel.run(left_speed + bonus)
            right_wheel.off()
        elif is2onwhite:
            right_wheel.run(left_speed + bonus)
            left_wheel.off()
        else:
            left_wheel.off()
            right_wheel.off()

    # obstacle sensor
    elif mode == 2:
        '''
        if ultrasonic.distance() < 40:
            #start_time = time.time()  # remember when we started
            #while (time.time() - start_time) < 0.75:
            #    left_wheel.run(-50)
            #    right_wheel.run(-50)
            
            left_wheel.run(50)
            right_wheel.run(-50)
        else:
            left_wheel.run(50)
            right_wheel.run(50)
        '''
        front = ultrasonic.distance() < 40
        
        right_power = 40
        left_power = 30
        max_distance = 40 # cm
        
        if ultrasonic.distance() < max_distance:
            dist = ultrasonic.distance()
            
            timer_1 = timer.Timer()
            #timer_1.stop()
            #timer_1.reset()
            #timer_1.start()
            #while timer_1.elapsed_time() < 0.5:
            #    left_wheel.run(-left_power)
            #    right_wheel.run(-right_power)
            
            timer_1.stop()
            timer_1.reset()
            timer_1.start()
            while timer_1.elapsed_time() < 0.5:
                left_wheel.run(left_power)
                right_wheel.run(-right_power)
            
                
            timer_1.stop()
            timer_1.reset()
            timer_1.start()
            while timer_1.elapsed_time() < 1 and ultrasonic.distance() < dist + 10:
                left_wheel.run(-left_power)
                right_wheel.run(right_power)
        else:
            left_wheel.run(left_power)
            right_wheel.run(right_power)
