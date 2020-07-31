import sqlite3
from datetime import datetime
from datetime import timedelta
import time
from operator import add,itemgetter

stationen=['Rohstofflager', 'Drehmaschine', 'Zwischenlager 1', 'Fräsmaschine', 'Zwischenlager 2', 'Schleifmaschine', 'Fertigwarenlager']

def berechne_Zeitunterschied(anzahl, inhalt): 

    if len(inhalt)>=anzahl:        
        Zeit = str(list(inhalt[anzahl-1]))
        Zeit2 = str(list(inhalt[anzahl]))
        datetime_Zeit = datetime.strptime(Zeit, "['%Y-%m-%d %H:%M:%S.%f']")
        datetime_Zeit2 = datetime.strptime(Zeit2, "['%Y-%m-%d %H:%M:%S.%f']")
        Zeitunterschied1 = datetime_Zeit2 - datetime_Zeit
        Zeitunterschied1 = Zeitunterschied1.total_seconds()
    
    return(Zeitunterschied1)

def berechnung(produktnummer):

    verbindung = sqlite3.connect ("Database.db")
    zeiger = verbindung.cursor()
    Produktnummer=produktnummer    
    zeiger.execute("SELECT Zeitpunkt FROM scans WHERE Produktnummer="+ str(Produktnummer))
    inhalt = zeiger.fetchall()
    Differenzenliste=[] 
    for i in range(len(inhalt)-1):
        Differenzenliste.append(berechne_Zeitunterschied(i+1, inhalt)) 
    
    return(Differenzenliste)     

def vervollständigen(produktnummer):
       
    Differenzenliste=berechnung(produktnummer)
    while len(Differenzenliste)<7:
        Differenzenliste.append(0)
    return(Differenzenliste)

def listenlänge(produktnummer):
                                         
    bearbeitungsfortschritt=len(berechnung(produktnummer))
    return(bearbeitungsfortschritt)

def liegz():

    Differenzenliste55101 = vervollständigen(55101)   
    Differenzenliste55102 = vervollständigen(55102)    
    Differenzenliste55103 = vervollständigen(55103)    
    Differenzenliste55104 = vervollständigen(55104)
            
    data = {'stationen' : stationen,
            '55101' : Differenzenliste55101,
            '55102' : Differenzenliste55102,
            '55103' : Differenzenliste55103,
            '55104' : Differenzenliste55104}

    return(data)

def lagk():

    Dif55101 = vervollständigen(55101)   
    Dif55102 = vervollständigen(55102)    
    Dif55103 = vervollständigen(55103)    
    Dif55104 = vervollständigen(55104)
   
    Dif55101_55102=list(map(add,Dif55101,Dif55102))
    Dif55103_55104=list(map(add,Dif55103,Dif55104))
    addierte_Listen = list(map(add,Dif55101_55102,Dif55103_55104))
    multiplizierte_Listen = [element*1/60 for element in addierte_Listen]
    Lagerkosten=itemgetter(0,2,4,6)(multiplizierte_Listen)

    return Lagerkosten

def wertsch():

    WertschoepfungDrehen=30 
    WertschoepfungFraesen=40
    WertschoepfungSchleifen=20
    
    laenge55101=listenlänge(55101)
    laenge55102=listenlänge(55102)
    laenge55103=listenlänge(55103)
    laenge55104=listenlänge(55104)

    a = [laenge55101, laenge55102, laenge55103, laenge55104]
    WS = []

    for i in a:
        print(i)
        if i < 2:      
            WS.append(0)            
        if i >=2 and i<4:    
            WS.append(WertschoepfungDrehen)                  
        if i >=4 and i<6:      
            WS.append(WertschoepfungDrehen+WertschoepfungFraesen)                
        if i >=6:      
            WS.append(WertschoepfungDrehen+WertschoepfungFraesen+WertschoepfungSchleifen) 
                          
    return WS


