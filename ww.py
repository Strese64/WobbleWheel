import WobbleWheel as ww, os

# Kopiere die Schlüsseldatei ww.ww nach C:/Temp
# - Nutze kleine Binärdatei (PNG/JPG) zwischen 10-20 KByte
os.chdir("C:/Temp")
# Starte eine Verschlüsselungsinstanz
# - parameter 1: 0.1 - 20.0
# - parameter 2: 0.1 - 20.0
# - parameter 3: 1000-8999
w = ww.WobbleWheel(11.736, 3.7731, 5764)
# Wähle den zu schlüsselnden Inhalt
myString = 'Ach wie gut das niemand weiß, dass ich Rumpelstielschen heiß'
# Verschlüsseln, als ASCII-Text, ready to transfer to ...
s1 = w.EncryptArray( bytearray(myString,"utf-8") )
b1 = w.ToBase64(s1)
# verschlüsselter ASCII-Text, received from ... wird entschlüsselt
s2 = w.FromBase64(b1)
s3 = w.DecryptArray(s2)
# Vergleichen
if myString == s3.decode("utf-8"):
    print( 'OK' )
    print( 'Original: {}'.format(myString) )
    print( 'CryptStr: {}'.format(b1) )
else:
    print( 'ERROR: {}'.format(s2.decode("utf-8")))
