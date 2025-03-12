#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Controle-Access-Point"; // Access point SSID
const char* password = "Zeus-2025-AT"; // Access point password (at least 8 characters)

WebServer server(80); // Web server on port 80

void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP32 Web Server</h1>";
  html += "<form action='/send' method='POST'>";
  html += "<button type='submit'>Envoyer Bonjour</button>";
  html += "</form>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void handleSend() {
  Serial.println("Bonjour");
  server.send(200, "text/plain", "Bonjour envoye");
}

void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.softAP(ssid, password); // Start access point

  IPAddress myIP = WiFi.softAPIP(); // Get ESP32's IP address
  Serial.print("AP IP address: ");
  Serial.println(myIP);

  server.on("/", handleRoot); // Handle root URL
  server.on("/send", HTTP_POST, handleSend);
  server.onNotFound(handleNotFound); // Handle unknown URLs

  server.begin(); // Start web server
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient(); // Handle incoming client requests
}