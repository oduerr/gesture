import matplotlib.pyplot as plt
import numpy as np
import warnings
import math

from quaternion_utils import quart_to_ypr

class Plotter:

    def __init__(self, name='Unnamed'):
        self.fig = plt.figure(figsize=(10, 6))
        self.fig.canvas.manager.set_window_title(name)

        self.ax = plt.axes(projection='3d')
        # Set the labels for the axes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        # Rotate the viewport
        self.axis_setrange()
        plt.show(block=False)
        self.qtext = self.fig.text(0, 0.95, s='', fontsize=12,ha='left', va='top')
        self.atext = self.fig.text(0, 0.9, s='', fontsize=12,ha='left', va='top')
        self.gtext = self.fig.text(0, 0.85, s='', fontsize=12,ha='left', va='top')
        self.mtext = self.fig.text(0, 0.8, s='', fontsize=12,ha='left', va='top')
        self.ttext = self.fig.text(0, 0.7 , s='', fontsize=12,ha='left', va='bottom')
        self.ytext = self.fig.text(0, 0.05, s='', fontsize=12,ha='left', va='bottom')

    @staticmethod
    def qm(quaternion1, quaternion0):
        w0, x0, y0, z0 = quaternion0
        w1, x1, y1, z1 = quaternion1
        return np.array([-x1 * x0 - y1 * y0 - z1 * z0 + w1 * w0,
                         x1 * w0 + y1 * z0 - z1 * y0 + w1 * x0,
                         -x1 * z0 + y1 * w0 + z1 * x0 + w1 * y0,
                         x1 * y0 - y1 * x0 + z1 * w0 + w1 * z0], dtype=np.float64)

    def axis_setrange(self):
        #self.ax.view_init(elev=46, azim=61, roll=0) good for yaw experiment
        self.ax.view_init(elev=30, azim=-80)
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_zlim(-1, 1)

    def set_text(self, q, a=None, w=None, m=None, ypr=None, time=None):
        ypr_q = 360 * quart_to_ypr(q) / (2 * math.pi)
        self.qtext.set_text('q = ({:.2f}, {:.2f}, {:.2f}, {:.2f}) ypr[Deg] = ( {:.1f}, {:.1f}, {:.1f})'.format(q[0],q[1],q[2],q[3], ypr_q[0], ypr_q[1], ypr_q[2]))
        if (a is not None):
            a = a / 16384.0 #In Units of g when resulution to +- 2g
            self.atext.set_text('a[g] = ({:.2f}, {:.2f}, {:2f}) ||a||={:.2f}'.format(a[0],a[1],a[2], np.sqrt(np.sum(a**2))))
        if (w is not None):
            w = w / 131. #See MPU-6000/MPU-6050 Product Specification
            self.gtext.set_text('w    = ({:.2f}, {:.2f}, {:2f}) ||g||={:.2f}'.format(w[0], w[1], w[2], np.sqrt(np.sum(w ** 2))))
        if (m is not None):
            m = m #TODO Check product specification
            self.mtext.set_text('m    = ({:.2f}, {:.2f}, {:2f}) ||g||={:.2f}'.format(m[0],m[1],m[2], np.sqrt(np.sum(m**2))))
        if (ypr is not None):
            ypr = 360 * ypr / (2*math.pi)
            self.ytext.set_text('ypr (from lib)    = ({:.2f}, {:.2f}, {:2f})'.format(ypr[0],ypr[1],ypr[2]))
        if (time is not None):
            self.ttext.set_text('time [sec] : {}'.format(time / 1000))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        #print(self.ax.elev, " ", self.ax.azim)

    def show_coordinate(self, q, DIR_IS_LAB_TO_IMU = False):
        q_n = np.sqrt(np.sum(q**2))
        if (np.abs((q_n -1) > 1e-3)):
            warnings.warn("Not a unit quaternion ||q||{}".format(q_n), category=UserWarning, stacklevel=2)
        q /= np.sqrt(np.sum(q**2))
        self.ax.clear()

        if DIR_IS_LAB_TO_IMU:
            qt = q
            q = np.array([q[0], -q[1], -q[2], -q[3]])
        else:
            qt = np.array([q[0], -q[1], -q[2], -q[3]])
        #No q is going from IMU to Lab

        #The unit vectors the in coordinate space of the body
        ex = np.asarray((0, 1, 0, 0))
        ey = np.asarray((0, 0, 1, 0))
        ez = np.asarray((0, 0, 0, 1))

        #Transformation to the lab space
        ex_lab = self.qm(self.qm(q, ex), qt)
        ey_lab = self.qm(self.qm(q, ey), qt)
        ez_lab = self.qm(self.qm(q, ez), qt)

        # Plot the sphere with a translucent surface (many thanks to chatGPT)
        # Generate data for the sphere
        u, v = np.mgrid[0:2 * np.pi:40j, 0:np.pi:20j]
        r = 0.99 #So that they are slightly off
        x = r * (np.cos(u) * np.sin(v))
        y = r * (np.sin(u) * np.sin(v))
        z = r * np.cos(v)
        self.ax.plot_surface(x, y, z, alpha=0.1, color='gray')

        # Plot the  unit vectors
        # Define the origin
        if False:
            o = [0, 0, 0]
            d = 1
            self.ax.quiver(o[0], o[1], o[2], d*ex[1], d*ex[2], d*ex[3], color='r', arrow_length_ratio=0.1, linewidth=0.5)
            self.ax.quiver(o[0], o[1], o[2], d * ey[1], d * ey[2], d * ey[3], color='y', arrow_length_ratio=0.1,
                           linewidth=0.5)
            self.ax.quiver(o[0], o[1], o[2], d * ez[1], d * ez[2], d * ez[3], color='b', arrow_length_ratio=0.1,
                           linewidth=0.5)


        # Plot the transformend unit vectors
        # Define the origin
        o = [0, 0, 0]
        self.ax.quiver(o[0], o[1], o[2], ex_lab[1], ex_lab[2], ex_lab[3], color = 'r', arrow_length_ratio=0.1, linewidth=2)
        self.ax.quiver(o[0], o[1], o[2], ey_lab[1], ey_lab[2], ey_lab[3], color = 'y', arrow_length_ratio=0.1, linewidth=2)
        self.ax.quiver(o[0], o[1], o[2], ez_lab[1], ez_lab[2], ez_lab[3], color = 'b', arrow_length_ratio=0.1, linewidth=2)

        # Plot the projection to the xy plane
        if False:
            # Define the vector to be plotted
            v = ex_lab[1:4]
            # Define the normal vector of the plane
            n = np.array([0, 0, 1])
            # Find the projection of v onto the plane
            v_projection = v - (v.dot(n)) * (n / np.linalg.norm(n) ** 2)
            # Plot the projection of the vector onto the plane
            self.ax.quiver(0, 0, 0, *v_projection, color='red', label='Projection onto plane')
            # Define the points on the plane
            x = np.linspace(-2, 2, 50)
            y = np.linspace(-2, 2, 50)
            X, Y = np.meshgrid(x, y)
            Z = -(X * n[0] + Y * n[1]) / n[2]
            Z = Z - 1
            # Plot the plane
            self.ax.plot_surface(X, Y, Z, alpha=0.5)

        #self.set_text(q)
        self.axis_setrange()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        # Show the plot

if __name__ == '__main__':
    q = np.asarray([0.15,  0.41,  0.05, -0.9])
    quart_to_ypr(q)
    from plot_quaternion import Plotter
    plotter = Plotter('IMU 2')
    # Just dummy values
    q = np.asarray([0.69, 0.32, -0.05, -0.65])
    a = 16384 * np.asarray([0.9805807, 0.1961161, 0.0000000])
    w = np.asarray([0.9805807, 0.1961161, 0.0000000, 0.0000000])
    m  = np.asarray([0.9805807, 0.1961161, 0.0000000, 0.0000000])
    ypr = np.asarray([0.9805807, 0.1961161, 0.0000000])

    plotter.show_coordinate(q) #Shows the quaternion
    while True:
        plotter.set_text(q, a=a, w=w, m=m, ypr=ypr) #shows addition
        # Delay for 0.5 seconds
        import time
        time.sleep(0.1)
    input("Press any key to continue...")