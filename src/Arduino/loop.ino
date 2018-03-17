#include <FastCRC.h>


#define EN 2
#define ADDR 1
#define CMDLEN 7
#define RX 10
#define TX 11
FastCRC16 CRC16;
uint8_t cnt = 0;
void setup() {
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  Serial.begin(9600);
  //Serial1.begin(9600);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);
}

enum State { // <-- the use of typedef is optional
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
      //Serial.println("Waiting for cmd");
      if (Serial.available()) {
        if (Serial.readBytes(cmd, CMDLEN) != CMDLEN) {
          next_state = WAIT;
         // Serial.println("Incorrect len of cmd");
        } else {
          /*Serial.print("CMD: ");
          Serial.print(cmd[0], HEX);
          Serial.print(" ");
          Serial.print(cmd[1], HEX);
          Serial.print(" ");
          Serial.print(cmd[2], HEX);
          Serial.print(" ");
          Serial.print(cmd[3], HEX);
          Serial.print(" ");
          Serial.print(cmd[4], HEX);
          Serial.print(" ");
          Serial.print(cmd[5], HEX);
          Serial.print(" ");
          Serial.println(cmd[6], HEX);*/
          next_state = CHECK;

          //delay(500);
        }
      }
      //delay(500);
      break;

    case CHECK:
      if (cmd[0] != ADDR) {
        //Serial.println("Address invalid");
        next_state = WAIT;
      } else if (!checkCRC(cmd)) {
        //Serial.println("CRC invalid");
        next_state = WAIT;
      } else if (cmd[1] != cnt) {
        //Serial.println("Redundant CMD");
        sendAck();
        next_state = WAIT;
      } else {
        sendAck();
        cnt++;
        next_state = RUN;
      }
      break;

    case RUN:
      //Serial.println("Running commands");
      digitalWrite(13, HIGH);
      delay(500);
      digitalWrite(13, LOW);
      next_state = WAIT;
      break;
  }
  curr_state = next_state;
}

bool checkCRC(byte cmd[CMDLEN]) {
  uint8_t buff[CMDLEN - 2];
  for (int i = 0; i < CMDLEN - 2; ++i) {
    buff[i] = cmd[i];
  }
  uint16_t tmp = (cmd[CMDLEN - 2] << 8) | cmd[CMDLEN - 1];
  if (CRC16.ccitt(buff, sizeof(buff)) != tmp) {
    return false;
  } else {
    return true;
  }

}

void sendAck() {
  delay(500);
  uint8_t ack[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x11, 0x0C }; //ack with CRC
  digitalWrite(EN, HIGH);
  Serial.write(ack, sizeof(ack));
  Serial.flush();
  digitalWrite(EN, LOW);
  
  //Serial.println("ACK");
}



