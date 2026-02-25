#include "ZeusData.h"
#include "ReseauZeus.h"
#include "ZeusHardware.h"

#define PIN_SERVO 2
#define PIN_JACK 10
#define PIN_BUZZER 3
#define PIN_BUTTON_PARA 0
#define PIN_LED_LAUNCH 4
#define PIN_LED_ACTUATOR 1
#define TIME_FOR_LANDING 251
#define MON_ID 1

uint8_t mac_sequenceur[] = {0xA8, 0x46, 0x74, 0x47, 0xB4, 0xB8};
uint8_t mac_data[] = {0xA0, 0x85, 0xE3, 0xAE, 0x63, 0xC8};
//uint8_t mac_payload[] = {};

ReseauZeus network;
ZeusHardware hardware(PIN_SERVO,PIN_JACK,PIN_BUZZER,PIN_BUTTON_PARA,PIN_LED_LAUNCH,PIN_LED_ACTUATOR);
volatile bool flagLaunch = false;
volatile bool flagButton = false;
volatile unsigned long lastTimeButton = 0;
volatile unsigned long lastTimeJack = 0;
const unsigned long debounceTime = 200;
unsigned long previousMillis = 0;
const long interval = 5000;

void IRAM_ATTR handleLaunchInterrupt() {
  unsigned long now = millis();
  if (now - lastTimeJack > debounceTime) {
    flagLaunch = true;
    flagButton = false; 
    lastTimeJack = now;
  }
}

void IRAM_ATTR handleButtonInterrupt() {
  if (flagLaunch == true) {
    return; 
  }

  unsigned long now = millis();
  if (now - lastTimeButton > debounceTime) {
    flagButton = true;
    lastTimeButton = now;
  }
}

void setup() {
  Serial.begin(115200);
  delay(2000);
  hardware.begin();
  attachInterrupt(digitalPinToInterrupt(PIN_BUTTON_PARA), handleButtonInterrupt, FALLING);
  attachInterrupt(digitalPinToInterrupt(PIN_JACK), handleLaunchInterrupt, RISING);

  if(hardware.isLaunch()){
    flagLaunch = true;
    flagButton = false; 
  }
}

void loop(){
  if (flagLaunch) {
    hardware.launch_done();
    chronologie(); 
    flagLaunch = false; 
  }
  else{
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      Serial.println("Waiting...");
    }
  }

  if (flagButton) {
    if (!flagLaunch) {
      flagButton = false;
      hardware.openParaGround();
    }
  }
}

void chronologie(){
  delay(abs(hardware.getTimeForApogee()*1000 - 5500));
  hardware.openParachute();

  float current_time = 0;
  float max_delay = abs(TIME_FOR_LANDING - 7 - hardware.getTimeForApogee());

  while (current_time < max_delay){
    hardware.descent();
    current_time += 1.1;
  }
  Serial.println("---- End of flight ----");
}