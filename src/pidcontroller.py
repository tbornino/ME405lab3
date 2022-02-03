'''!@file pidcontroller.py
    A class that performs closed loop pid control.
    
    @author     Tori Bornino
    @author     Jackson McLaughlin
    @author     Zach Stednitz
    @date       February 3, 2022
'''

import time

class PIDController:
    '''! 
    This class implements a generic proportional controller.
    '''
   
    def __init__ (self, set_point, Kp, Ki, Kd, sensor_share):
        '''! 
        Creates a proportional controller by initializing setpoints and gains
        
        @param setpoint      The initial desired location of the step response  
        @param Kp            The proportional gain for the controller.
                             Units of (dutyCycle/ticks)
        @param Ki            The integral gain for the controller.
                             Units of (dutyCycle/(ticks*seconds))
        @param Kd            The derivative gain for the controller.
                             Units of (dutyCycle/(ticks/seconds))
        @param sensor_share  A share the contains the read position from sensor        
        '''
        self._set_point = set_point
        self._Kp = Kp
        self._Ki = Ki
        self._Kd = Kd
        self._sensor_share = sensor_share
        
        ##  @brief      Stored Step Response Data.
        #   @details    Recorded as (time(ms), position(ticks))
        self.data_list = []
        
        ##  @brief      Step response start time
        self.start_time = None
        
        self._last_time = 0
        self._last_error = 0
        self._Iduty = 0
        
        # Active Data Store Counter
        ## Number of times the controller runs before a data sample is stored
        self.data_store_counter = 1
        self._counter = self.data_store_counter
        
        
    def run(self):
        '''! 
        Continuously runs the control algorithm. Reads the position data from a
        sensor and then finds the error between the actual position and the 
        desired setpoint value. Then we append the stored data list with a
        tuple of values.
        
        @return The actuation value to fix steady state error.
        '''
        # Store initial step time
        if self.start_time == None:
            self.start_time = time.ticks_ms()
            self._last_time = self.start_time
        
        # Calculate the current error in position
        error = self._sensor_share.read() - self._set_point
        curr_time = time.ticks_diff(time.ticks_ms(),self.start_time)
        
        # Calculate the PID actuation value
        Pduty = self._Kp*error
        
        _Iduty_new = self._Ki*error*(curr_time - self._last_time)
        if (self._Iduty > 0 and _Iduty_new < 0) \
            or  (self._Iduty < 0 and _Iduty_new > 0):
            self._Iduty = _Iduty_new
        else:
            self._Iduty += _Iduty_new
        
        Dduty = self._Kd*(error-self._last_error)/(curr_time - self._last_time)
        
        actuation_value = Pduty + self._Iduty + Dduty
        
        # Store the time and position data
        if self._counter <= 0:
            self.data_store()
            self._counter = self.data_store_counter
        else:
            self._counter-=1
        
        # Filter saturated values
        if actuation_value > 100:
            actuation_value = 100
        elif actuation_value < -100:
            actuation_value = -100
        
        # Store values for next iteration
        self._last_error = error
        self._last_time = curr_time
        
        return actuation_value
    
    def set_set_point(self, set_point):
        '''! 
        Sets the desired setpoint for the step response.
        
        @param set_point  The desired steady state response value.  
        '''
        self._set_point = set_point
        
    def set_gains(self, Kp, Ki, Kd):
        '''! 
        Sets the proportional gain controller value.
        
        @param Kp           The proportional gain for the controller.
                            Units of (dutyCycle/ticks)
        @param Ki           The integral gain for the controller.
                            Units of (dutyCycle/(ticks*seconds))
        @param Kd           The derivative gain for the controller.
                            Units of (dutyCycle/(ticks/seconds))
        '''
        self._Kp = Kp
        self._Ki = Ki
        self._Kd = Kd
        
    def data_store(self):
        '''!
        Stores the data in a csv format.
        '''            
        self.data_list.append((time.ticks_diff(time.ticks_ms(),self.start_time),
                                self._sensor_share.read()))
        
    def print_data(self):
        '''!
        Prints each line in the data list in a comma separated format.
        '''
        for data_point in self.data_list:
            print(f"{data_point[0]},{data_point[1]}")
        
        # Reset variables for next step response 
        self.data_list = []
        self.start_time = None
        self._last_time = 0
        self._last_error = 0
        self._Iduty = 0
            
