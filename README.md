# ME405 Lab 3: On Schedule

## Scheduling Experiments

The purpose of this lab is to run tasks simultaneously using a real time scheduler. The main goal is to get proper multitasking
between multiple motors using previous lab assignments. We're able to run more than one motor at once in combination with our generic 
controller from Lab 2. As we run these experiments, we're interested in running the tasks at slower and slower rates until the response
of the motors is noticeably delayed, and affects the controller performance. Below are step response plots that show the tasks running
at a relatively fast rate of 10ms, and then we can see when the tasks are running at a rate of 75ms, the step response is noticeably worse
and does not reach the set point efficiently due to %OS and having to control the response back to the set point. As we increased the time 
rate, we noticed that the steady state error steadily increases until about the 75ms response. So although there is a noticeable steady state
error in the response, it takes about the same amount of time to reach the set point and the SSE could be eliminated through the use of an
integral controller in addition to the proportional controller used.


## Step Response Plots
| ![Step Response 1: K_P = 0.9](plots/10ms.png) |
|:--:|
|**Figure 1: K<sub>P</sub> = 0.9, Task Run Rate = 10ms**|


| ![Step Response 2: K_P = 0.9](plots/50ms.png) |
|:--:|
|**Figure 2: K<sub>P</sub> = 0.9, Task Run Rate = 50ms**|


| ![Step Response 2: K_P = 0.9](plots/75ms.png) |
|:--:|
|**Figure 3: K<sub>P</sub> = 0.9, Task Run Rate = 75ms**|