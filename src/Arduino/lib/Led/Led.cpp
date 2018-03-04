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
Led::on() {
  digitalWrite(m_pin, HIGH);  //zapnutí LED
}

//------------------------------------------------------------------------------
Led::off() {
  digitalWrite(m_pin, LOW);  //vypnutí LED
}

//------------------------------------------------------------------------------
Led::setDim(byte intensity) {  //pokud se změní hodnota stmívání, je intenzita osvětlení plynule upravena na novou úroveň
  if (intesity < m_currIntensity) {
    for (byte i = m_currIntensity; i < intensity; ++i){
      analogWrite(m_pin, i);
      delay(C_DIM_DELAY);      //zpoždění kvůli plynulosti
    }
    m_currIntensity = intensity;
  } else if (intensity > m_currIntensity) {
    for (byte i = m_currIntensity; i > intensity; --i){
      analogWrite(m_pin, i);
      delay(C_DIM_DELAY);
    }
    m_currIntensity = intensity;
//==============================================================================
}