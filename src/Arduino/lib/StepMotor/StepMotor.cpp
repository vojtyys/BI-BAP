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
StepMotor::StepMotor(int pin1,
                     int pin2,
										 int pin3,
										 int pin4)
{
  m_pin1 = pin1;
  m_pin2 = pin2;
  m_pin3 = pin3;
  m_pin4 = pin4;
  
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
//sekvence příkazů dané výrobcem pro provedení jednoho kroku
void StepMotor::step1(){
  digitalWrite(m_pin1, HIGH);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void StepMotor::step2(){
  digitalWrite(m_pin1, HIGH);
  digitalWrite(m_pin2, HIGH);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void StepMotor::step3(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, HIGH);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void StepMotor::step4(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, HIGH);
  digitalWrite(m_pin3, HIGH);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void StepMotor::step5(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, HIGH);
  digitalWrite(m_pin4, LOW);
  delay(SPEED);
}
void StepMotor::step6(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, HIGH);
  digitalWrite(m_pin4, HIGH);
  delay(SPEED);
}
void StepMotor::step7(){
  digitalWrite(m_pin1, LOW);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, HIGH);
  delay(SPEED);
}
void StepMotor::step8(){
  digitalWrite(m_pin1, HIGH);
  digitalWrite(m_pin2, LOW);
  digitalWrite(m_pin3, LOW);
  digitalWrite(m_pin4, HIGH);
  delay(SPEED);
}

//------------------------------------------------------------------------------
//sekvence příkazů pro krok motoru
void StepMotor::move() {
  StepMotor::step1();
  StepMotor::step2();
  StepMotor::step3();
  StepMotor::step4();
  StepMotor::step5();
  StepMotor::step6();
  StepMotor::step7();
  StepMotor::step8();
}

//------------------------------------------------------------------------------
//sekvence příkazů pro krok motoru na opačnou stranu
void StepMotor::moveOpposite() {
  StepMotor::step8();
  StepMotor::step7();
  StepMotor::step6();
  StepMotor::step5();
  StepMotor::step4();
  StepMotor::step3();
  StepMotor::step2();
  StepMotor::step1();
}
//==============================================================================