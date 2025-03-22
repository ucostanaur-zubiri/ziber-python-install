import warnings
warnings.filterwarnings("ignore")


import ctypes
import snap7
from snap7.types import Areas, S7DataItem,S7WLBit,S7WLWord
#Linux inguruneetan arazoak ematen ditu. Azpiko lerroa jarrita aurrekoaren ordez, ondo dabil
#from snap7.type import Areas, S7DataItem
from snap7.util import set_int,set_usint,set_real,get_int,get_real
import snap7.server as server
import time



class OIL:
    def __init__(self):
        self.client=snap7.client.Client()
        self.IP="192.168.2.5"
        self.rack=0
        self.CPU=1

    def connect(self):
        self.client.connect(self.IP,self.rack,self.CPU)

    def disconnect(self):
        self.client.disconnect()


    def marcha_bomba(self):
        actual1=self.client.db_read(9,60,1)
        actual1[0]=actual1[0]|2
        self.client.db_write(9,60,actual1)
        self.client.db_write(9,90,actual1)
        self.client.db_write(9,120,actual1)
        actual=self.client.db_read(9,0,1)
        actual[0]=actual[0]|3
        self.client.db_write(9,0,actual)

    def paro_bomba(self):
        actual=self.client.db_read(9,0,1)
        actual[0]=actual[0]|1
        actual[0]=actual[0]&253
        self.client.db_write(9,0,actual)

    def abrir_800(self):
        actual=self.client.db_read(9,6,1)
        actual[0]=actual[0]|3
        actual[0]=actual[0]&251
        self.client.db_write(9,6,actual)
        actual1=self.client.db_read(9,60,1)
        actual1[0]=actual[0]|2
        self.client.db_write(9,60,actual1)
    
    def cerrar_800(self):
        print("TO DO")


    def abrir_850(self):
        actual=self.client.db_read(9,12,1)
        actual[0]=actual[0]|3
        actual[0]=actual[0]&251
        self.client.db_write(9,12,actual)
        actual1=self.client.db_read(9,90,1)
        actual1[0]=actual[0]|2
        self.client.db_write(9,90,actual1)
 
    def cerrar_850(self):
        print("TO DO")

    def abrir_888(self):
        actual=self.client.db_read(9,18,1)
        actual[0]=actual[0]|3
        actual[0]=actual[0]&251
        self.client.db_write(9,18,actual)
        actual1=self.client.db_read(9,120,1)
        actual1[0]=actual1[0]|2
        self.client.db_write(9,120,actual1)
    
    def cerrar_888(self):
        print("TO DO")


    def niveles(self,tank,level):
        if(tank=="800"):
            direccion=0
        if(tank=="850"):
            direccion=4
        if(tank=="888"):
            direccion=8
        if(tank=="1000"):
            direccion=12

        data=self.client.db_read(10,direccion,4)

        
        snap7.util.set_real(data,0,float(level))
        self.client.db_write(10,direccion,data)
    

