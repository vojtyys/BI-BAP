#include <Wire.h>
#include <BH1750.h>
#include <dht.h>
#include <Relay.h>
#include <Led.h>
#include <FastCRC.h>




//adresa univerzáního modulu, každý modul musí mít unikátní adresu
#define ADDR 1
//délka CMD v B
#define CMDLEN 8

//pin pro ovládání výstupu na RS485
#define EN 2
//LED dioda na desce pro testovací CMD Led
#define LED 13

//piny pro čtení okenních dorazů
#define WINDOW_IS_OPEN 9
#define WINDOW_IS_CLOSED 10

//piny pro tlačítka ovládající světlo 1
#define LIGHT_1_BTN_ON A0
#define LIGHT_1_BTN_OFF A1

//piny pro tlačítka ovládající okno
#define WIN_BTN_OPEN A2
#define WIN_BTN_CLOSE A3


//Nastavení hystereze pro ovládání kotle. Topení se vypne při dosažení nastavené teploty + HYST. Topeni se zapne při poklesu pod stanovenou teplotu - HYST.
#define HYST 1

//práh intenzity osvětlení v luxech pro automatické zapnutí osvětlení
#define LUX_TRESHOLD 50


//inicializace CRC
FastCRC16 CRC16;

//inicializace světelného senzoru
BH1750 lightSensor;

//inicializace teploměru
dht12 DHT(0x5c);

//inicializace ovládaných zařízení
//osvětlení
Led light1(3);
Led light2(5);

//zásuvky
Relay socket1(4);
Relay socket2(6);
Relay socket3(11);
Relay socket4(13);

//okno
Relay windowOpen(7);
Relay windowClose(8);

//topení
Relay boiler(12);

//globální proměnné

//číslo paketu
uint8_t cnt = 0;

//časy pro periodické spouštění řídícího cyklu
unsigned long lastTime = 0;
unsigned long currTime = 0;

//čas pro periodické čtení senzorů
unsigned long lastMeasTime = 0;

//řízení osvětlení

//světlo 1
byte currDim1 = 0;  //aktuální hodnota stmívání
byte targetDim1 = 0; //cílová hodnota stmívání
byte lastDim1 = 255;  //hodnota stmívání používaná při zapnutí světel
unsigned long light1OnTime = 0; //čas za jak dlouho má dojít k zapnutí
unsigned long light1OffTime = 0; //čas za jak dlouho má dojít k vypnutí
unsigned long light1OnStartTime = 0; //čas přijetí příkazu k časovému zapnutí - k výpočtu času vypnutí spolu s light1OnTime
unsigned long light1OffStartTime = 0; //čas přijetí příkazu k časovému vypnutí - k výpočtu času vypnutí spolu s light1Of
bool light1TimeOnEn = false; //časové zapnutí povoleno/zakázáno
bool light1TimeOffEn = false; //časové vypnutí povoleno/zakázáno
bool light1AutoOnEn = false; //automatické zapnutí podle úrovně osvětlení povoleno/zakázáno
bool dim1En = false; //stmívání povoleno/zakázáno - není povoleno při vypnutém světle, díky tomu lze nastavit cílovou hodnotu stmívání aniž by se světlo zapnulo
bool light1On = false; //světlo je zapnuté/vypnuté

//světlo 2 analogicky
byte currDim2 = 0;
byte targetDim2 = 0;
byte lastDim2 = 255;
unsigned long light2OnTime = 0;
unsigned long light2OffTime = 0;
unsigned long light2OnStartTime = 0;
unsigned long light2OffStartTime = 0;
bool light2TimeOnEn = false;
bool light2TimeOffEn = false;
bool light2AutoOnEn = false;
bool dim2En = false;
bool light2On = false;


//řízení zásuvek

//zásuvka 1
unsigned long socket1OnTime = 0; //čas za jak dlouho má dojít k sepnutí zásuvky
unsigned long socket1OffTime = 0; //čas, za jak dlouho má dojít k vypnutí zásuvky
unsigned long socket1OnStartTime = 0; //čas přijetí příkazu k časovému zapnutí
unsigned long socket1OffStartTime = 0; //čas přijetí příkazu k časovému vypnutí
bool socket1TimeOnEn = false; //časové zapnutí povoleno/zakázáno
bool socket1TimeOffEn = false; //časové vypnutí povoleno/zakázáno

//zásuvka 2 analogicky jako 1
unsigned long socket2OnTime = 0;
unsigned long socket2OffTime = 0;
unsigned long socket2OnStartTime = 0;
unsigned long socket2OffStartTime = 0;
bool socket2TimeOnEn = false;
bool socket2TimeOffEn = false;

//zásuvka 3 analogicky jako 1
unsigned long socket3OnTime = 0;
unsigned long socket3OffTime = 0;
unsigned long socket3OnStartTime = 0;
unsigned long socket3OffStartTime = 0;
bool socket3TimeOnEn = false;
bool socket3TimeOffEn = false;

//zásuvka 4 analogicky jako 1
unsigned long socket4OnTime = 0;
unsigned long socket4OffTime = 0;
unsigned long socket4OnStartTime = 0;
unsigned long socket4OffStartTime = 0;
bool socket4TimeOnEn = false;
bool socket4TimeOffEn = false;

//řízení okna
bool winIsOpening = false; //určuje, zda je okno právě otevíráno nebo ne
bool winIsClosing = false; //určuje, zda je okno právě zavíráno nebo ne

//řízení kotle
float temp = 0; //nastavená teplota
bool boilerTempEn = false; //udržování teploty zapnuto/vypnuto
bool boilerIsOn = false; //kotel je právě zapnutý/vypnutý

//pole pro přijímání příkazů
byte cmd[CMDLEN];

//definice stavů
enum State {
  CHECK_BUS,
  CHECK_CMD,
  DECODE,
  RUN
};


//aktuální a příští stav
State currState;
State nextState;


//deklarace funkcí
//funkce pro detekování reset příkazu
bool isResetCmd(uint8_t cmd[CMDLEN]);

//kontrola nutnosti sepnutí nebo vypnutí kotle
void checkBoiler();

//kontrola automatického zapnutí světel
void checkLight(int which);

//získání crc z pole bytů
uint16_t getCRC(byte * cmd, int len);

//kontrola CRC přijaté zprávy
bool checkCRC(byte cmd[CMDLEN]);

//kontrola stisku tlačítka
bool isPressed(int button);




void setup() {
  //nastavení pinů pro tlačítka jako vstup
  pinMode(LIGHT_1_BTN_ON, INPUT_PULLUP);
  pinMode(LIGHT_1_BTN_OFF, INPUT_PULLUP);

  pinMode(WIN_BTN_OPEN, INPUT_PULLUP);
  pinMode(WIN_BTN_CLOSE, INPUT_PULLUP);

  //nastavení pinů pro dorazy okna
  pinMode(WINDOW_IS_OPEN, INPUT);
  pinMode(WINDOW_IS_CLOSED, INPUT);

  //inicializace světelného senzoru
  lightSensor.begin();

  //inicializace komunikace po sběrnici
  Serial.begin(9600);
  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);

  currState = CHECK_BUS;
  nextState = CHECK_BUS;

}


void loop() {
  switch (currState) {
    case CHECK_BUS:
      //kontrola příchozích dat

      if (Serial.available()) {
        if (Serial.readBytes(cmd, CMDLEN) != CMDLEN) {
          nextState = RUN;
        } else {
          nextState = CHECK_CMD;
        }
      }  else {
        nextState = RUN;
      }
      break;

    case RUN:
      //periodická kontrola tlačítek a provádění akcí jednou za 50 ms a senzorů jednou za 30 s
      currTime = millis();
      if (currTime - lastTime > 50) {
        //kontola, jestli nějaké zařízení nemá být automaticky spuštěno
        //zapnutí světla 1
        if (light1TimeOnEn) {
          if (currTime - light1OnStartTime >= light1OnTime) {
            light1TimeOnEn = false;
            targetDim1 = lastDim1;
            dim1En = true;
          }
        }

        //vypnutí světla 1
        if (light1TimeOffEn) {
          if (currTime - light1OffStartTime >= light1OffTime) {
            light1TimeOffEn = false;
            targetDim1 = 0;
            dim1En = true;
          }
        }

        //zapnutí světla 2
        if (light2TimeOnEn) {
          if (currTime - light2OnStartTime >= light2OnTime) {
            light2TimeOnEn = false;
            targetDim2 = lastDim2;
            dim2En = true;
          }
        }

        //vypnutí světla 2
        if (light2TimeOffEn) {
          if (currTime - light2OffStartTime >= light2OffTime) {
            light2TimeOffEn = false;
            targetDim2 = 0;
            dim2En = true;
          }
        }

        //změna stmívání světla 1
        if (dim1En) {
          if (currDim1 < targetDim1) {
            currDim1++;
          } else if (currDim1 > targetDim1) {
            currDim1--;
          } else {
            dim1En = false;
          }
          light1.setDim(currDim1);
          if (currDim1 == 0) {
            light1On = false;
          }

        }

        //změna stmívání světla 2
        if (dim2En) {
          if (currDim2 < targetDim2) {
            currDim2++;
          } else if (currDim2 > targetDim2) {
            currDim2--;
          } else {
            dim2En = false;
          }
          light2.setDim(currDim2);
          if (currDim2 == 0) {
            light2On = false;
          }
        }


        //zapnutí zásuvky 1
        if (socket1TimeOnEn) {
          if (currTime - socket1OnStartTime >= socket1OnTime) {
            socket1TimeOnEn = false;
            socket1.on();
          }
        }

        //vypnutí zásuvky 1
        if (socket1TimeOffEn) {
          if (currTime - socket1OffStartTime >= socket1OffTime) {
            socket1TimeOffEn = false;
            socket1.off();
          }
        }

        //zapnutí zásuvky 2
        if (socket2TimeOnEn) {
          if (currTime - socket2OnStartTime >= socket2OnTime) {
            socket2TimeOnEn = false;
            socket2.on();
          }
        }

        //vypnutí zásuvky 2
        if (socket2TimeOffEn) {
          if (currTime - socket2OffStartTime >= socket2OffTime) {
            socket2TimeOffEn = false;
            socket2.off();
          }
        }

        //zapnutí zásuvky 3
        if (socket3TimeOnEn) {
          if (currTime - socket3OnStartTime >= socket3OnTime) {
            socket3TimeOnEn = false;
            socket3.on();
          }
        }

        //vypnutí zásuvky 3
        if (socket3TimeOffEn) {
          if (currTime - socket3OffStartTime >= socket3OffTime) {
            socket3TimeOffEn = false;
            socket3.off();
          }
        }

        //zapnutí zásuvky 4
        if (socket4TimeOnEn) {
          if (currTime - socket4OnStartTime >= socket4OnTime) {
            socket4TimeOnEn = false;
            socket4.on();
          }
        }

        //vypnutí zásuvky 4
        if (socket4TimeOffEn) {
          if (currTime - socket4OffStartTime >= socket4OffTime) {
            socket4TimeOffEn = false;
            socket4.off();
          }
        }

        //kontrola stisku tlačítka

        //světlo 1 on tlačítko
        if (isPressed(LIGHT_1_BTN_ON)) {
          targetDim1 = currDim1;
          if (targetDim1 < 255) {
            targetDim1++;
            lastDim1 = targetDim1;
            dim1En = true;
          }
          light1On = true;
        }

        //světlo 1 off tlačítko
        if (isPressed(LIGHT_1_BTN_OFF)) {
          targetDim1 = currDim1;
          if (targetDim1 > 0) {
            lastDim1 = targetDim1; //ponechání alespon 1, pokud dojde k úplnému vypnutí, aby při zapnutí světlo opravdu svítilo
            targetDim1--;
            dim1En = true;
          }
        }

        //otevírací tlačítko okna
        if (isPressed(WIN_BTN_OPEN)) {
          if (!isPressed(WINDOW_IS_OPEN)) { //pokud už je světlo otevřené, neděje se nic
            winIsClosing = false; //případná změna ze zavírání na otevírání
            windowClose.off();

            winIsOpening = true;
            windowOpen.on();
          }
        }

        //zavírací tlačítko okna
        if (isPressed(WIN_BTN_CLOSE)) {
          if (!isPressed(WINDOW_IS_CLOSED)) { //pokud už je okno zavřené, neděje se nic
            winIsOpening = false;  //případná změna z otvírání na zavírání
            windowOpen.off();

            winIsClosing = true;
            windowClose.on();
          }
        }

        //kontrola dorazů okna

        //okno se otevřelo
        if (isPressed(WINDOW_IS_OPEN)) {
          winIsOpening = false;
          windowOpen.off();
        }

//okno se zavřelo
        if (isPressed(WINDOW_IS_CLOSED)) {
          winIsClosing = false;
          windowClose.off();
        }

        //aktualizace posledního času spuštění smyčky
        lastTime = millis();
      }

      //smyčka pro měření 
      if (currTime - lastMeasTime > 30000) {
        //kontrola teploty
        if (boilerTempEn) {
          checkBoiler();
        }

        //kontrola intenzity osvětlení
        if (light1AutoOnEn) {
          checkLight(1);
        }
        if (light2AutoOnEn) {
          checkLight(2);
        }

        //aktualizace posledního času měření
        lastMeasTime = millis();
      }
      
      nextState = CHECK_BUS;
      break;
      
    case CHECK_CMD:
      if (cmd[0] != ADDR) {    //kontrola, zda je zpráva určena této jednotce
        nextState = RUN;
      } else if (!checkCRC(cmd)) { //kontrola CRC
        nextState = RUN;
      } else if (cmd[1] != cnt) { //pokud je paket pro tuto jednotku, ale číslo paketu je neočekávané, zkontrolu je se, jestli to není zpráva pro reset číslování zpráv
        if (isResetCmd(cmd)) {
          cnt = 0;
        }
        sendAck(cmd[1]); //odeslání potvrzovacího paketu
        nextState = RUN;
      } else {
        sendAck(cnt); //vše v pořádku, odeslání potvrzovacího paketu, inkrementace čísla paketu
        cnt++;
        nextState = DECODE;
      }
      break;

    case DECODE:   //dekódování přijaté zprávy
      switch (cmd[2]) {
        case 0: //reset
          if  (isResetCmd(cmd)) {
            cnt = 0;
          }
          break;
        case 1:  //světlo 1
          switch (cmd[3]) {
            case 0:  //zapnout 
              targetDim1 = lastDim1; //poslední nastavená hodnota stmívání před vypnutím
              dim1En = true;
              light1On = true;
              break;

            case 1: //vypnutí
              targetDim1 = 0;
              dim1En = true;
              break;

            case 2: //nastavení stmívání
              targetDim1 = cmd[4];
              cmd[4] == 0 ? lastDim1 = currDim1 : lastDim1 = targetDim1;  //nastavení poslední hodnoty stmívání pro obnovení po zapnutí
              if (light1On) {
                dim1En = true;
              }
              break;

            case 3: //časové sepnutí
              light1TimeOnEn = true;
              light1OnTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              light1OnStartTime = millis();
              break;

            case 4: //časové vypnutí
              light1TimeOffEn = true;
              light1OffTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              light1OffStartTime = millis();
              break;

            case 5: //automatické zapnutí podle intenzity osvětlení
              light1AutoOnEn = true;
              break;

            case 6: //zrušení automatických a časovývh naplánovaných akcí
              light1AutoOnEn = false;
              light1TimeOnEn = false;
              light1TimeOffEn = false;
              break;
          }
          break;

        case 2:  //světlo 2
          switch (cmd[3]) {
            case 0:  //zapnutí
              targetDim2 = lastDim2;
              dim2En = true;
              light2On = true;
              break;

            case 1: //vypnutí
              targetDim2 = 0;
              dim2En = true;
              break;

            case 2: //stmívání
              targetDim2 = cmd[4];
              cmd[4] == 0 ? lastDim2 = currDim2 : lastDim2 = targetDim2;
              if (light2On) {
                dim2En = true;
              }
              break;

            case 3: //časové zanutí
              light2TimeOnEn = true;
              light2OnTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              light2OnStartTime = millis();
              break;

            case 4: //časové vypnutí
              light2TimeOffEn = true;
              light2OffTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              light2OffStartTime = millis();
              break;

            case 5: //automatické zapnutí podle intenzity osvětelení
              light2AutoOnEn = true;
              break;

            case 6: //zrušení automatických a časovývh naplánovaných akcí
              light2AutoOnEn = false;
              light2TimeOnEn = false;
              light2TimeOffEn = false;
              break;
          }
          break;

        case 3: //zásuvka 1
          switch (cmd[3]) {
            case 0:  //zapnutí
              socket1.on();
              break;

            case 1: //vypnutí
              socket1.off();
              break;

            case 2: //časové zapnutí
              socket1TimeOnEn = true;
              socket1OnTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              socket1OnStartTime = millis();
              break;

            case 3: //časové vypnutí
              socket1TimeOffEn = true;
              socket1OffTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              socket1OffStartTime = millis();
              break;

            case 4: //zrušení časového zapnutí a vypnutí
              socket1TimeOnEn = false;
              socket1TimeOffEn = false;
              break;
          }
          break;

        case 4: //zásuvka 2
          switch (cmd[3]) {
            case 0:  //zapnutí
              socket2.on();
              break;

            case 1: //vypnutí
              socket2.off();
              break;

            case 2: //časové zapnutí
              socket2TimeOnEn = true;
              socket2OnTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              socket2OnStartTime = millis();
              break;

            case 3: //časové vypnutí
              socket2TimeOffEn = true;
              socket2OffTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              socket2OffStartTime = millis();
              break;

            case 4: //zrušení časového zapnutí a vypnutí
              socket2TimeOnEn = false;
              socket2TimeOffEn = false;
              break;
          }
          break;

        case 5: //zásuvka 3
          switch (cmd[3]) {
            case 0:  //zapnutí
              socket3.on();
              break;

            case 1: //vypnutí
              socket3.off();
              break;

            case 2: //časové zapnutí
              socket3TimeOnEn = true;
              socket3OnTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              socket3OnStartTime = millis();
              break;

            case 3: //časové vypnutí
              socket3TimeOffEn = true;
              socket3OffTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              socket3OffStartTime = millis();
              break;

            case 4: //zrušení časového zapnutí a vypnutí
              socket3TimeOnEn = false;
              socket3TimeOffEn = false;
              break;
          }
          break;

        case 6: //zásuvka 4
          switch (cmd[3]) {
            case 0:  //zapnutí
              socket4.on();
              break;

            case 1: //vypnutí
              socket4.off();
              break;

            case 2: //časové zapnutí
              socket4TimeOnEn = true;
              socket4OnTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              socket4OnStartTime = millis();
              break;

            case 3: //časov vypnutí
              socket4TimeOffEn = true;
              socket4OffTime = (((unsigned long) cmd[4] << 8) | (unsigned long) cmd[5]) * 1000;
              socket4OffStartTime = millis();
              break;

            case 4: //zrušení časového zapnutí a vypnutí
              socket4TimeOnEn = false;
              socket4TimeOffEn = false;
              break;
          }
          break;

        case 7:  //kotel
          switch (cmd[3]) {
            case 0: //nastavení teploty
              temp = float(cmd[4]);
              break;
            case 1:  //zapnutí udržování nastavené teploty
              boilerTempEn = true;
              boilerIsOn = false;
              break;
            case 2: //vypnutí udržování nastavené teploty
              boilerTempEn = false;
              boilerIsOn = false;
              boiler.off();
              break;
          }
          break;

        case 8: //okno
          switch (cmd[3]) {
            case 0://otevírání
              if (!isPressed(WINDOW_IS_OPEN)) { //jen pokud okno není otevřené
                winIsClosing = false;//případná změna směru otevírání/zavírání
                windowClose.off();

                winIsOpening = true;
                windowOpen.on();
              }
              break;

            case 1://zavírání
              if (!isPressed(WINDOW_IS_CLOSED)) {//jen pokud okno není zavřené
                winIsOpening = false; //případná změna směru otevírání/zavírání
                windowOpen.off();

                winIsClosing = true;
                windowClose.on();
              }
              break;
          }
          break;

        default:
          //tuhle zprávu neznám, nic neudělám
          break;
      }
      nextState = RUN;
      break;
  }
  currState = nextState;
}

uint16_t getCRC(byte * cmd, int len) {//získání crc pro pole bytů zadané délky, vrátí vypočítanou CRC hodnotu
  return CRC16.ccitt(cmd, len);
}

bool checkCRC(byte cmd[CMDLEN]) { //kontrola CRC přijatého paketu
  byte buff[CMDLEN - 2];
  for (int i = 0; i < CMDLEN - 2; ++i) {
    buff[i] = cmd[i];
  }
  uint16_t tmp = ((uint16_t) cmd[CMDLEN - 2] << 8) | (uint16_t) cmd[CMDLEN - 1];
  if (getCRC(buff, sizeof(buff)) != tmp) {
    return false;
  } else {
    return true;
  }

}



void sendAck(uint8_t ackCnt) {
  delay(50); //zpoždění, jinak by potvrzovací paket byl odeslán dříve než řídící jednotka stihne shodit nastavení OE pinu, hodnota určena experimentálně
  uint8_t ack[CMDLEN]; //vytvoření potvrzovacího paketu
  ack[0] = 0x00;  //adresa ridici jednotky
  ack[1] = ackCnt;  //cislo potvrzovaneho ramce
  ack[2] = 0x00;   //ACK
  ack[3] = ADDR;
  ack[4] = 0x00;
  ack[5] = 0x00;
  uint16_t crc = getCRC(ack, 6);
  ack[6] = (crc & 0xFF00) >> 8;  //pripojeni CRC
  ack[7] = (crc & 0x00FF);
  digitalWrite(EN, HIGH); //odeslání
  Serial.write(ack, sizeof(ack));
  Serial.flush();
  digitalWrite(EN, LOW);
}

bool isResetCmd(uint8_t cmd[CMDLEN]) { //kontrola, zda jde o příkaz reset
  return (cmd[2] == 0x00 && cmd[3] == 0x00 && cmd[4] == 0x00 && cmd[5] == 0x00);
}

void checkBoiler() {//kontrola kotle - reakce na teplotu
  DHT.read();//měření aktuální teploty
  float measTemp = DHT.getTemperature() / 10.0;
  if (boilerIsOn) { //kotel je zapnuty, vypne, kdyz teplota presahne nastavenou teplotu + hystereze
    if (measTemp > (temp + HYST)) {
      boiler.off();
      boilerIsOn = false;
    }
  } else { //kotel je vypnuty, zapne se, pokud teplota klesne pod nastavenou teplotu - hystereze
    if (measTemp < (temp - HYST)) {
      boiler.on();
      boilerIsOn = true;
    }
  }
}

bool isPressed(int button) { //kontrola stisku tlačítka
  return (digitalRead(button) == LOW);
}
void checkLight(int which) { //kontrola intenzity osvětlení
  uint16_t lux = lightSensor.readLightLevel(); //čtení hodnoty ze senzoru
  if (lux < LUX_TRESHOLD) { //reakce pokud byl překročen práh
    if (which == 1) {
      targetDim1 = lastDim1;
      dim1En = true;
      light1AutoOnEn = false;
    } else if (which == 2) {
      targetDim2 = lastDim2;
      dim2En = true;
      light2AutoOnEn = false;
    }
  }
}

