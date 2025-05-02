#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <LittleFS.h>

Adafruit_MPU6050 mpu;

#define FORMAT_LITTLEFS_IF_FAILED true

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!mpu.begin()) {
    Serial.println("Não foi possível encontrar o MPU6050");
    while (1);
  }
  Serial.println("MPU6050 encontrado!");

  if (!LittleFS.begin(FORMAT_LITTLEFS_IF_FAILED)) {
    Serial.println("Erro ao montar LittleFS");
    return;
  }

  File file = LittleFS.open("/dados_mpu.txt", FILE_WRITE);
  if (file) {
    file.println("ax,ay,az,gx,gy,gz");
    file.close();
  }
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  Serial.printf("Acel: %.2f, %.2f, %.2f | Giro: %.2f, %.2f, %.2f\n",
                a.acceleration.x, a.acceleration.y, a.acceleration.z,
                g.gyro.x, g.gyro.y, g.gyro.z);

  File file = LittleFS.open("/dados_mpu.txt", FILE_APPEND);
  if (file) {
    file.printf("%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n",
                a.acceleration.x, a.acceleration.y, a.acceleration.z,
                g.gyro.x, g.gyro.y, g.gyro.z);
    file.close();
  }

  delay(100);
}
