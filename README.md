# ME405 Lab 3: On Schedule

## Scheduling Experiments


## Step Response Plots
| ![Step Response 1: K_P = 0.3](plots/KP=0.3.png) |
|:--:|
|**Figure 1: K<sub>P</sub> = 0.3**|

The first proportional controller value shows that the system doesnt reach the desired setpoint, so we have to gradually
increase it in order to get closer to our desired value for the second order system.

| ![Step Response 2: K_P = 1.2](plots/KP=1.2.png) |
|:--:|
|**Figure 2: K<sub>P</sub> = 1.2**|


| ![Step Response 3: K_P = 0.9](plots/KP=0.9.png) |
|:--:|
|**Figure 3: K<sub>P</sub> = 0.9**|

Figure 3 shows an acceptable response with nearly overshoot and settles with a negligible amount of steady state error.
| ![Step Response 4: K_P = 36](plots/KP=36.png) |
|:--:|
|**Figure 4: K<sub>P</sub> = 36**|

After tuning to a proper K_p value of about 1.2 in Figure 3, we wanted to find the point of marginal stability of the system
and we found that a proportional controller value of K_p = 36 works well to give us marginal stability. We can tell it is 
marginally stable by the near sinusoidal shape of the plot as it oscillates about the set point. 