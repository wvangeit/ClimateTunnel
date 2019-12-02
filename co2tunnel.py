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


import ftplib
ftp = ftplib.FTP('aftp.cmdl.noaa.gov')
ftp.login()
ftp.cwd('/products/trends/co2/')


csv_filename = 'co2_mm_gl.txt'
csv_path = os.path.join(data_dir, csv_filename)
csv_file = open(csv_path, 'wb')

ftp.retrbinary('RETR ' + csv_filename, csv_file.write)

data = numpy.genfromtxt(
    csv_path,
    filling_values=[float('nan')])
years = [int(y[0]) for y in data]

fig = plt.figure(figsize=(9, 9))

ax = fig.add_subplot(1, 1, 1, projection='polar')

marker, = ax.plot([], [], '.', alpha=.3, ms=10, mfc='black')
line = collections.LineCollection(
    [],
    linewidth=10,
    alpha=.2,
    cmap=plt.get_cmap('afmhot'),
    norm=plt.Normalize(
        300,
        500))
ax.add_collection(line)
title = ax.text(-0.11, 0.0, '', fontsize=50, transform=ax.transAxes)
caption1 = ax.text(-0.11,
                   1.1,
                   'Global CO2 concentration anomaly in ppm (1980-)',
                   fontsize=20,
                   transform=ax.transAxes)
caption2 = ax.text(-0.11, 1.05,
                   'data: Ed Dlugokencky and Pieter Tans, NOAA/ESRL '
                   '(www.esrl.noaa.gov/gmd/ccgg/trends/) \n'
                   'code: https://github.com/wvangeit/ClimateTunnel',
                   fontsize=7, transform=ax.transAxes)

circle_r = numpy.zeros(50)
circle_theta = 2.0 * numpy.pi * numpy.linspace(0, 1, len(circle_r))
ax.plot(circle_theta, circle_r, 'k')

ax.set_ylim([320, 420])
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
ax.set_yticks([320, 420])
ax.set_yticklabels(['320', '420'], fontsize=20)


def init():
    """Init"""

    line.set_segments([])
    title.set_text('')
    return line, title


frame_filenames = []


def animate(t):
    """Animate"""

    if t < len(years):
        rs = numpy.array([])
        thetas = numpy.array([])

        year = years[t]

        for it in range(t):
            r = data[it][3]
            rs = numpy.append(rs, r)

            theta = 2.0 * numpy.pi * ((it % 12) / 12)
            thetas = numpy.append(thetas, theta)

        points = numpy.array([thetas, rs]).T.reshape(-1, 1, 2)
        segments = numpy.concatenate([points[:-1], points[1:]], axis=1)

        title.set_text(str(year))
        line.set_segments(segments)
        line.set_array(rs)
        marker.set_data(thetas, rs)

    frame_filename = os.path.join("frames", "%d.png" % t)
    frame_filenames.append(frame_filename)
    plt.savefig(frame_filename)
    return line, title


ani = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=len(data) + 10,
    blit=True,
    repeat=False)

print("Saving co2 gif ...")
ani.save(
    'gifs/co2.gif',
    dpi=60,
    fps=10,
    writer='imagemagick')
