import numpy as np

def quart_to_ypr(q_body_2_lab):
    """
        Convert a quaternion representation of rotation from body frame to lab frame to yaw, pitch, roll representation.

        Reference see:
        https://ibrahimcahitozdemir.com/2022/01/08/quaternion-based-ahrs-estimation-using-mpu9250-and-stm32g431/


        Parameters:
        - q_body_2_lab: A 4-element numpy array representing the quaternion in the form [w, x, y, z].

        Returns:
        - A 3-element numpy array representing the yaw, pitch, roll angles in radians.
    """
    w = q_body_2_lab[0]
    x = q_body_2_lab[1]
    y = q_body_2_lab[2]
    z = q_body_2_lab[3]
    roll = np.arctan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch = np.arcsin(2 * (w * y - x * z))
    yaw = np.arctan2(2 * (w * z + x * y), 1 - 2 * (z * z + y * y))
    return np.asarray((yaw, pitch, roll))

#######################################
# Old routines translated e.g. form https://github.com/jrowberg/i2cdevlib/blob/master/Arduino/MPU6050/MPU6050_9Axis_MotionApps41.cpp
# Just for reference
import math

def DONTUSEdmpGetYawPitchRoll(q, gravity):
  qw = q[0]
  qx = q[1]
  qy = q[2]
  qz = q[3]
  yaw = math.atan2(2*qx*qy - 2*qw*qz, 2*qw*qw+2*qx*qx-1)
  pitch = math.atan(gravity[0]/np.sqrt(gravity[1]**2+gravity[2]**2))
  roll = math.atan(gravity[1]/np.sqrt(gravity[0]**2+gravity[2]**2))
  return(np.array((yaw, pitch, roll)))

def dmpGetGravity(q):
  qw = q[0]
  qx = q[1]
  qy = q[2]
  qz = q[3]
  vx = 2 * (qx * qz - qw*qy)
  vy = 2 * (qw * qx + qy*qz)
  vz = qw**2 - qx**2 - qy**2 + qz**2
  return(np.array((vx,vy,vz)))

def DONT_USE_quart_to_ypr_aduino(q_body_2_lab):
    g = dmpGetGravity(q_body_2_lab)
    return DONTUSEdmpGetYawPitchRoll(q_body_2_lab, g)

if __name__ == '__main__':
    import quaternion

    # We yaw around 30 degrees around z-axis
    yaw = 30 * 2 * np.pi / 360.
    r = np.array((0, 0, 1))
    s = np.sin(yaw / 2)
    q1 = np.quaternion(np.cos(yaw / 2), s * r[0], s * r[1], s * r[2])

    # We take-off with 35 Degrees (negative value is nose up) around y
    pitch = -35 * 2 * np.pi / 360.
    r = np.array((0, 1, 0))
    s = np.sin(pitch / 2)
    q2 = np.quaternion(np.cos(pitch / 2), s * r[0], s * r[1], s * r[2])

    # We roll about 10 degrees around x
    r = np.array((1, 0, 0))
    roll = 10 * 2 * np.pi / 360.
    s = np.sin(roll / 2)
    q3 = np.quaternion(np.cos(roll / 2), s * r[0], s * r[1], s * r[2])

    q = (q1*q2)*q3
    print(360/(2*math.pi) * quart_to_ypr(np.array((q.w, q.x, q.y, q.z))))

    q = q1 * (q2 * q3)
    print(360 / (2 * math.pi) * quart_to_ypr(np.array((q.w, q.x, q.y, q.z))))