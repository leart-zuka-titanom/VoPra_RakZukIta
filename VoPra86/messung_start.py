# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 15:13:11 2014

@author: localadmin
"""
from pylab import *
import time
import numpy as np
import steprocker
import counter

#Anzahl von schritten bis zur Mitte
mitSchritt=5884486
#Messzeit pro Messpunkt (auf sinnvollen Wert stellen)
messzeit=8229 
#Umrechnungsfaktor von Schritten in Weg in mm
mmps=1.56e-5
#Schrittweite
schrittw=round(1/mmps)

anzahlmesspunkte=63
anzahl_mp_seite=(anzahlmesspunkte-1)/2

delta_winkel=0.5e-3
delta_laenge=1.25*delta_winkel
delta_schritt=round((delta_laenge*10**3)/mmps)

#Steuerung für den Schrittmotor
sp=steprocker.steprocker()
#Steuerung für den Counter
co=counter.counter()

#Erstmal bis zum Endschalter fahren
sp.schnell()
sp.rotLinks()
while sum(sp.statusLimitSwitch())==0: time.sleep(1)
sp.stop()
sp.langsam()

#Und dann zum ersten Messpunkt fahren
sp.fahreSchritte(mitSchritt-anzahl_mp_seite*delta_schritt)
#Warten bis die Position erreicht ist
while sp.posEreicht()==0: time.sleep(1)
data = []

#Eigentliche Messung
for idx in range(anzahlmesspunkte):   
    #Counter starten 
    co.start()
    #gewisse Zeit warten
    time.sleep(messzeit)
    #Counter stoppen
    co.stop()
    #Counter auslesen
    a,b = co.counts()
    print(a,b)
    #Ergebnis speichern
    with open("data.csv","a") as file:
        file.write("{},{}\n".format(a,b))
    #Counter auf null setzen
    co.clear()
    #Schrittmotor verfahren
    sp.fahreSchritte(delta_schritt)
    #Warten bis die Position erreicht ist
    while sp.posEreicht()==0: time.sleep(1)
   
#Ergebnis speichern
