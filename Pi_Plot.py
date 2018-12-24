from __future__ import with_statement
#   http://www.pyqtgraph.org/documentation/colormap.html
import numpy as np
import decimal, time
import pyqtgraph as pg
import pyqtgraph.exporters

def pi_gauss_legendre():
    D = decimal.Decimal
    with decimal.localcontext() as ctx:
        ctx.prec += 2                
        a, b, t, p = 1, 1/D(2).sqrt(), 1/D(4), 1                
        pi = None
        while 1:
            an    = (a + b) / 2
            b     = (a * b).sqrt()
            t    -= p * (a - an) * (a - an)
            a, p  = an, 2*p
            piold = pi
            pi    = (a + b) * (a + b) / (4 * t)
            if pi == piold:  # equal within given precision
                break
    return +pi

starttime=time.process_time()
DigitCount =  1000000

decimal.getcontext().prec = DigitCount + 1   #8751
pi = pi_gauss_legendre()
stoptime=time.process_time()
# print(pi)
duration = stoptime - starttime
if duration == 0:
    duration = .0001    # if calculation take less than one second, this prevents a divide by zero error.
decimalPlaces = len(str(pi))-2
CharPerSec = decimalPlaces/(duration)

print('Decimal Places Calculated: {0:,d}'.format(decimalPlaces))
print('After {0:5.4f} seconds of computation, {1:,d} decimal places were computed resulting is a {2:5.3f} decimals/second.'.format(duration, decimalPlaces, CharPerSec))

# define the data
theTitle = "Plot " + format(DigitCount, ",d") + " digits of PI()"

xDict = {0: 0, 1: 1.2, 2: 2.4, 3: 2.4, 4: 1.2, 5: 0, 6: -1.2, 7: -2.4, 8: -2.4, 9: -1.2}
yDict = {0: 3, 1: 1.8, 2: 0.6, 3: -0.6, 4: -1.8, 5: -3, 6: -1.8, 7: -0.6, 8: 0.6, 9: 1.8}

y = []
x = []
sPi = str(pi)

for index in range(2, len(sPi)):       #   Build the plot series
    if index == 2:
        x.append(0)
        y.append(0)
    else:
        x.append(float(xDict[int(sPi[index])]) + x[index-3])
        y.append(float(yDict[int(sPi[index])]) + y[index-3])

# create plot
    
pg.setConfigOption('background', 'w')
plt = pg.plot(x, y, title=theTitle, pen='b')    #, symbol='.')
plt.showGrid(x=True,y=True)
plt.hideAxis('left')
plt.hideAxis('bottom')

# exporter = pg.exporters.ImageExporter(plt.plotItem)
# exporter.parameters()['width'] = int(100)
# exporter.export('Output.png')


## Start Qt event loop.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
