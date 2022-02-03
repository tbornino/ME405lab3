"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share

kp = 0.9*(360/_PPR)
ki = 0*(360/_PPR)
kd = 0*(360/_PPR)
# Read time length of step response from serial port
_stepResponseTime = 3

def task_enc_fun():
    """!
    Task which reads encoders position
    """
    while True:
        encoder_share.put (encoder1.read())
        yield ()

def task_controller_fun ():
    """!
    Task that runs a PID controller.
    """
    while True:
        motor1.set_duty_cycle(pidController1.run()) # set motor duty
        yield ()


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
    encoder_share = task_share.Share('i', thread_protect = False, name = "Encoder Share")
    
     # Instantiate encoder 1 with default pins and timer
    encoder1 = encoder.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    
    # Instantiate proportional controller 1
    pidController1 = pidcontroller.PIDController(0, 1, 0, 0, encoder_share)
    
    pidController1.set_gains(kp, ki, kd) # Kd
    # Read desired set point position from serial port
    # Converts degrees to ticks
    pidController1.set_set_point(float(360)*(_PPR/360))
    
    # Instantiate motor 1 with default pins and timer
    motor1 = motor.MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4,
                               pyb.Pin.board.PB5, pyb.Timer(3, freq=20000))
    
#     share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
#     q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
#                            name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task_encoder = cotask.Task (task_enc_fun, name = 'Encoder_Task', priority = 2, 
                         period = 10, profile = True, trace = False)
    task_controller = cotask.Task (task_controller_fun, name = 'Controller_Task', priority = 1, 
                         period = 10, profile = True, trace = False)
    cotask.task_list.append (task_encoder)
    cotask.task_list.append (task_controller)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
