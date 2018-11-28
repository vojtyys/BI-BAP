#include <SoftwareSerial.h>
#define RX 10
#define TX 11
#define OE 3
#define LED 13
#define ADDR 2
#define BR 9


//
SoftwareSerial RS485(RX, TX);
char recByte;
enum states {WAIT_ID, CHCK_ID, ACTION};
states state = WAIT_ID;
states nextState = WAIT_ID;

bool checkID() {
  String tmp(recByte);
  return tmp.toInt() == ADDR || tmp.toInt() == BR;
}

void ledOn() {
  digitalWrite(LED, HIGH);
}

void ledOff() {
  digitalWrite(LED, LOW);
}

void setup() {
  Serial.begin(9600);
  RS485.begin(9600);
  pinMode(OE, OUTPUT);
  digitalWrite(OE, LOW);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
}

void loop() {
  switch (state) {
    case WAIT_ID:
      //Serial.println("Awaiting ID");
      if (RS485.available()) {
        do {
          recByte = RS485.read();
        } while (!isDigit(recByte));
        Serial.print("Got ID: ");
        Serial.println(recByte);
        nextState = CHCK_ID;
      }
      break;

    case CHCK_ID:
      if (checkID()) {
        nextState = ACTION;
        Serial.println("ID OK");
      } else {
        nextState = WAIT_ID;
        Serial.println("ID NOK");
      }
      do {
        recByte = RS485.read();
      } while (!isDigit(recByte));
      break;

    case ACTION:
      Serial.print("Got code: ");
      Serial.println(recByte);
      String tmp(recByte);
      if (tmp.toInt() == 1) {
        ledOn();
      } else if (tmp.toInt() == 0) {
        ledOff();
      }
      nextState = WAIT_ID;
      break;
  }
  state = nextState;
}
