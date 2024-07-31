#include <WiFi.h>

#define pin 13
#define led 25

boolean flag = true;

const char* ssid = "Bitch";
const char* password = "12345578";

WiFiServer wifiServer(80);

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to the WiFi network");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Subnet Mask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("Gateway IP: ");
  Serial.println(WiFi.gatewayIP());
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());
  Serial.println("");

  wifiServer.begin();

  pinMode(pin, INPUT);
  pinMode(led, OUTPUT);
  digitalWrite(led,LOW);
  attachInterrupt(digitalPinToInterrupt(pin), handleInterrupt, RISING);

}

void loop() {
  WiFiClient client = wifiServer.available();

  if (client) {
    if (flag==false) {
      client.println("Motion detected!");
    }
    delay(10);
    client.stop();
  }
  
  if (flag==true) {
    Serial.println("Listening for motion...");
    delay(2000);
  }
  else {
    digitalWrite(led,LOW);
    delay (6000);
    flag = true;
    Serial.println("Motion detection resumed.");
  }

}

void handleInterrupt() {
  if (flag==true) {
    digitalWrite(led,HIGH);
    flag = false;
    Serial.println("Pausing motion detection...");
  }
}