#include <WiFi.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN  5
#define RST_PIN 22

MFRC522 rfid(SS_PIN, RST_PIN);

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://192.168.1.100:5000/api/rfid/scan"; // Update IP

const String READER_ID = "READER-01";

void setup() {
    Serial.begin(115200);
    SPI.begin();
    rfid.PCD_Init();

    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected!");
}

void loop() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        return;
    }

    String tagId = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        tagId += String(rfid.uid.uidByte[i], HEX);
    }
    tagId.toUpperCase();
    
    Serial.println("Tag read: " + tagId);
    
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverUrl);
        http.addHeader("Content-Type", "application/json");

        String jsonPayload = "{\"tag_id\":\"" + tagId + "\", \"reader_id\":\"" + READER_ID + "\", \"trigger_source\":\"HARDWARE\"}";
        int httpResponseCode = http.POST(jsonPayload);
        
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        
        http.end();
    }
    
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
    delay(2000); // Debounce
}
