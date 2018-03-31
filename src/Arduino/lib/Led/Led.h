/*
  Led.h - knihovna pro pro stmívání LED
*/

#ifndef LED_H
#define LED_H

#include "Arduino.h"

/** Zpoždení v ms po jednotlivých krocích stmívání.
 *  Čím je hodnota vyšší, tí déle bude trvat přechod mezi intenzitami osvětlení při volání metody setDim.
 */
#define C_DIM_DELAY 50 

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
   * Pokud je světlo vypnuté, pouze se nastaví hodnota, která se použije připříštím spuštění, jinak dojde ke změně intenzity osvětlení.
   * Změna intenzity je provedena plynule.
   * @param intensity - Intenzita osvětlení, rozsah 0-255, hodnota 0 odpovídá vypnuté LED, hodnota 255 je maximální intenzita světla.
   */
  void setDim(byte intensity);
private:
	//nastaví intnzity na zadanou úroveň
	void dim(byte intensity);
  //číslo pinu pro ovládání LED
  int m_pin;
  //aktualní hodnota intenzity osvětlení
  byte m_currIntensity;
	//předchozí hodnota intenzity osvětlení, nastaví se při volání metody on
	byte m_lastIntensity;
	
	bool m_isOn;  
};

#endif