#ifndef ZEUS_HARDWARE_H
#define ZEUS_HARDWARE_H

#include <Arduino.h>
#include <Preferences.h>
#include <ESP32Servo.h>

#define FREQUENCY_SERVO 50
#define MIN_PULSE_SERVO 500
#define MAX_PULSE_SERVO 2400
#define INIT_POS_SERVO 0
#define OPEN_POS_SERVO 90
#define LED_BLINK 100
#define SERVO_OPEN_TIME 500
#define BUZ_FREQUENCY_TEST 500


class ZeusHardware {
  private:
    //Sequenceur pin
      const int pinParachute;
      const int pinJack;
      const int pinBuzzer;
      const int pinButtonPara;
      const int pinLedLaunch;
      const int pinLedActuator;
    
    //Object
    Servo servoPara;
    Preferences prefSeq;

    //Constant
    float timeForApogee;
    unsigned long timerLaunch;
    bool launch;

    void printTestMessage(const __FlashStringHelper* component, int duration) {
      Serial.print(F("Testing ")); 
      Serial.print(component);
      Serial.print(F("... (Active for "));
      Serial.print(duration);
      Serial.println(F(" ms)"));
    }

    void testHardware() {
      // --- Test LEDs ---
      printTestMessage(F("LEDs"), LED_BLINK);
      delay(500); 
      digitalWrite(pinLedLaunch, HIGH);
      digitalWrite(pinLedActuator, HIGH);
      delay(LED_BLINK);
      digitalWrite(pinLedLaunch, LOW);
      digitalWrite(pinLedActuator, LOW);

      // --- Test Servo ---
      printTestMessage(F("Servo"), SERVO_OPEN_TIME);
      delay(500); 
      servoPara.write(OPEN_POS_SERVO);
      delay(SERVO_OPEN_TIME);
      servoPara.write(INIT_POS_SERVO);

      // --- Test Buzzer ---
      printTestMessage(F("Buzzer"), LED_BLINK);
      delay(500);
      tone(pinBuzzer, BUZ_FREQUENCY_TEST);
      delay(LED_BLINK);
      noTone(pinBuzzer);
      
      // Final cooldown
      delay(500);
  }

  public:
    ZeusHardware(int pinP, int pinJ, int pinB, int pinBP, int pinLL, int pinLA) : pinParachute(pinP), pinJack(pinJ), pinBuzzer(pinB), pinButtonPara(pinBP), pinLedLaunch(pinLL), pinLedActuator(pinLA){
      timerLaunch = 0;
      launch = false;
      timeForApogee = 0.0;
    }

    void begin(){
      // Init Hardware
      pinMode(pinJack,INPUT_PULLUP);
      pinMode(pinBuzzer,OUTPUT);
      pinMode(pinLedLaunch,OUTPUT);
      pinMode(pinLedActuator,OUTPUT);
      pinMode(pinButtonPara,INPUT_PULLUP);

      // Init servomotor
      servoPara.setPeriodHertz(FREQUENCY_SERVO);
      servoPara.attach(pinParachute,MIN_PULSE_SERVO,MAX_PULSE_SERVO);
      servoPara.write(INIT_POS_SERVO);

      // Init Memory (NVS)
      prefSeq.begin("zeus_config", false);
      timeForApogee = prefSeq.getFloat("valeur_zeus", 20.1);
        
      Serial.print("Valeur chargée : ");
      Serial.println(timeForApogee);

      delay(500);

      // Test Hardware (Optional)
      testHardware();

      Serial.println("--- End of initialization, ready to launch ---");
      digitalWrite(pinLedLaunch, HIGH);
    }

    void saveNewApogee(float val) {
        // On n'écrit en mémoire flash QUE si la valeur est différente (pour préserver la durée de vie)
        if (abs(val - timeForApogee) > 0.001) { 
            timeForApogee = val;
            prefSeq.putFloat("valeur_zeus", val);
            Serial.println("Mémoire Flash mise à jour !");
        }
    }

    float getTimeForApogee() { 
        return timeForApogee; 
    }

    void openParachute(){
      Serial.println("Opening parachute...");
      // Total excecution time : 3s
      for (int i = 0; i < 3; i += 1){
        tone(pinBuzzer, 200);
        digitalWrite(pinLedActuator, HIGH);
        delay(100);
        digitalWrite(pinLedActuator, LOW);
        noTone(pinBuzzer);
        delay(300); 
      }
      digitalWrite(pinLedActuator, HIGH);
      servoPara.write(OPEN_POS_SERVO);
      delay(600);
      digitalWrite(pinLedActuator, LOW);
      for (int i = 0; i < 3; i += 1){
        tone(pinBuzzer, 200);
        digitalWrite(pinLedActuator, HIGH);
        delay(100);
        digitalWrite(pinLedActuator, LOW);
        noTone(pinBuzzer);
        delay(300); 
      }
      servoPara.write(INIT_POS_SERVO);
      Serial.println("Parachute déployé !");
    }

    void launch_done(){
      // Total excecution time : 4s
      digitalWrite(pinLedLaunch, LOW);
      for (int i = 0; i < 20; i += 1){
        tone(pinBuzzer, 600);
        delay(100);
        noTone(pinBuzzer);
        delay(100); 
      }
      Serial.println("Lancement effectué !");
    }

    void descent(){
      // Total excecution time : 1.1s
      tone(pinBuzzer, 800);
      delay(100);
      noTone(pinBuzzer);
      delay(1000); 
    }

    bool isLaunch(){
      return digitalRead(pinJack) == HIGH;
    }

    bool isButtonPressed(){
      return digitalRead(pinButtonPara) == LOW;
    }

    void openParaGround(){
      Serial.println("Opening parachute...");
      servoPara.write(OPEN_POS_SERVO);
      delay(2000);
      servoPara.write(INIT_POS_SERVO);
    }
};

#endif