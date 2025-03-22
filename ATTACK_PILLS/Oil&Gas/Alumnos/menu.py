import progressbar
from time import sleep
import keyboard
import sys
import pildorasSiemens
sys.tracebacklimit = 0




class menu:
    def __init__(self):
        self.opcion=0
        self.texto="> "
        self.valvula="800"
        self.tanque="800"
        self.sensor="0"
        self.oil=pildorasSiemens.OIL()



        


    def print_welcome(self):
        print(" ____  __  __  ____  ____  ____  ____    __  __    __    _  _  ____  ____  _____ ")
        print("(_   )(  )(  )(  _ \(_  _)(  _ \(_  _)  (  \/  )  /__\  ( \( )(_  _)( ___)(  _  )")
        print(" / /_  )(__)(  ) _ < _)(_  )   / _)(_    )    (  /(__)\  )  (   )(   )__)  )(_)( ")
        print("(____)(______)(____/(____)(_)\_)(____)  (_/\/\_)(__)(__)(_)\_) (__) (____)(_____)")



    def print_menu(self):
        print("Choose your action by introducing the number")
        print("1 - open_valve")
        print("2 - close_valve")
        print("3 - burn_pump")
        print("4 - stop pump")
        print("5 - run_pump")
        print("6 - false_level")


    def imprimir_prompt(self):
        print(self.texto, end="")
    
    def procesar_respuesta(self,resp):
        option=0        

        if(resp[0]=="use"):
            option=resp[1]
            

        if(resp[0]=="1" or option=="1"):
            self.opcion=1
            self.texto="open_valve> "

        if(resp[0]=="2" or option=="2"):
            self.opcion=2
            self.texto="close_valve> "

        if(resp[0]=="3" or option=="3"):
            self.opcion=3
            self.texto="burn_pump> "

        if(resp[0]=="4" or option=="4"):
            self.opcion=4
            self.texto="stop_pump> "

        if(resp[0]=="5" or option=="5"):
            self.opcion=5
            self.texto="run_pump> "

        if(resp[0]=="6" or option=="6"):
            self.opcion=6
            self.texto="false_level> "
        
        if(resp[0]=="run"):
            if(self.opcion==1):
                self.P01()
            if(self.opcion==2):
                self.P02()
            if(self.opcion==3):
                self.P03()
            if(self.opcion==4):
                self.P04()
            if(self.opcion==5):
                self.P05()
            if(self.opcion==6):
                self.P06()

        if(resp[0]=="show"):
            if(self.opcion in [1,2,3,4,5,6]):
                print("IP "+self.oil.IP)

            if(self.opcion==1 or self.opcion==2):
                print("Valve "+self.valvula)

            if(self.opcion==6):
                print("Tank "+self.tanque)
                print("Sensor "+self.sensor)

        if(resp[0]=="set"):
            if(self.opcion in [1,2,3,4,5,6]):
                if(resp[1].lower()=="ip"):
                    self.oil.IP=resp[2]
            if(self.opcion in [1,2]):
                if(resp[1].lower()=="valve"):
                    self.valvula=resp[2]
            if(self.opcion==6):
                if(resp[1].lower()=="tank"):
                    self.tanque=resp[2]
                if(resp[1].lower()=="sensor"):
                    self.sensor=resp[2]

        if(resp[0]=="exit"):
                self.opcion=0
                self.print_menu()
                self.texto=">"

        if(resp[0]=="help"):
                print("use X -> select the action number X")
                print("exit -> closes the script")
                print("set -> modify a parameter")
                print("show -> shows all the parameters from the selected action")
                print("run -> runs the selected action with current parameters")
                print("help -> this menu")
                print("")
                print("")

                self.print_menu()


        

    def barra_progreso(self):
        bar = progressbar.ProgressBar(maxval=20, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        for i in range(20):
            bar.update(i+1)
            sleep(0.1)
        bar.finish()
        

    def P01(self):
        print("Connecting to PLC")
        self.oil.connect()
        self.barra_progreso()
        print("Opening Valve "+self.valvula)
        #print("Detener ejecución pulsando tecla c")
        while True:
            if(self.valvula=="800"):
                self.oil.abrir_800()
            if(self.valvula=="850"):
                self.oil.abrir_850()
            if(self.valvula=="888"):
                self.oil.abrir_888()
            if(keyboard.is_pressed('c')):
                break
        self.oil.disconnect()

    def P02(self):
        print("Connecting to PLC")
        self.oil.connect()
        self.barra_progreso()
        print("Closing Valve "+self.valvula)
        #print("Detener ejecución pulsando tecla c")
        while True:
            if(self.valvula=="800"):
                self.oil.cerrar_800()
            if(self.valvula=="850"):
                self.oil.cerrar_850()
            if(self.valvula=="888"):
                self.oil.cerrar_888()
            if(keyboard.is_pressed('c')):
                break
        self.oil.disconnect()

    def P03(self):
        print("Connecting to PLC")
        self.oil.connect()
        self.barra_progreso()
        print("Running & stopping Pump")
        #print("Detener ejecución pulsando tecla c")
        while True:
            self.oil.marcha_bomba()
            sleep(1)
            self.oil.paro_bomba()
            sleep(1)
            if(keyboard.is_pressed('c')):
                break
        self.oil.disconnect()

    def P04(self):
        print("Connecting to PLC")
        self.oil.connect()
        self.barra_progreso()
        print("Stopping Pump")
        #print("Detener ejecución pulsando tecla c")
        while True:
            self.oil.paro_bomba()
            sleep(1)
            if(keyboard.is_pressed("c")):
                break
        self.oil.disconnect()


    def P05(self):
        print("Connecting to PLC")
        self.oil.connect()
        self.barra_progreso()
        print("Overflowing Tank T1000")
        #print("Detener ejecución pulsando tecla c")
        while True:
            self.oil.abrir_888()
            self.oil.abrir_850()
            self.oil.abrir_800()
            self.oil.marcha_bomba()
        self.oil.disconnect()
     


    def P06(self):
        print("Connecting to PLC")
        self.oil.connect()
        self.barra_progreso()
        print("False level. Tank "+self.tanque)
        #print("Detener ejecución pulsando tecla c")
        while True:
            self.oil.niveles(self.tanque,self.sensor)
        self.oil.disconnect()





menu=menu()



if(len(sys.argv)>1):
    opt=str(sys.argv[1])


    if(opt in ["1","2"]):
        menu.valvula=str(sys.argv[2])

        if(opt=="1"):
            menu.P01()
        if(opt=="2"):
            menu.P02()

    if(opt=="3"):
        menu.P03()
   
    if(opt=="4"):
        menu.P04()

    if(opt=="5"):
        menu.P05()

    if(opt=="6"):
        menu.tanque=str(sys.argv[2])
        menu.sensor=str(sys.argv[3])
        menu.P06()
else:
    menu.print_welcome()

    menu.print_menu()
    menu.imprimir_prompt()
    resp=input()

    while(not resp=="exit"):
        menu.procesar_respuesta(resp.split(' '))
        menu.imprimir_prompt()
        resp=input()


