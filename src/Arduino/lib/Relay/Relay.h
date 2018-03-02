/*
  Relay.h - knihovna pro zapínaní a vypínaní relé.
*/

#ifndef Relay_h
#define Relay_h

#include "Arduino.h"

class Relay {
public:
  /**  Konstruktor
   *   @param pin Číslo pinu pro spínaní
   */
  Relay(int pin);
  
  /**Funkce k sepnutí relé.
   */
  void on();
  
  /** Funkce k vypnutí relé
   */
  void off();
private:
  int m_pin; //číslo pinu pro ovládání relé  
}

#endif