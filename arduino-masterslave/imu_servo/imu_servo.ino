#include <Wire.h> // I2C通信を行うためのライブラリ
#include <Servo.h> // サーボを動かすためのライブラリ

Servo myservo;  // サーボに名前を付ける

int pos = 0;    // サーボの値を入れる変数（箱）を作り0を入れる。


// MPU-6050のアドレス、レジスタ設定値（モジュールの決まり事）
#define MPU6050_WHO_AM_I     0x75  // Read Only
#define MPU6050_PWR_MGMT_1   0x6B  // Read and Write
#define MPU_ADDRESS  0x68


// 電源投入時に一度だけ実行される
void setup() {
  // I2C通信の開始
  Wire.begin();

  // PCとの通信を開始（データ表示用）
  Serial.begin(19200); //115200bps
 
  // 初回確認処理（接続センサの確認）
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(MPU6050_WHO_AM_I);  //MPU6050_PWR_MGMT_1
  Wire.write(0x00);
  Wire.endTransmission();

  // 動作モードの設定（データの送り方など）
  Wire.beginTransmission(MPU_ADDRESS);
  Wire.write(MPU6050_PWR_MGMT_1);  //MPU6050_PWR_MGMT_1レジスタの設定
  Wire.write(0x00);
  Wire.endTransmission();

  // ピン9番をサーボ用の通信用に設定
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object

  
}

// 電源が入っている限り、繰り返し実行される
void loop() {
  // センサ値の読み込み
  // IMUモジュールと通信を開始し、値を取得する。
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 14, true);
  // データ読み込み
  while (Wire.available() < 14);
  int16_t axRaw, ayRaw, azRaw, gxRaw, gyRaw, gzRaw, TemperatureRaw;

  // 取得した値を用意したそれぞれの変数（箱）に入れる
  axRaw = Wire.read() << 8 | Wire.read();
  ayRaw = Wire.read() << 8 | Wire.read();
  azRaw = Wire.read() << 8 | Wire.read();
  TemperatureRaw = Wire.read() << 8 | Wire.read();
  gxRaw = Wire.read() << 8 | Wire.read();
  gyRaw = Wire.read() << 8 | Wire.read();
  gzRaw = Wire.read() << 8 | Wire.read();
  
  // データの変換（センサのデータシートより）
  // 加速度値を分解能で割って加速度(G)に変換する
  float acc_x = axRaw / 16384.0;  //FS_SEL_0 16,384 LSB / g
  float acc_y = ayRaw / 16384.0;
  float acc_z = azRaw / 16384.0;

  // 角速度値を分解能で割って角速度(度/秒)に変換する
  float gyro_x = gxRaw / 131.0;//FS_SEL_0 131 LSB / (°/s)
  float gyro_y = gyRaw / 131.0;
  float gyro_z = gzRaw / 131.0;

  // 温度の計算。
  float temp = (TemperatureRaw + 12412.0) / 340.0;

  // X加速度（G）の値をサーボ角度指示（度）に変換する
  pos=(acc_x+1.0)*90.0;

  // 結果を（人間が見るために）出力する
  Serial.print(pos);  Serial.print(", ");
  Serial.print(acc_x);  Serial.print(", ");
  Serial.print(acc_y);  Serial.print(", ");
  Serial.print(acc_z);  Serial.print(", ");
  Serial.print(gyro_x); Serial.print(", ");
  Serial.print(gyro_y); Serial.print(", ");
  Serial.print(gyro_z); Serial.print(", ");
  Serial.print(temp); Serial.println("");

  // サーボに角度支持（度）を出す。
  myservo.write(pos);
  
}
