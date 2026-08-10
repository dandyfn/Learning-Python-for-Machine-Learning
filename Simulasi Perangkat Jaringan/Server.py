from Router import router
class servercenter:
    def __init__(self,merek,ip,status,router):
        self.merek=merek
        self.ip=ip
        self.gateway = 0
        self.router = router
        self.status=status
        self.koneksi = False

    def setgateway(self):

        if self.router.ip is None:
             self.gateway = 0;
        else:
             self.gateway = self.router.ip
 

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
        print("Gateway:", self.gateway)
        print("Status:", self.status) 
        print("Terkoneksi:", self.koneksi)





class homeserver:
    def __init__(self,merek,ip,status,router):
        self.merek=merek
        self.ip=ip
        self.gateway = 0
        self.router = router
        self.status=status
        self.koneksi = False

    def setgateway(self):

        if self.router.ip is None:
             self.gateway = 0;
        else:
             self.gateway = self.router.ip

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
        print("Gateway:", self.gateway)
        print("Status:", self.status) 
        print("Terkoneksi:", self.koneksi)
   