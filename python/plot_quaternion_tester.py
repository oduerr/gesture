import numpy as np
import time
import quaternion

from plot_quaternion import Plotter
from quaternion_utils import DONT_USE_quart_to_ypr_aduino


def replay_file():
    import pandas as pd
    fn = 'value-TestQuat.csv'
    fn = 'value-TestYaw.csv'
    df = pd.read_csv('~/Google Drive/_HTWG/Sabatical WS 2022/Gesture_Recognition/data/second_version/{}'.format(fn),sep=',')
    plotter = Plotter(fn)
    #plotter2 = Plotter('Q Inver')
    # df = pd.read_csv('~/Google Drive/_HTWG/Sabatical WS 2022/Gesture_Recognition/data/second_version/value-nomove.csv', sep=',')
    df = df.rename(columns={df.columns[0]: 'IMU'})
    # Limit to certain IMU
    df = df[df['IMU'] == 4].reset_index(drop=True)
    print(df.shape)
    Q = df[['q1', 'q2', 'q3', 'q4']].to_numpy()
    start_time_in_video = 17.0 #Starting time in video
    clock = time.time()
    s = df.loc[df['time'] > 5000].index[0]
    print(s)
    print(Q[s])
    plotter.show_coordinate(Q[s])
    plotter.set_text(Q[s], time=df.loc[s, 'time'])
    for i in range(s, df.shape[0] - 1):
        # bottom_text
        accel = np.array([df.loc[i, 'accel_x'], df.loc[i, 'accel_y'], df.loc[i, 'accel_z']])
        w = np.array([df.loc[i, 'gyro_x'], df.loc[i, 'gyro_y'], df.loc[i, 'gyro_z']])
        ypr = np.array((df.loc[i, 'yaw'], df.loc[i, 'pitch'],  df.loc[i, 'roll']))
        # show_coordinate([0.86169383, 0.02081877, -0.5058515, 0.03412598])
        plotter.show_coordinate(Q[i])
        plotter.set_text(Q[i], a=accel, w=w, ypr=ypr, time = df.loc[i, 'time'])
        #plotter2.show_coordinate(Q[i],  DIR_IS_LAB_TO_IMU = False)
        #plotter2.set_text(Q[i], a=accel, w=w, ypr=ypr, time = df.loc[i, 'time'])
        time_in_animation = (df.loc[i+1, 'time'] - df.loc[i, 'time']) / 1000
        delta_rel = time.time() - clock
        dsec = (time_in_animation - delta_rel)#Need to wait
        if (dsec > 0):
            print('Sleeping for {}'.format(dsec))
            time.sleep(dsec)
            clock = time.time()



def plot_kown_quanternions():
    plotter = Plotter('Testing Quaterionons')

    q1 = np.array((1., 0., 0., 0.))
    plotter.show_coordinate(q1)
    plotter.set_text(q1)
    input("Press any key to continue...")

    r = np.array((0,0,1))
    yaw = 30 * 2 * np.pi / 360.
    s = np.sin(yaw/2)
    q1 = np.quaternion(np.cos(yaw/2), s*r[0],s*r[1],s*r[2])
    q_np = np.array((q1.w, q1.x, q1.y, q1.z))
    plotter.show_coordinate(q_np)
    plotter.set_text(q=q_np, ypr=DONT_USE_quart_to_ypr_aduino(q_np))
    input("Press any key to continue...")

    r = np.array((0, 1, 0))
    #A negative value corresponds to take off
    pitch = -35 * 2 * np.pi / 360.
    s = np.sin(pitch / 2)
    q2 = np.quaternion(np.cos(pitch / 2), s * r[0], s * r[1], s * r[2])
    q_np = np.array((q2.w, q2.x, q2.y, q2.z))
    plotter.show_coordinate(q_np)
    plotter.set_text(q=q_np, ypr=DONT_USE_quart_to_ypr_aduino(q_np))
    input("Press any key to continue...")

    r = np.array((1, 0, 0))
    roll = 10 * 2 * np.pi / 360.
    s = np.sin(roll / 2)
    q3 = np.quaternion(np.cos(roll / 2), s * r[0], s * r[1], s * r[2])
    q_np = np.array((q3.w, q3.x, q3.y, q3.z))
    plotter.show_coordinate(q_np)
    plotter.set_text(q=q_np, ypr=DONT_USE_quart_to_ypr_aduino(q_np))
    input("Press any key to continue...")

    q4 = (q1*q2)*q3
    q_np = np.array((q4.w, q4.x, q4.y, q4.z))
    plotter.show_coordinate(q_np)
    plotter.set_text(q=q_np, ypr=DONT_USE_quart_to_ypr_aduino(q_np))
    input("Press any key to continue...")







if __name__ == '__main__':
    #replay_file()
    plot_kown_quanternions()