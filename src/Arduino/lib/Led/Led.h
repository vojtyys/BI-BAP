/*
  Led.h - knihovna pro pro stmívání LED
*/

#ifndef LED_H
#define LED_H

#include "Arduino.h"

/** Zpoždení v ms po jednotlivých krocích stmívání.
 *  Čím je hodnota vyšší, tí déle bude trvat přechod mezi intenzitami osvětlení při volání metody setDim.
 */
#define C_DIM_DELAY 100 

/** Třída sloužící k ovládání stmívání LED.
 */
class Led{
public:
  /** Vytoří instanci třídy Led.
   * @param pin - Číslo pinu pro ovládání stmívání LED, musí podporovat PWM.
   */
  Led(int pin);
  
  /** Metoda pro zapnutí LED s maximálním jasem.
   */
  void on();
  
  /** Metoda pro vypnutí LED.
   */
  void off();
  
  /** Metoda pro nastavení intenzity stmívání LED.
   * Změna intenzity je provedena plynule.
   * @param intensity - Intenzita osvětlení, rozsah 0-255, hodnota 0 odpovídá vypnuté LED, hodnota 255 je maximální intenzita světla.
   */
  void setDim(byte intensity);
private:
  //číslo pinu pro ovládání LED
  int m_pin;
  //aktualní hodnota intenziti osvětlení
  byte m_currIntensity;    
};

#endif