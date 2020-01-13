# squarewave

Dieses Repository enthält Information zum Erzeugen von Rechtecksignalen mit Arduino Hardware mittels bit-banging durch Interrupts.

Die ursprüngliche Motivation war einen Signale eines Drehzahlmessers zu simmulieren.

Das folgende Diagram zeigt das Signal das bei einer Umdrehung erzeugt wird:


```
 +---+   +---+   +---+   +--     -+   +---+   +---+                  
 |   |   |   |   |   |   |   ...  |   |   |   |   |
 +   +---+   +---+   +---+        +---+   +---+   +---+---+---+---+---

 1       2       3       4            61      62      63      64
```
 
Wie man sehen kann wird ein High-Signal 62 mal erzeugt gefolgt von einer kurzen Pause.

Die ursprüngliche Anforderung war das Signale bis zu einer Frequenz von 7000 Drehungen des Drehzahlmessers simuliert werden können.
Wir bezeichenen diese Frequenz als Rad-Frequenz. Da eine Drehung ein Signal mit 64 Abschnitten erzeugt ist die Signal-Frequenz 64 mal höher.

Der im Arduino Nano V3 enthaltene ATmega328P besitzt drei Hardware-Timer die PWM Signale erzeugen können.
Da unser Signal eine Pause am Ende jeder Drehung enthält muessen wir das PWM Signal irgendwie modifizieren.
Wir benutzten eine Interrupt Service Routine um den Signalwert zu verändern welche von einem der Hardware-Timer mit der richtigen Frequenz aufgerufen wird.

Da Timer 1 ein 16-bit Hardware-Timer ist der mit 16 MHz (mit einem Prescale von 1) zaehlt dauert es 4096 us (4096 Mikrosekunden ~ (1/16 MHz)*2^16) bis ein Ueberlauf getriggert wird.
Man kann eine Compare-Register mit einem spezifischen Wert initialisieren und bei Erreichen diese Wertes einen Interrupt auslösen. D.h. man kann in einem beliebigen Intervall zwischen 1/16 MHz und 4096 us periodische Interrupts ausloesen.

Da die Berechnung und das Setzen des Output-Pins innerhalb der Interrupt Service Routine einige CPU Zyklen benötigt kann die Interrupt-Frequenz nicht Nahe bei 16 MHz sein.

Die Berechnung des Signals kann mit Hilfe des folgenden Pseudocodes und Hilfe einer globalen Variable durchgefuehrt werden:

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

Die ausstehende Frage ist nun wie hoch ist die maximale Rad-Frequenz die wir erzeugen können, bzw. wieviele CPU Zyklen verbraucht die Interrupt Service Routine.

Mit Hilfe eines Zwei-Signal-Osziloskop mit ausreichender Bandbreite, können wir dies Messen indem wir einen Ausgabe-Pin am Anfang der Routine auf 1 und am Ende auf 0 setzen.

Wir habe gemessen, dass mehr als 160 CPU Zyklen notwendig sind. Wenn wir 320 als Minimum für den Wert des Compare-Registers verwenden können wird Rad-Frequenzen über 20000 RPM erzeugen.

## Moegliche Verbesserungen
- FastWrite

## Setup:
Bei Verwendung eines Arduino Nano Clones mit CH340 chip muss man einen Treiber installieren (siehe [3]) und "ATmega328P (Old Bootloader)" als Prozessor in der Arduino IDE einstellen.

## Structure:
```
README.md - readme (english)
LIESMICH.md - readme (german)
v1_1000_rpm - yields ~ 1000 rpm
v1_maximum - proof of concept that 20000 rpm can be reached
v1_measurement - was used to determine minimum value for compare interrupt
```

Informationen ueber Timer und Interrupts koennen unter [1] nachgelesen werden.
Der verwendete Arduino Clone "Nano V3.0 CH340" ist unter [2] erhaeltlich.
Installationshinweise zum Treiber für den CH320 USB2Serial Chip stehen unter [3].

## Referenzen

[1] https://www.heise.de/developer/artikel/Timer-Counter-und-Interrupts-3273309.html (deutsch)

[2] https://www.az-delivery.de/products/nano-v3-0-pro (deutsch)

[3] https://www.makershop.de/ch340-341-usb-installieren/ (deutsch)
