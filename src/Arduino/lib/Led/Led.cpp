/*
Led.cpp - Implementační soubor knihovny pro ovládání LED.
*/

#include "Arduino.h"
#include "Led.h"

//==============================================================================
Led::Led(int pin) {
  m_pin = pin;                //nastavení čísla pinu
  m_currIntensity = 0;        //intenzita světla je na počátku 0
  pinMode(m_pin, OUTPUT);     //nastavení pinu jako výstup
  digitalWrite(m_pin, LOW);   //led je na začátku vypnutá
}

//------------------------------------------------------------------------------
void Led::on() {
  digitalWrite(m_pin, HIGH);  //zapnutí LED
  m_currIntensity = 255;      //intenzita je maximální
}

//------------------------------------------------------------------------------
void Led::off() {
  digitalWrite(m_pin, LOW);  //vypnutí LED
  m_currIntensity = 0;       //intenzita je nulová
}

//------------------------------------------------------------------------------
void Led::setDim(byte intensity) {  //pokud se změní hodnota stmívání, je intenzita osvětlení plynule upravena na novou úroveň
  if (intensity < m_currIntensity) {
    for (int i = m_currIntensity; i >= intensity; --i){
      analogWrite(m_pin, i);
      delay(C_DIM_DELAY);      //zpoždění kvůli plynulosti
    }
    m_currIntensity = intensity;
  } else if (intensity > m_currIntensity) {
    for (int i = m_currIntensity; i < intensity; ++i){
      analogWrite(m_pin, i);
      delay(C_DIM_DELAY);
    }
    m_currIntensity = intensity;
  }
}
//==============================================================================