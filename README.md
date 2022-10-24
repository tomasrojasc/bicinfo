# Circuit connections

### SD card:
| module side  | ESP32 side |
|--------------|------------|
| GND          | GND        |
| VCC          |  5V        |
| MISO         |  Pin 13    |
| MOSI         |  Pin 12    |
| SCK          |  Pin 14    |
| CS           |  Pin 27    |

### GPS

| module side | ESP32 side |
|-------------|------------|
| GND         |  GND       |
| TX          |  Pin 16    |
| RX          |  Pin 17    |
| VCC         |  3V3       |

### BMP280

| module side |  ESP32 side |
|-------------|-------------|
| VIN         | 3V3         |
| GND         | GND         |
| SCL         | Pin 5       |
| SDA         | Pin 4       |