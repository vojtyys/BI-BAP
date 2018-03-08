/* ========================================================================== */
/*                                                                            */
/*   StepMotor.cpp                                                            */
/*                                                                            */
/*                                                                            */
/*   Implementační soubor knihvny pro ovládání krokového motoru               */
/*                                                                            */
/* ========================================================================== */


#include "Arduino.h"
#include "StepMotor.h"
//Kód byl převzat a upraven z http://navody.arduino-shop.cz/navody-k-produktum/krokovy-motor-a-driver.html
//==============================================================================

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

//------------------------------------------------------------------------------
StepMotor::StepMotor(int pin1,
                     int pin2,
										 int pin3,
										 int pin4)
{
  m_pin1 = pin1;
  m_pin1 = pin2;
  m_pin1 = pin3;
  m_pin1 = pin4;
  
  pinMode(m_pin1, OUTPUT);
  pinMode(m_pin2, OUTPUT);
  pinMode(m_pin3, OUTPUT);
  pinMode(m_pin4, OUTPUT);
}

//------------------------------------------------------------------------------
void StepMotor::moveAngle(int ang)
{
  if (ang > 0) {
	  for (int i = 0; i < (ang * 64 / 45); ++i) {  //360° odpovídá podle výrobce 512 krokům motoru, 1° tedy odpovídá 64/45 krokům
		  move();
		}
	} else if (ang < 0) {
	  for (int i = 0; i < (-ang * 64 / 45); ++i){
		  moveOpposite();
		}
	} 
}

//------------------------------------------------------------------------------
void StepMotor::moveRotation(int nRotation)
{
  if (nRotation > 0) {
	  for (int i = 0; i < nRotation * 512; ++i) {  //otočení o 360° odpovídá 512 krokům motoru
		  move();
		}
	} else if (nRotation < 0) {
	  for (int i = 0; i < -nRotation * 512; ++i) {
		  moveOpposite();
		}
	}
}

//------------------------------------------------------------------------------
//sekvence příkazů dané výrobcem pro provdení jednoho kroku
void step1(){
  digitalWrite(m_pin1, HIGH);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void step2(){
  digitalWrite(m_pin1, HIGH);
  digitalWrite(m_pin2, HIGH);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void step3(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, HIGH);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void step4(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, HIGH);
  digitalWrite(m_pin3, HIGH);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void step5(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, HIGH);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void step6(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, HIGH);
  digitalWrite(m_pin4, HIGH);
  delay(SPEED);
}
void step7(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, HIGH);
  delay(SPEED);
}
void step8(){
  digitalWrite(m_pin1, HIGH);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, HIGH);
  delay(SPEED);
}

//------------------------------------------------------------------------------
//sekvence příkazů pro krok motoru
void move() {
  step1();
  step2();
  step3();
  step4();
  step5();
  step6();
  step7();
  step8();
}

//------------------------------------------------------------------------------
//sekvence příkazů pro krok motoru na opačnou stranu
void moveOposit() {
  step8();
  step7();
  step6();
  step5();
  step4();
  step3();
  step2();
  step1();
}
//==============================================================================