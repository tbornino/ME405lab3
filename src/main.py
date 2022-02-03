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
import print_task
import encoder
import motor
import pidcontroller


kp = 0.9*(360/_PPR)
ki = 0*(360/_PPR)
kd = 0*(360/_PPR)
# Read time length of step response from serial port
_stepResponseTime = 3

def task_enc1_fun():
    """!
    Task which reads encoders position
    """
    while True:
        encoder1_share.put (encoder1.read())
        yield ()

def task_enc2_fun():
    """!
    Task which reads encoders position
    """
    while True:
        encoder2_share.put (encoder2.read())
        yield ()
        
def task_controller1_fun ():
    """!
    Task that runs a PID controller.
    """
    while True:
        motor1.set_duty_cycle(pidController1.run()) # set motor duty
        shares.print_task.put(pidController1.get_data_str())
        yield ()

def task_controller2_fun ():
    """!
    Task that runs a PID controller.
    """
    while True:
        motor2.set_duty_cycle(pidController2.run()) # set motor duty
        yield ()


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
    encoder1_share = task_share.Share('i', thread_protect = False, name = "Encoder 1 Share")
    encoder2_share = task_share.Share('i', thread_protect = False, name = "Encoder 2 Share")
    
     # Instantiate encoder 1 with default pins and timer
    encoder1 = encoder.EncoderDriver(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    encoder2 = encoder.EncoderDriver(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 8)
    
    # Instantiate proportional controller 1
    pidController1 = pidcontroller.PIDController(0, 1, 0, 0, encoder1_share)
    pidController2 = pidcontroller.PIDController(0, 1, 0, 0, encoder2_share)
    
    pidController1.set_gains(kp, ki, kd)
    pidController2.set_gains(kp, ki, kd)
    # Read desired set point position from serial port
    # Converts degrees to ticks
    pidController1.set_set_point(float(360)*(_PPR/360))
    pidController2.set_set_point(float(360)*(_PPR/360))
    
    # Instantiate motor 1 with default pins and timer
    motor1 = motor.MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4,
                               pyb.Pin.board.PB5, pyb.Timer(3, freq=20000))
    motor2 = motor.MotorDriver(pyb.Pin.board.PC1, pyb.Pin.board.PA0,
                               pyb.Pin.board.PA1, pyb.Timer(5, freq=20000))
    
#     share0 = task_share.Share ('h', thread_protect = False, name = "Share 0")
#     q0 = task_share.Queue ('L', 16, thread_protect = False, overwrite = False,
#                            name = "Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task_encoder1 = cotask.Task (task_enc1_fun, name = 'Encoder_1_Task', priority = 2, 
                         period = 10, profile = True, trace = False)
    task_encoder2 = cotask.Task (task_enc2_fun, name = 'Encoder_2_Task', priority = 2, 
                         period = 10, profile = True, trace = False)
    task_controller1 = cotask.Task (task_controller1_fun, name = 'Controller_1_Task', priority = 1, 
                         period = 10, profile = True, trace = False)
    task_controller2 = cotask.Task (task_controller2_fun, name = 'Controller_2_Task', priority = 1, 
                         period = 10, profile = True, trace = False)
    
    # In the main module or wherever tasks are created:
    shares.print_task = print_task.PrintTask (name = 'Printing', 
        buf_size = 100, thread_protect = True, priority = 0)
    cotask.task_list.append (shares.print_task)
    cotask.task_list.append (task_encoder1)
    cotask.task_list.append (task_controller1)
    cotask.task_list.append (task_encoder2)
    cotask.task_list.append (task_controller2)

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
