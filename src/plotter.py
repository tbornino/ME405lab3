'''!@file       plotter.py
    The main code to run on the PC to run and plot a step response on
    a motor. Includes functionality to set the setpoint and controller gain.
    The data is exchanged with the microcontroller over serial.
    @author     Tori Bornino
    @author     Jackson McLaughlin
    @author     Zach Stednitz
    @date       January 27, 2022
'''

from matplotlib import pyplot
import serial
import time

_PPR = 256*4*16
_set_point = 360 # deg

# Open serial port with the Nucleo
_port = "COM3"
with serial.Serial(_port, 115200, timeout=1) as ser_port:
    # Reset the Nucleo and start its program
    ser_port.write(b'\x03')
    time.sleep(1)
    ser_port.write(b'\x02')
    time.sleep(1)
    ser_port.write(b'\x04')
    # Receive data from the Nucleo and process it into 2 lists
    _xs = []
    _ys = []
    while True:
        _line = ser_port.readline()
        print(_line)
        if _line == b'Done!\r\n':
            break
        _cells = _line.split(b',')
        try:
            _x = float(_cells[0].strip())
            _y = float(_cells[1].strip())
        except (ValueError, IndexError):
            continue
        _xs.append(_x)
        _ys.append(_y)
# Plot step response
pyplot.plot(_xs, _ys)
# Plot line for setpoint
_t_max = _xs[-1]
_set_point_ticks = _set_point * _PPR / 360
pyplot.plot([0, _t_max], [_set_point_ticks, _set_point_ticks], 'r--')
pyplot.xlabel("time [ms]")
pyplot.ylabel("position [ticks]")
pyplot.show()