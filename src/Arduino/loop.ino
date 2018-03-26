#include <Wire.h>
#include <dht.h>
#include <StepMotor.h>
#include <Relay.h>
#include <Led.h>
#include <FastCRC.h>
//#include <SoftwareSerial.h>


#define EN 2
#define ADDR 10
#define CMDLEN 8
#define LED 13
#define RX 10
#define TX 11
#define HYST 1

//SoftwareSerial RS(RX, TX);
FastCRC16 CRC16;
Led light(3);
Relay socket(4);
Relay boiler(5);
StepMotor window(6, 7, 8, 9);
dht12 DHT(0x5c);


uint8_t cnt;
bool gTempEn;
bool gBoilerIsOn;
byte gTempSet;

unsigned long time;
unsigned long curr_time;

bool isResetCmd(uint8_t cmd[CMDLEN]);
void checkBoiler();

enum State {
  WAIT,
  CHECK,
  RUN
};

byte cmd[CMDLEN];

State curr_state;
State next_state;


void setup() {
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  Serial.begin(9600);
  //Serial1.begin(9600);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);
  //RS.begin(9600);
  cnt = 0;
  gTempEn = false;
  gBoilerIsOn = false;
  curr_state = WAIT;
  next_state = WAIT;
  time = 0;
}


void loop() {
  switch (curr_state) {
    case WAIT:
      curr_time = millis();
      if (curr_time - time > 30000) {
        if (gTempEn) {
          checkBoiler();
        }
        time = millis();
      }
      if (Serial.available()) {
        if (Serial.readBytes(cmd, CMDLEN) != CMDLEN) {
          next_state = WAIT;
        } else {
          next_state = CHECK;
        }
      }
      break;

    case CHECK:
      if (cmd[0] != ADDR) {
        next_state = WAIT;
      } else if (!checkCRC(cmd)) {
        next_state = WAIT;
      } else if (cmd[1] != cnt) {
        if (isResetCmd(cmd)) {
          cnt = 0;
        }
        sendAck(cmd[1]);
        next_state = WAIT;
      } else {
        sendAck(cnt);
        cnt++;
        next_state = RUN;
      }
      break;

    case RUN:
      switch (cmd[2]) {
        case 0: //reset
          if  (isResetCmd(cmd)) {
            cnt = 0;
          }
          break;
        case 1:  //light
          switch (cmd[3]) {
            case 0:  //on
              light.on();
              break;

            case 1: //off
              light.off();
              break;

            case 2: //dim
              light.setDim(cmd[4]);
          }
          break;

        case 2: //socket
          switch (cmd[3]) {
            case 0:  //on
              socket.on();
              break;

            case 1: //off
              socket.off();
              break;
          }
          break;

        case 3:  //boiler
          switch (cmd[3]) {
            case 0: //teplota
              gTempSet = float(cmd[4]);
              break;
            case 1:  //zap
              gTempEn = true;
              gBoilerIsOn = false;
              break;
            case 2: //vyp
              gTempEn = false;
              gBoilerIsOn = false;
              boiler.off();
              break;
          }
          break;

        case 4: //window
          /*switch (cmd[3]) {
              //TODO
            }*/
          break;

        case 5: //led
          switch (cmd[3]) {
            case 0:
              digitalWrite(LED, HIGH);
              break;
            case 1:
              digitalWrite(LED, LOW);
              break;
          }
          break;

        default:
          for (int i = 0; i < 5; i++) {
            digitalWrite(LED, HIGH);
            delay(100);
            digitalWrite(LED, LOW);
            delay(100);
          }
          break;
      }
      next_state = WAIT;
      break;
  }
  curr_state = next_state;
}

uint16_t getCRC(byte * cmd, int len) {
  return CRC16.ccitt(cmd, len);
}

bool checkCRC(byte cmd[CMDLEN]) {
  byte buff[CMDLEN - 2];
  for (int i = 0; i < CMDLEN - 2; ++i) {
    buff[i] = cmd[i];
  }
  uint16_t tmp = (cmd[CMDLEN - 2] << 8) | cmd[CMDLEN - 1];
  if (getCRC(buff, sizeof(buff)) != tmp) {
    return false;
  } else {
    return true;
  }

}



void sendAck(uint8_t ackCnt) {
  delay(100);
  uint8_t ack[CMDLEN];
  ack[0] = 0x00;  //adresa ridici jednotky
  ack[1] = ackCnt;  //cislo potvrzovaneho ramce
  ack[2] = 0x00;   //ACK
  ack[3] = ADDR;
  ack[4] = 0x00;
  ack[5] = 0x00;
  uint16_t crc = getCRC(ack, 6);
  ack[6] = (crc & 0xFF00) >> 8;  //pripojeni CRC
  ack[7] = (crc & 0x00FF);
  digitalWrite(EN, HIGH);
  Serial.write(ack, sizeof(ack));
  Serial.flush();
  digitalWrite(EN, LOW);
}

bool isResetCmd(uint8_t cmd[CMDLEN]) {
  return (cmd[2] == 0x00 && cmd[3] == 0x00 && cmd[4] == 0x00 && cmd[5] == 0x00);
}

void checkBoiler() {
  DHT.read();
  float temp = DHT.getTemperature() / 10.0;
  if (gBoilerIsOn) { //kotel je zapnuty, vypne, kdyz teplota presahne nastavenou teplotu + hystereze
    if (temp > (gTempSet + HYST)) {
      boiler.off();
      gBoilerIsOn = false;
    }
  } else { //kotel je vypnuty, zapne se, pokud teplota klesne pod nastavenou teplotu minus hystereze
    if (temp < (gTempSet - HYST)) {
      boiler.on();
      gBoilerIsOn = true;
    }
  }
}




