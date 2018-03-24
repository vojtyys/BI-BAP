#include <StepMotor.h>
#include <Relay.h>
#include <Led.h>
#include <FastCRC.h>


#define EN 2
#define ADDR 10
#define CMDLEN 7
#define LED 13

FastCRC16 CRC16;
Led light(3);
Relay socket(4);
StepMotor window(5, 6, 7, 8);

uint8_t cnt = 0;




void setup() {
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  Serial.begin(9600);
  //Serial1.begin(9600);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);
}

enum State {
  WAIT,
  CHECK,
  RUN
};

byte cmd[CMDLEN];

State curr_state = WAIT;
State next_state = curr_state;
void loop() {
  switch (curr_state) {
    case WAIT:
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
        case 0:  //light
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

        case 1: //socket
          switch (cmd[3]) {
            case 0:  //on
              socket.on();
              break;

            case 1: //off
              socket.off();
              break;
          }
          break;

        case 2:  //boiler
          /*switch (cmd[3]) {
              //TODO
            }*/
          break;

        case 3: //window
          /*switch (cmd[3]) {
              //TODO
            }*/
          break;

        case 4: //led
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
            delay(50);
            digitalWrite(LED, LOW);
            delay(50);
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
  delay(500);
  uint8_t ack[CMDLEN];
  ack[0] = 0x00;  //adresa ridici jednotky
  ack[1] = ackCnt;  //cislo potvrzovaneho ramce
  ack[2] = 0x00;   //ACK
  ack[3] = ADDR;
  ack[4] = 0x00;
  uint16_t crc = getCRC(ack, 5);
  ack[5] = (crc & 0xFF00) >> 8;  //pripojeni CRC
  ack[6] = (crc & 0x00FF);
  digitalWrite(EN, HIGH);
  Serial.write(ack, sizeof(ack));
  Serial.flush();
  digitalWrite(EN, LOW);

}




