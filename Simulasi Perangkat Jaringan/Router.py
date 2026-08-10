class router:
    def __init__(self,merek,ip,status):
        self.merek=merek
        self.ip=ip
        self.status=status
        self.koneksi = False


    def gantistatus(self,status):
        self.status=status

    def gantiip(self,ip):
            self.ip=ip

    def gantimerek(self,merek):
            self.merek=merek

    def periksakoneksi(self):

         if self.ip is None:
              self.koneksi = False
         else:
              self.koneksi = True



    def tampilkankondisi(self):
        print("Merek :", self.merek)
        print("IP    :", self.ip)
        print("Status:", self.status) 
        print("Terkoneksi :", self.koneksi)

