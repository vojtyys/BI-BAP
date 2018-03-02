/*
  relay.cpp - implementační soubor pro knihovnu ovládající relé
*/

#include "Arduino.h"
#include "Relay.h"
//==============================================================================
Relay::Relay(int pin){
  m_pin = pin;
  pinMode(m_pin, OUTPUT);    //nastavení pinu jako výtupu
  digitalWrite(m_pin, HIGH); //relé je vypnuté v HIGH
}

//------------------------------------------------------------------------------
void Relay::on(){
  digitalWrite(m_pin, LOW);
}

//------------------------------------------------------------------------------
void Relay::off(){
  digitalWrite(m_pin, HIGH);
}
//==============================================================================