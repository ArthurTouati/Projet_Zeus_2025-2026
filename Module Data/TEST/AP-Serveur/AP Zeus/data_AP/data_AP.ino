#include <WiFi.h>
#include <WebServer.h>
#include <cstdlib>
#include <ctime>

const char* ssid = "Controle-Access-Point"; // Access point SSID
const char* password = "************"; // Access point password (at least 8 characters)
float latitude;
float longitude;

WebServer server(80); // Web server on port 80

void handleRoot() {
  String html = "<!DOCTYPE html>\n";
  html += "<html>\n";
  html += "<head>\n";
  html += "<title>Centre de contrôle</title>\n";
  html += "<meta charset=\"UTF-8\">\n";
  html += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
  html += "<style>\n";
  html += "body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background-color: #f4f4f4; margin: 0; }\n";
  html += ".container { background-color: #fff; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); max-width: 800px; width: 100%; text-align: center; }\n";
  html += "h1 { margin-bottom: 20px; }\n";
  html += ".button-row { display: flex; justify-content: center; margin-bottom: 20px; }\n";
  html += "button { padding: 10px 20px; margin: 0 10px; border: none; border-radius: 5px; background-color: #007bff; color: #fff; cursor: pointer; }\n";
  html += "button:hover { background-color: #0056b3; }\n";
  html += "a { text-decoration: none; }\n";
  html += "</style>\n";
  html += "</head>\n";
  html += "<body>\n";
  html += "<div class=\"container\">\n";
  html += "<h1>Centre de contrôle projet Zeus</h1>\n";
  html += "<div class=\"button-row\">\n";
  html += "<a href=\"/gps\"><button>GPS</button></a>\n";
  html += "<a href=\"/test\"><button>Contrôle</button></a>\n";
  html += "<a href=\"/data\"><button>Données</button></a>\n";
  html += "</div>\n";
  html += "</div>\n";
  html += "</body>\n";
  html += "</html>\n";

  server.send(200, "text/html", html);
}

void handleGPS() {
  latitude = random(0, 20000) / 100.0;
  longitude = random(0, 20000) / 100.0;
  String html = "<!DOCTYPE html>\n";
  html += "<html>\n";
  html += "<head>\n";
  html += "<title>Coordonnées GPS</title>\n";
  html += "<meta charset=\"UTF-8\">\n";
  html += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
  html += "<style>\n";
  html += "body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background-color: #f4f4f4; margin: 0; }\n";
  html += "h1 { color: #333; }\n";
  html += ".container { background-color: #fff; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); max-width: 800px; width: 100%; display: flex; flex-direction: column; align-items: center;}\n";
  html += "#map { width: 100%; height: 400px; margin-top: 20px; border-radius: 5px; }\n";
  html += ".menu-button { margin-top: 20px; padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; }\n";
  html += "</style>\n";
  html += "</head>\n";
  html += "<body>\n";
  html += "<div class=\"container\">\n";
  html += "<h1>Coordonnées GPS</h1>\n";
  html += "<p>Les coordonnées GPS de la fusée sont les suivantes :</p>\n";
  html += "<p>Latitude : " + String(latitude) + "</p>\n";
  html += "<p>Longitude : " + String(longitude) + "</p>\n";
  html += "<a href=\"/\" class=\"menu-button\">Menu</a>\n";
  html += "</div>\n";
  html += "</body>\n";
  html += "</html>\n";

  server.send(200, "text/html", html);
}

void handleTest() {
  String html = "<!DOCTYPE html>\n";
  html += "<html>\n";
  html += "<head>\n";
  html += "<title>Contrôle</title>\n";
  html += "<meta charset=\"UTF-8\">\n";
  html += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
  html += "<style>\n";
  html += "body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background-color: #f4f4f4; margin: 0; }\n";
  html += ".container { background-color: #fff; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); max-width: 800px; width: 100%; text-align: center; }\n";
  html += ".button-row { display: flex; justify-content: center; margin-bottom: 20px; }\n";
  html += "button { padding: 10px 20px; margin: 0 10px; border: none; border-radius: 5px; background-color: #007bff; color: #fff; cursor: pointer; }\n";
  html += "button:hover { background-color: #0056b3; }\n";
  html += "h2 { margin-bottom: 20px; }\n";
  html += "</style>\n";
  html += "</head>\n";
  html += "<body>\n";
  html += "<div class=\"container\">\n";
  html += "<h2>Test des systèmes</h2>\n";
  html += "<div class=\"button-row\">\n";
  html += "<button>Bouton 1</button>\n";
  html += "<button>Bouton 2</button>\n";
  html += "<button>Bouton 3</button>\n";
  html += "<button>Bouton 4</button>\n";
  html += "<button>Bouton 5</button>\n";
  html += "</div>\n";
  html += "<a href=\"/\"><button>Menu</button></a>\n";
  html += "</div>\n";
  html += "</body>\n";
  html += "</html>\n";

  server.send(200, "text/html", html);
}

void handleData() {
  String html = "<!DOCTYPE html>\n";
  html += "<html>\n";
  html += "<head>\n";
  html += "<title>Données de vol Projet Zeus</title>\n";
  html += "<meta charset=\"UTF-8\">\n";
  html += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
  html += "<style>\n";
  html += "body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background-color: #f4f4f4; margin: 0; }\n";
  html += ".container { background-color: #fff; padding: 30px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); max-width: 800px; width: 100%; text-align: center; }\n";
  html += "h1, h2 { margin-bottom: 20px; }\n";
  html += "table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }\n";
  html += "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n";
  html += "th { background-color: #f2f2f2; }\n";
  html += "a { text-decoration: none; }\n";
  html += "button { padding: 10px 20px; margin: 0 10px; border: none; border-radius: 5px; background-color: #007bff; color: #fff; cursor: pointer; }\n";
  html += "button:hover { background-color: #0056b3; }\n";
  html += "</style>\n";
  html += "</head>\n";
  html += "<body>\n";
  html += "<div class=\"container\">\n";
  html += "<h1>Données de vol Projet Zeus</h1>\n";
  html += "<h2>État des systèmes</h2>\n";
  html += "<table>\n";
  html += "<thead>\n";
  html += "<tr>\n";
  html += "<th>Temp en seconde</th>\n";
  html += "<th>Module</th>\n";
  html += "<th>Commentaire</th>\n";
  html += "</tr>\n";
  html += "</thead>\n";
  html += "<tbody>\n";
  html += "<tr><td>0</td><td>Module contrôle</td><td>OK</td></tr>\n";
  html += "<tr><td>1</td><td>Module télémesure</td><td>OK</td></tr>\n";
  html += "<tr><td>2</td><td>Module charge utile</td><td>OK</td></tr>\n";
  html += "<tr><td>3</td><td>Module charge utile largué</td><td>OK</td></tr>\n";
  html += "</tbody>\n";
  html += "</table>\n";
  html += "<h2>Trajectoire</h2>\n";
  html += "<table>\n";
  html += "<thead>\n";
  html += "<tr>\n";
  html += "<th>Temp en seconde</th>\n";
  html += "<th>Latitude</th>\n";
  html += "<th>Longitude</th>\n";
  html += "<th>Roulis</th>\n";
  html += "<th>Tangage</th>\n";
  html += "<th>Lacet</th>\n";
  html += "<th>Altitude</th>\n";
  html += "</tr>\n";
  html += "</thead>\n";
  html += "<tbody>\n";
  html += "<tr><td>0</td><td>48.8566</td><td>2.3522</td><td>0</td><td>0</td><td>0</td><td>100</td></tr>\n";
  html += "<tr><td>1</td><td>48.8567</td><td>2.3523</td><td>1</td><td>2</td><td>3</td><td>101</td></tr>\n";
  html += "<tr><td>2</td><td>48.8568</td><td>2.3524</td><td>2</td><td>4</td><td>6</td><td>102</td></tr>\n";
  html += "<tr><td>3</td><td>48.8569</td><td>2.3525</td><td>3</td><td>6</td><td>9</td><td>103</td></tr>\n";
  html += "</tbody>\n";
  html += "</table>\n";
  html += "<a href=\"/\"><button>Menu</button></a>\n";
  html += "</div>\n";
  html += "</body>\n";
  html += "</html>\n";

  server.send(200, "text/html", html);
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
  server.on("/gps", handleGPS);
  server.on("/test", handleTest);
  server.on("/data", handleData);
  server.onNotFound(handleNotFound); // Handle unknown URLs

  server.begin(); // Start web server
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient(); // Handle incoming client requests
}
