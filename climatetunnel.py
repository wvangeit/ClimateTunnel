"""Polar plot of temperature"""

import os
import numpy

import matplotlib

matplotlib.use('Agg')

import matplotlib.animation as animation
import matplotlib.collections as collections
import matplotlib.pyplot as plt


plt.style.use('ggplot')

data_dir = 'data'

csv_filename = os.path.join(data_dir, 'GLB.Ts+dSST.csv')
data = numpy.genfromtxt(
    csv_filename,
    delimiter=',',
    skip_header=2,
    missing_values=['***'],
    filling_values=[float('nan')])

print data
years = [int(y[0]) for y in data]

fig = plt.figure(figsize=(12, 12))

ax = fig.add_subplot(1, 1, 1, projection='polar')

marker, = ax.plot([], [], '.', alpha=.3, ms=10, mfc='black')
line = collections.LineCollection(
    [],
    linewidth=10,
    alpha=.2,
    cmap=plt.get_cmap('afmhot'),
    norm=plt.Normalize(
        -1.5,
        3))
ax.add_collection(line)
title = ax.text(-0.11, 0.0, '', fontsize=50, transform=ax.transAxes)
caption1 = ax.text(-0.11,
                   1.1,
                   'Global land/sea surface temperature anomaly (1880-2017)',
                   fontsize=25,
                   transform=ax.transAxes)
caption2 = ax.text(-0.11,
                   1.025,
                   'data: http://data.giss.nasa.gov/gistemp\n'
                   'code: https://github.com/wvangeit/ClimateTunnel',
                   fontsize=10,
                   transform=ax.transAxes)

circle_r = numpy.zeros(50)
circle_theta = 2.0 * numpy.pi * numpy.linspace(0, 1, len(circle_r))
ax.plot(circle_theta, circle_r, 'k')
ax.set_ylim([-1.5, 1.5])
ax.set_xticks(2.0 * numpy.pi * numpy.linspace(0, 1, 12, endpoint=False))
ax.set_xticklabels(['Jan',
                    'Feb',
                    'Mar',
                    'Apr',
                    'May',
                    'Jun',
                    'Jul',
                    'Aug',
                    'Sep',
                    'Oct',
                    'Nov',
                    'Dec'], fontsize=20)
ax.set_yticks([-1.5, 1.5])
ax.set_yticklabels(['-1.5 C', '+1.5 C'], fontsize=20)

def init():
    """Init"""

    line.set_segments([])
    title.set_text('')
    return line, title


def animate(t):
    """Animate"""

    if t < len(years):
        ys = []
        xs = []

        rs = numpy.array([])
        thetas = numpy.array([])

        print years[t]
        for row in range(t + 1):
            r = data[row][1:13]
            rs = numpy.append(rs, r)

            yt = data[row][1:13]
            ys.append(yt)

            x = range(len(yt))
            xs.append(x)

            theta = 2.0 * numpy.pi * \
                numpy.linspace(0, 1, len(r), endpoint=False)
            thetas = numpy.append(thetas, theta)

        points = numpy.array([thetas, rs]).T.reshape(-1, 1, 2)
        segments = numpy.concatenate([points[:-1], points[1:]], axis=1)

        title.set_text(str(years[t]))
        line.set_segments(segments)
        line.set_array(rs)
        marker.set_data(thetas, rs)

    return line, title

ani = animation.FuncAnimation(
    fig,
    animate,
    numpy.arange(
        0,
        len(data) +
        50),
    init,
    interval=len(data),
    blit=False,
    repeat=False)

ani.save('gifs/climate.gif', dpi=80, writer='imagemagick')
# plt.show()
