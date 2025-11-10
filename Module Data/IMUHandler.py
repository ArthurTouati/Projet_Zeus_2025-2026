from adafruit_bno08x import  BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER, BNO_REPORT_ROTATION_VECTOR, BNO_REPORT_LINEAR_ACCELERATION
from adafruit_bno08x.i2c import BNO08X_I2C
from scipy.spatial.transform import Rotation

class IMUHandler:
    def __init__(self,i2c):
        # Accelerometer :
        self.ax = []
        self.ay = []
        self.az = []

        # Gyroscope :
        self.gx = []
        self.gy = []
        self.gz = []

        # Magnetometer :
        self.mx = []
        self.my = []
        self.mz = []

        # Quaternion :
        self.qi = []
        self.qj = []
        self.qk = []
        self.qr = []

        # Rotation :
        self.roll = []
        self.pitch = []
        self.yaw = []

        # Export dict :
        self.header = ['ax','ay','az','gx','gy','gz','mx','my','mz','qi','qj','qk','qreal','roll','pitch','yaw']
        self.imu_dict = dict.fromkeys(self.header)

        # Init sensor
        self.sensor = BNO08X_I2C(i2c)
        self.sensor.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)
        self.sensor.enable_feature(BNO_REPORT_GYROSCOPE)
        self.sensor.enable_feature(BNO_REPORT_MAGNETOMETER)
        self.sensor.enable_feature(BNO_REPORT_ROTATION_VECTOR)
        print("BNO085 init done !")

    def read_data(self):
        # Extract data from the sensor
        ax,ay,az = self.sensor.linear_acceleration
        gx,gy,gz = self.sensor.gyro
        mx,my,mz = self.sensor.magnetic
        qi,qj,qk,qr = self.sensor.quaternion

        # Store data into list
        self.ax.append(ax)
        self.ay.append(ay)
        self.az.append(az)
        self.gx.append(gx)
        self.gy.append(gy)
        self.gz.append(gz)
        self.mx.append(mx)
        self.my.append(my)
        self.mz.append(mz)
        self.qi.append(qi)
        self.qj.append(qj)
        self.qk.append(qk)
        self.qr.append(qr)

        # Transform quaternion into roll, pitch, yaw
        r = Rotation([qi, qj, qk, qr])
        euler_angle = r.as_euler('zyx', degrees=True)
        self.roll.append(euler_angle[0])
        self.pitch.append(euler_angle[1])
        self.yaw.append(euler_angle[2])

    def export_to_dict(self):
        # Add each list into the dictionary
        self.imu_dict['ax'] = self.ax
        self.imu_dict['ay'] = self.ay
        self.imu_dict['az'] = self.az
        self.imu_dict['gx'] = self.gx
        self.imu_dict['gy'] = self.gy
        self.imu_dict['gz'] = self.gz
        self.imu_dict['mx'] = self.mx
        self.imu_dict['my'] = self.my
        self.imu_dict['mz'] = self.mz
        self.imu_dict['qi'] = self.qi
        self.imu_dict['qj'] = self.qj
        self.imu_dict['qk'] = self.qk
        self.imu_dict['qreal'] = self.qr
        self.imu_dict['roll'] = self.roll
        self.imu_dict['pitch'] = self.pitch
        self.imu_dict['yaw'] = self.yaw

        # Export dictionary
        return self.imu_dict

    def clear_dict(self):
        self.imu_dict.clear()

        # Clear all list
        self.ax.clear()
        self.ay.clear()
        self.az.clear()
        self.gx.clear()
        self.gy.clear()
        self.gz.clear()
        self.mx.clear()
        self.my.clear()
        self.mz.clear()
        self.qi.clear()
        self.qj.clear()
        self.qk.clear()
        self.qr.clear()
        self.roll.clear()
        self.pitch.clear()
        self.yaw.clear()

        print("Dictionary is clear !")