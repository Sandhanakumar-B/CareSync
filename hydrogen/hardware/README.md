# Hardware Setup - ESP32 + MFRC522

This folder contains a reference implementation for a physical ESP32 connected to an RC522 RFID reader. The hardware will read an RFID tag and send an HTTP POST request to the CareSync backend over Wi-Fi.

## Wiring (SPI)

| RC522 Pin | ESP32 Pin |
|-----------|-----------|
| SDA (SS)  | GPIO 5    |
| SCK       | GPIO 18   |
| MOSI      | GPIO 23   |
| MISO      | GPIO 19   |
| IRQ       | N/A       |
| GND       | GND       |
| RST       | GPIO 22   |
| 3.3V      | 3.3V      |

## Dependencies
- MFRC522 library by GithubCommunity
- WiFi.h
- HTTPClient.h

Configure your Wi-Fi credentials and the CareSync server IP address in the `.ino` sketch before uploading.
