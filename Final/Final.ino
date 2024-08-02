#include <WiFi.h>

#define pin 13
#define led 25

boolean connected = false;
boolean flag = true;

const char* ssid = "PLDTHOMEFIBR26212";
const char* password = "PLDTWIFI12OKE";

WiFiServer wifiServer(80);
WiFiClient client;

void setup() {
    Serial.begin(115200);
    delay(1000);

    WiFi.mode(WIFI_AP_STA);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
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
    digitalWrite(led, LOW);
    attachInterrupt(digitalPinToInterrupt(pin), handleInterrupt, RISING);
}

void loop() {
    if (!client.connected()) {
        if (client.connect("ccscloud.dlsu.edu.ph", 20257)) {
            Serial.println("Connected to server");
            connected = true;
        } else {
            Serial.println("Connection to server failed");
            delay(1000); // Wait before retrying
        }
    }

    if (client.connected()) {
        if (!flag) {
            client.print("Motion detected!");
            delay(10);
        }
    } else {
        connected = false;
    }

    if (flag) {
        Serial.println("Listening for motion...");
        delay(2000);
    } else{
        digitalWrite(led, LOW);
        delay(6000);
        flag = true;
        Serial.println("Motion detection resumed.");
    }
}

void handleInterrupt() {
    if (flag) {
        digitalWrite(led, HIGH);
        flag = false;
        Serial.println("Pausing motion detection...");
    }
}

