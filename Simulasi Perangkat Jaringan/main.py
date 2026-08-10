from Router import router
from Server import *
r1 = router("Cisco","192.168.1.1","Aktif")
r1.periksakoneksi()
r1.tampilkankondisi()

s1 = servercenter("Meraki Server","192.168.1.2","Aktif",r1)
s1.periksakoneksi()
s1.setgateway()
s1.tampilkankondisi()

s1 = homeserver("Ubuntu Server","192.168.1.3","Aktif",r1)
s1.tampilkankondisi()