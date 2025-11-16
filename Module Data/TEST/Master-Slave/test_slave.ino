#include <Wire.h>

// --- Configuration ---
#define I2C_SLAVE_ADDR 0x08  // The I2C address for this ESP32
#define SDA_PIN 8            // CHANGE TO YOUR SDA PIN
#define SCL_PIN 9            // CHANGE TO YOUR SCL PIN
#define MAX_STRING_LEN 20    // Our new fixed buffer size

// --- Global Variables ---
// 'volatile' is important
volatile char dataBuffer[MAX_STRING_LEN];
unsigned long lastUpdateTime = 0;
const long updateInterval = 2000; // 2 seconds

// Your four messages
const char* messages[] = {
  "Polution-OK",
  "Polution-N-OK",
  "Meteo-OK",
  "Meteo-N-OK"
};
int currentMessageIndex = 0;

/**
 * @brief Updates the data buffer with the next message.
 */
void updateMessage() {
  // Get the next message
  const char* message = messages[currentMessageIndex];
  
  // CRITICAL: Clear the entire buffer with nulls
  memset((void*)dataBuffer, 0, MAX_STRING_LEN);
  
  // Copy the message into the buffer. 
  // The buffer is now "Meteo-OK\0\0\0\0\0..."
  strncpy((char*)dataBuffer, message, MAX_STRING_LEN - 1);

  Serial.print("Set buffer to: ");
  Serial.println((char*)dataBuffer);

  // Move to the next message index
  currentMessageIndex = (currentMessageIndex + 1) % 4; // 4 messages total
}

/**
 * @brief I2C Event Handler: Called when the Master (Jetson) requests data.
 */
void requestEvent() {
  // Send the entire fixed-size buffer (20 bytes)
  Wire.write((const uint8_t*)dataBuffer, MAX_STRING_LEN);
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("ESP32-C3 I2C Slave (Variable String)");

  // Set the initial message
  updateMessage();
  
  Serial.println("Attempting to start I2C...");
  if (!Wire.begin(I2C_SLAVE_ADDR)) {
    Serial.println("Failed to join I2C bus as slave. Halting.");
    while(1); 
  }
  
  Serial.println("I2C Started Successfully.");
  Wire.onRequest(requestEvent);
  Serial.println("Setup complete.");
}

void loop() {
  // Use millis() for non-blocking timer
  unsigned long currentTime = millis();
  if (currentTime - lastUpdateTime >= updateInterval) {
    lastUpdateTime = currentTime;
    updateMessage(); // Update the buffer with the next message
  }
  
  delay(10); // Small delay
}