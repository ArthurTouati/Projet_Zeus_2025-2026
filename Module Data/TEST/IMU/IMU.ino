#include <Adafruit_BNO08x.h>
#include <Adafruit_Sensor.h>

Adafruit_BNO085 bno085;

float roll, pitch, yaw;
float speed_x, speed_y, speed_z;
float x, y, z;
float time = 0.5;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  if (!bno085.begin_I2C()) {
    Serial.println("Failed to find BNO085 chip");
    while (1) { delay(10); }
  }
  Serial.println("BNO085 Found!");

  // Enable rotation vector, accelerometer, and linear acceleration
  bno085.enableRotationVector();
  bno085.enableAccelerometer();
  bno085.enableLinearAcceleration();

  // Initialize position to 0
  x = 0;
  y = 0;
  z = 0;
}

void loop() {
  sensors_event_t orientationData, accelerometerData, linearAccelData;

  if (bno085.getSensorEvent(&orientationData, &accelerometerData, &linearAccelData)) {

    // Rotation vector to Euler angles (roll, pitch, yaw)
    roll = atan2(2.0f * (orientationData.orientation.w * orientationData.orientation.x + orientationData.orientation.y * orientationData.orientation.z),
                 1.0f - 2.0f * (orientationData.orientation.x * orientationData.orientation.x + orientationData.orientation.y * orientationData.orientation.y));
    pitch = asin(2.0f * (orientationData.orientation.w * orientationData.orientation.y - orientationData.orientation.z * orientationData.orientation.x));
    yaw = atan2(2.0f * (orientationData.orientation.w * orientationData.orientation.z + orientationData.orientation.x * orientationData.orientation.y),
                1.0f - 2.0f * (orientationData.orientation.y * orientationData.orientation.y + orientationData.orientation.z * orientationData.orientation.z));

    // Convert radians to degrees
    roll *= RAD_TO_DEG;
    pitch *= RAD_TO_DEG;
    yaw *= RAD_TO_DEG;

    // Linear acceleration (speed change)
    speed_x += linearAccelData.acceleration.x * time; // Assuming loop runs every 100ms
    speed_y += linearAccelData.acceleration.y * time;
    speed_z += linearAccelData.acceleration.z * time;

    // Position integration (simple Euler integration)
    x += speed_x * time;
    y += speed_y * time;
    z += speed_z * time;

    // Print the data
    Serial.print("Roll: "); Serial.print(roll); Serial.print(" degrees  ");
    Serial.print("Pitch: "); Serial.print(pitch); Serial.print(" degrees  ");
    Serial.print("Yaw: "); Serial.print(yaw); Serial.println(" degrees");

    Serial.print("Speed X: "); Serial.print(speed_x); Serial.print(" m/s  ");
    Serial.print("Speed Y: "); Serial.print(speed_y); Serial.print(" m/s  ");
    Serial.print("Speed Z: "); Serial.print(speed_z); Serial.println(" m/s");

    Serial.print("X: "); Serial.print(x); Serial.print(" m  ");
    Serial.print("Y: "); Serial.print(y); Serial.print(" m  ");
    Serial.print("Z: "); Serial.print(z); Serial.println(" m");

    Serial.println("-------------------------------------");

    delay(500); // Adjust delay as needed
  }
}
