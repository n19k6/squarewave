drei digitale signale

- kurbelwellen signal 150 Umdrehngen bis 5000 Umdrehungen
- scheibe mit 34 zacken 2 leer, pro 10 grad eine markierung 25, 75 leer (10 bit)


 - nockenwellen signal
 - 3/4 zacken sind besetzt einer fehlt
 - kurbelwelle dreht doppel so schnell wie nockenwelle
 - 2 potentiometer
 - 0-360
 
 - zündreferenzsignal, phasen verschiebung bzgl kurbelwelle
 - potis 10kOhm
 - 1 umdrehung pro sekunde, nach strom, 100 umdrehung
 
 20210123: new try (alles einfach, ohne optimierungen, brute-force)
 - a) sketch machen der schnelles rechteck signal erzeugt (potenziell nicht schneller als 20-100 cpu takt zykel)
 - b) sketch machen der parallel poti werte ausliest und auf der werte auf seriellen schnittstelle dumpt
 - c) anpassung von a) auf kurbelwellen signal (34 zacken, 2 leer, 50% duty cycle)
 - d) steuerung der umdrehungen der kurbelwelle via poti 1. 6000 Umdrehungen können wegen geringem CPU takt von 8 MHz wahrscheinlich nicht erreicht werden
 
 
neues signal für lambda sonde:
0.1Hz-1Hz-10Hz
duty cycle 0%-100%, Mittelstellung ist 50%
duty cycle<5% = always low
duty cycle>95& = always high

poti 1: kurbelwelle, poti 2: lambda sonde frequenz, poti 3: lambda sonde duty cycle
