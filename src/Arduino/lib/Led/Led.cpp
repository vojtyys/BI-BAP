/*
Led.cpp - Implementační soubor knihovny pro ovládání LED.
*/

#include "Arduino.h"
#include "Led.h"

//==============================================================================
Led::Led(int pin) {
  m_pin = pin;                //nastavení čísla pinu
  m_currIntensity = 0;        //intenzita světla je na počátku 0
  m_lastIntensity = 255;      //pokud bude voláno on před dim, rozsvítí se LED úplně
  pinMode(m_pin, OUTPUT);     //nastavení pinu jako výstup
  digitalWrite(m_pin, LOW);   //led je na začátku vypnutá
  m_isOn = false;             //led je na začátku vypnutá
}

//------------------------------------------------------------------------------
void Led::on() {
	Led::dim(m_lastIntensity);  //zapnuti LED na poslední nastavenou hodnotu
	m_isOn = true;              //led je zapnutá
}

//------------------------------------------------------------------------------
void Led::off() {
  Led::dim(0);     //vypnutí led
  m_isOn = false;  //led je vypnutá
}

//------------------------------------------------------------------------------
void Led::setDim(byte intensity) {
	if (m_isOn) {
		Led::dim(intensity);  //pokud je LED zapnutá, změňí intenzitu stmívání
	}
	m_lastIntensity = intensity;  //po zapnutí se nastaví tato úroveň stmívání
}
//------------------------------------------------------------------------------
void Led::dim(byte intensity) {  //pokud se změní hodnota stmívání, je intenzita osvětlení plynule upravena na novou úroveň
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