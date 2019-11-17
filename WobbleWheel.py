import math as M
import os, base64

class WobbleWheel:
    """ Der Algorithmus dient der symmetrischen Verschlüsselung von Strings
        und ByteArrays aus Variablen und Dateien
    """

    rho = 180.0 / M.pi
    wwm = 200 * 5               # Breite des Rades
    buf = bytearray(10000)      # Schlüssel-Puffer

    def __init__(self, mo, mu, ab):
        """ Setze eine Instanz der Klasse WobbleWheel auf:
            > Setze scale_up = Maßstand der linken Radseite
            > Setze scale_dn = Maßstand der rechten Radseite
            > Setze add_dist = Startwert (1000 - (9999-Radbreite))
            > Lade Datei individuelle Schlüsseldatei "ww.ww",
              mit mehr als 10.000 binäre Bytes
        """
        self.scale_up = float(mo)
        self.scale_dw = float(mu)
        self.add_dist = abs(ab)
        if self.add_dist<1000: self.add_dist = 1000
        if self.add_dist>(9999-self.wwm): self.add_dist = (9999-self.wwm)
        try:
            with open("ww.ww", "rb") as fp:
                self.buf = fp.read(10000)
            fp.close
            self.okay = True
        except:
            self.okay = False

    def Encrypt(self, by, pos):
        """ Verschlüssele ein Byte
        """
        if not self.okay: return -1
        cv = int(self.buf[pos])
        iv = (by + cv) % 256
        return iv

    def Decrypt(self, by, pos):
        """ Entschlüssle ein Byte
        """
        if not self.okay: return -1
        cv = int(self.buf[pos])
        iv = (256 + by - cv) % 256
        return iv

    def EncryptArray(self, bybuf):
        """ Verschlüssle eine Array of Bytes
        """
        l = len(bybuf)
        retbuf = bytearray(l)
        startv = i = p = 0
        while 42:
            (ab,anz) = self.GetKey(startv)
            startv += 1
            while i<anz:
                cv = self.Encrypt(int(bybuf[i]), ab+i-p)
                retbuf[i] = cv
                i += 1
                if i >= l: break
            p = i
            if i >= l: break
        return retbuf
        
    def DecryptArray(self, bybuf):
        """ Entschlüssle eine Array of Bytes
        """
        l = len(bybuf)
        retbuf = bytearray(l)
        startv = i = p = 0
        while 42:
            (ab,anz) = self.GetKey(startv)
            startv += 1
            while i<anz:
                cv = self.Decrypt(int(bybuf[i]), ab+i-p)
                retbuf[i] = cv
                i += 1
                if i >= l: break
            p = i
            if i >= l: break
        return retbuf
        
    def GetKey(self, pos):
        """ Bestimmt den Offset und die Anzahl der Bytes: 
            ! Der "taumelnde Rad"-Algorithmus !
        """
        if not self.okay: return (-1, -1)
        mc = M.cos((pos+51.234) * self.scale_up / self.rho)
        ms = M.sin((pos+51.234) * self.scale_dw / self.rho)
        po = int(self.wwm - mc * (self.wwm/5.0))
        pu = int(ms * (self.wwm/5.0) + (self.wwm/5.0))
        return (pu + self.add_dist, po-pu)

    def ToBase64(self,data):
        return str(base64.b64encode(data), "utf-8")

    def FromBase64(self,data):
        return base64.urlsafe_b64decode(data)

if __name__ == "__main__":
    """ Modultest der Klasse WobbleWheel
    """
    os.chdir("C:/Temp")
    w = WobbleWheel(11.736, 3.7731, 5764)
    myString = 'Ach wie gut das niemand weiß, dass ich Rumpelstielschen heiß'
    s1 = w.EncryptArray( bytearray(myString,"utf-8") )
    s2 = w.DecryptArray(s1)
    if myString == s2.decode("utf-8"):
        print( 'OK' )
        print( 'Original : {}'.format(myString) )
        print( 'CryptStr : {}'.format(s1) )
    else:
        print( 'ERROR    : {}'.format(s2.decode("utf-8")))
    b1 = w.ToBase64(s1)
    s3 = w.FromBase64(b1)
    if s3 == s1:
        print( 'OK' )
        print( 'Base64Str: {}'.format(b1) )
