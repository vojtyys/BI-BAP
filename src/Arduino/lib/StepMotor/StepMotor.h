/* ========================================================================== */
/*                                                                            */
/*   StepMotor.h                                                              */
/*                                                                            */
/*                                                                            */
/*   Knihovna pro ovládání krokového motoru                                   */
/*                                                                            */
/* ========================================================================== */


#ifndef STEPMOTOR_H
#define STEPMOTOR_H

#include "Arduino.h"
/** Rychlost otáčení, čím vyšší, tím je otáčení motoru pomalejší, nejnižší možná hodnota je 1
 */
#define SPEED 1
/** Třída obsahující metody kontrolující krokový motor.
 */
class StepMotor{
public:
  /** Konstruktor, inicializuje piny pro ovládání motoru.
   * @param pin1 Číslo prvního kontrolního pinu, nutné připojit na IN1.
   * @param pin2 Číslo druheho kontrolního pinu, nutné připojit na IN2.
   * @param pin3 Číslo třetího kontrolního pinu, nutné připojit na IN3.
   * @param pin4 Číslo čtvrtého kontrolního pinu, nutné připojit na IN4.
   */
  StepMotor(int pin1,
	          int pin2,
						int pin3,
						int pin4);
	/** Metoda pro pohnutí motoru o zadaný úhel.
	 * Úhel může být kladný i záporný, podle znaménka se určí směr otáčení.
	 * @param ang - Úhel otočení motoru.
	 */
	void moveAngle(int ang);
	
	/** Metoda pro otočení motoru o zadaný počet otáček.
	 * Jedna otáčka odpovídá 360°. Počet může být kladný i záporný, znamnko určí směr otáčení.
	 * @param nRotation - Počet otáček.
	 */
	void moveRotation(int nRotation);
private:
  //čísla ovládacích pinů
  int m_pin1;
  int m_pin2;
  int m_pin3;
  int m_pin4;
  
  //metody související s vykonáním kroku motoru
  void step1();
  void step2();
  void step3();
  void step4();
  void step5();
  void step6();
  void step7();
  void step8();
  void move();
  void moveOpposite();

};






#endif
