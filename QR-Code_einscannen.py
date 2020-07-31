import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import time
import cv2
import sqlite3
from datetime import datetime


verbindung = sqlite3.connect("Database.db")
zeiger = verbindung.cursor()

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="result.csv", help="path to csv file")
args = vars(ap.parse_args())

print('[INFO] starting stream')
vs = VideoStream(scr=0).start()
time.sleep(2.0)

csv = open(args["output"], "w")
found = set()
AltZeit = datetime.now()
frame = vs.read()
frame = imutils.resize(frame, width=400)
cv2.imshow("QR Code Scanner", frame)
time.sleep(4.0)


while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    barcodes = pyzbar.decode(frame)
    

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        Zeitpunkt = datetime.now()
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        
        
        z = Zeitpunkt- AltZeit
        z = z.total_seconds()
        AltZeit = Zeitpunkt
        if z > 3:
            text = "{}".format(barcodeData)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            
            Produktnummer = text
            zeiger.execute("""INSERT INTO scans VALUES ( ?, ?)""", (Produktnummer, Zeitpunkt))
            verbindung.commit()

        if barcodeData not in found:
            csv.write("{}\n".format(barcodeData))
            csv.flush()
            found.clear()
            found.add(barcodeData)
    cv2.imshow("QR Code Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


print("[INFO] Cleaning up")
verbindung.close()
csv.close()
cv2.destroyAllWindows()
vs.stop()




