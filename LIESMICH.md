# squarewave

Dieses Repository enthaelt Information zum Erzeugen von Rechtecksignalen mit Arduino Hardware mittels bit-banging durch Interrupts.

Die urspruengliche Motivation war ein Signal eines Drehzahlmessers zu simulieren.

Das folgende Diagramm zeigt das Signal das bei einer Umdrehung erzeugt wird:


```
 +---+   +---+   +---+   +--     -+   +---+   +---+                  
 |   |   |   |   |   |   |   ...  |   |   |   |   |
 +   +---+   +---+   +---+        +---+   +---+   +---+---+---+---+---

 1       2       3       4            61      62      63      64
```
 
Wie man sehen kann wird ein High-Signal 62 mal erzeugt gefolgt von einer kurzen Pause.

Die urspruengliche Anforderung war das ein Signal mit bis zu einer Frequenz von 7000 Drehungen des Drehzahlmessers simuliert werden kann.
Wir bezeichnen diese Frequenz als Rad-Frequenz. Da eine Drehung ein Signal mit 64 Abschnitten erzeugt ist die Signal-Frequenz 64 mal hoeher.

Der im Arduino Nano V3 enthaltene ATmega328P besitzt drei Hardware-Timer die PWM Signale erzeugen koennen.
Da unser Signal eine Pause am Ende jeder Drehung enthaelt muessen wir das PWM Signal irgendwie modifizieren.
Wir benutzten eine Interrupt Service Routine um den Signalwert zu veraendern welche von einem der Hardware-Timer mit der richtigen Frequenz aufgerufen wird.

Da Timer 1 ein 16-bit Hardware-Timer ist der mit 16 MHz (mit einem Prescale von 1) zaehlt dauert es 4096 us (4096 Mikrosekunden ~ (1/16 MHz)*2^16) bis ein Ueberlauf getriggert wird.
Man kann ein Compare-Register mit einem spezifischen Wert initialisieren und bei Erreichen diese Wertes einen Interrupt ausloesen. D.h. man kann in einem beliebigen Intervall zwischen 1/16 MHz und 4096 us periodische Interrupts ausloesen.

Da die Berechnung und das Setzen des Output-Pins innerhalb der Interrupt Service Routine einige CPU Zyklen benoetigt kann die Interrupt-Frequenz nicht Nahe bei 16 MHz sein.

Die Berechnung des Signals kann mit Hilfe des folgenden Pseudocodes und Hilfe einer globalen Variablen durchgefuehrt werden:

```
 +---+   +---+   +---+   +--     -+   +---+   +---+                  
 |   |   |   |   |   |   |   ...  |   |   |   |   |
 +   +---+   +---+   +---+        +---+   +---+   +---+---+---+---+---

 0   1   2   3   4   5   6            120 121 122 123 124 125 126 127

volatile byte count = 0

set counter of timer 1 to 0
if (count % 2 == 0 and count < 124):
  set output to 1
else
  set output to 0
count++
count = count % 128
```

Die ausstehende Frage ist nun wie hoch ist die maximale Rad-Frequenz die wir erzeugen koennen, bzw. wie viele CPU Zyklen verbraucht die Interrupt Service Routine.

Mit Hilfe eines Zwei-Signal-Oszilloskop mit ausreichender Bandbreite, koennen wir dies Messen indem wir einen Ausgabe-Pin am Anfang der Routine auf 1 und am Ende auf 0 setzen.

Wir haben gemessen, dass mehr als 160 CPU Zyklen notwendig sind. Wenn wir 320 als Minimum fuer den Wert des Compare-Registers verwenden koennen wir eine Rad-Frequenzen mit ueber 20000 RPM erzeugen.

## Moegliche Verbesserungen
- FastWrite

## Setup:
Bei Verwendung eines Arduino Nano Clones mit CH340 Chip muss man einen Treiber installieren (siehe [3]) und "ATmega328P (Old Bootloader)" als Prozessor in der Arduino IDE einstellen.

## Struktur:
```
README.md - readme (english)
LIESMICH.md - readme (german)
v1_1000_rpm - yields ~ 1000 rpm
v1_maximum - proof of concept that 20000 rpm can be reached
v1_measurement - was used to determine minimum value for compare interrupt
```

Informationen ueber Timer und Interrupts koennen unter [1] nachgelesen werden.
Der verwendete Arduino Clone "Nano V3.0 CH340" ist unter [2] erhaeltlich.
Installationshinweise zum Treiber fuer den CH320 USB2Serial Chip stehen unter [3].

## Referenzen

[1] https://www.heise.de/developer/artikel/Timer-Counter-und-Interrupts-3273309.html (deutsch)

[2] https://www.az-delivery.de/products/nano-v3-0-pro (deutsch)

[3] https://www.makershop.de/ch340-341-usb-installieren/ (deutsch)
