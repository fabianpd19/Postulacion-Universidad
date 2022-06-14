import datetime
from sys import settrace
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class estudiante:
    """
    Recopiación de la información de los aspirantes a la educación superior\n
    Basado en los siguientes lineamientos:
        Reglamentos Senescyt https://admision.senescyt.gob.ec/media/2021/06/acuerdo-_reglamento_del_snna-_21_junio_2021.pdf
        Admisión elnace: https://admision.senescyt.gob.ec/
    ----
    Parámetros:
    ----------
        nombre: str
            nombre del estudiante
        apellido: str
            apellido del estudiante
        cedula: str 
            cedula del estudiante
        puntaje: int 
            puntaje obtenido en el exámen de admisión
    ---
    Métodos:
    -------
    __init__(self, nombre, apellido, cedula, puntaje):
        Construye atributos para la clase estudiante
    ingresoDatos(self):
        Recopilación de datos, pidiéndolos por pantalla
    usuarioContrasena(self)):
        Genera un usuario y contraseña a partir de los datos ingresados
    iniciarSesión(self)):
        Valida datos para el ingreso de sesión (cambia un valor a true para acceder a demás menús)
    """   

    def __init__(self, nombre, apellido, cedula, puntaje): 
        '''
        Construsctores para los respectivos atributos 
        '''
        self.nombre=nombre
        self.apellido=apellido 
        self.cedula=cedula
        self.puntaje=puntaje 
    def ingresoDatos (self):
        """ 
        Recopilación de datos
        """
        self.nombre=str(input("Ingrese su nombre: "))  
        self.apellido=str(input("Ingrese su apellido: "))
         
        #asignamos un valor a la cédula, para evitar un error.
        self.cedula="0" 
        while len(self.cedula)!=10:
             
            #ciclo while para validar que la cédula tenga 10 dígitos 
            self.cedula=input("Ingrese su número de cédula: ")
            if len(self.cedula)==10: 
                '''
                función len: función para determinar la longitud de una cadena (string) 
                '''
                print("[+] Ingreso de datos correcto") 
            else:
                print("[x] Cédula incorrecta, vuelva a ingresar") 
    def usuarioContrasena (self):
        '''
        Método usuarioContrasena: 
        Creación tanto del usuario y contraseña con los 
        datos anteriormente ingresados, estos se basan en 
        el simple uso de cadenas (strings): 
            self.usuarioAspirante: Guarda el nombre de usuario del aspirante 
            self.constrasenaAspirante: Guarda el nombre de usuario del aspirante
        ''' 
        #uso de strings
        
        #En el usuario concatenamos ciertos caracteres del nombre y el  
        self.usuarioAspirante=self.nombre[0:4:1]+self.apellido[0:3]
        
        #En la contraseña concatemos ciertos caracteres del apellido, la cédula y el nombre con "asp" de aspirante 
        self.contrasenaAspirante=self.apellido[0:3]+self.nombre[0:2]+self.cedula[0:3]+"asp"
        
        #Cambio tanto del usuario como la contraseña a minúsculas para evitar conflictos
        '''
        función lower: se encarga de transformar toda una cadena a minúsculas
        '''
        self.usuarioAspirante=self.usuarioAspirante.lower()
        self.contrasenaAspirante=self.contrasenaAspirante.lower()
    def inicioSesion (self):
        ''''
        Se encarga de la validación de los datos para el respectivo ingreso de sesisón
        '''
        #Usamos una variable boolean para después poder usarla al momento de hacer el ingreso a otra parte del programa
        self.acceder=False
        #Pedir al usuario por pantallal los respectivos datos
        self.user=str(input("Usuario: "))
        self.password=str(input("Contraseña: "))
        #condicional donde se valida un usuario ya ingresado o un usuario resién creado
        if ((self.user == "grupo3" and self.password == "contrasenagrupo3") or (self.user == self.usuarioAspirante and self.password == self.contrasenaAspirante)):
            print("Ingreso correcto")
            #Si hay un inicio de sesión correcto cambiamos la variable boolean y usarla respectivamente en las siguientes funciones
            self.acceder=True
        else:
            print("[x] Usuario o contraseña incorrecta")

class universidad:
    """
    Recopilación de los datos de las universidades
    ---
    Parámetros
    -------
        nombre: str
            Nombre de la institución
        carrera: str
            Carreras universitarias que se encuentran en la institución
        ciudad: str
            Ciudad de donde son cada una de las instituciones
        puntaje: int
            Puntaje de las carreras a postular, para comparar con el puntaje 
    Métodos
    -------
    __init__(self, nombre, carrera, ciudad, puntaje)
        Construye los atributos de las clases
    """
    def __init__(self, nombre, carrera, ciudad, puntaje):
        self.nombre=list(nombre)
        self.carrera=list(carrera)
        self.ciudad=list(ciudad)
        self.puntaje=list(puntaje)

class FeriadoEcuador(HolidayBase):
    """
    Clase para determinar los feriados dentro de Ecuador
    Determina si una fecha en específico es de vacaciones, de una forma rápida y directa
    por ejemplo, en el siguiente enlace tenemos fechas de días festivos en Ecuador:
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    
    Los atributos se heredan de la clase HolidayBase
    """     
    # ISO 3166-2 código para las principales subdiviciones, llamadas provincias
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    # TODO agrega más provincias
    PROVINCES = ["EC-P"]  

    def __init__(self, **kwargs):
        """
        Construcción de cada uno de los atributos para la clase de FeriadoEcuador
        ----
        Atributos:
        prov: str (cadena string)
            Código de provincia según ISO3166-2
        Métodos:
        __init__(self, placa, fecha, tiempo, online=False):
        Construye todos los atributos para el objeto de FeriadoEcuador
        """         
        self.pais = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, anio):
        """
        Revisa si una fecha es feriado
        
        Parametros
        ----------
        anio : str (cadena string)
            año de una fecha
        Returns (Devuelve)
        -------
        Devuelve "True" si una fecha es día festivo
        de lo contraio devuelve el valor de "False"
        """                    
        #Días festivos 
        #Año nuevo 
        self[datetime.date(anio, JAN, 1)] = "Año Nuevo"
        
        # Navidad
        self[datetime.date(anio, DEC, 25)] = "Navidad"
        
        # Semana Santa
        self[easter(anio) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo)"
        self[easter(anio)] = "Día de Pascuas [Easter Day]"
        
        # Carnaval
        total_lent_days = 46
        self[easter(anio) - datetime.timedelta(days=total_lent_days+2)] = "Lunes de carnaval "
        self[easter(anio) - datetime.timedelta(days=total_lent_days+1)] = "Martes de carnaval "
        
        # Labor day
        nombre = "Día Nacional del Trabajo [Labour Day]"
        # (Ley 858/Ley Reformatoria a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae en sábado o martes
        # el descanso obligatorio irá al inmediato anterior viernes o lunes 
        # respectivamente
        if anio > 2015 and datetime.date(anio, MAY, 1).weekday() in (5,1):
            self[datetime.date(anio, MAY, 1) - datetime.timedelta(days=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906)) si el feriado cae en domingo
        # el descanso obligatorio irá al lunes siguiente
        elif anio > 2015 and datetime.date(anio, MAY, 1).weekday() == 6:
            self[datetime.date(anio, MAY, 1) + datetime.timedelta(days=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en miércoles o jueves
        # Se cambiará al viernes de esa semana
        elif anio > 2015 and  datetime.date(anio, MAY, 1).weekday() in (2,3):
            self[datetime.date(anio, MAY, 1) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(anio, MAY, 1)] = nombre
        
        # Batalla de Pichincha, las reglas son iguales a las del día del trabajo
        nombre = "Batalla del Pichincha "
        if anio > 2015 and datetime.date(anio, MAY, 24).weekday() in (5,1):
            self[datetime.date(anio, MAY, 24).weekday() - datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and datetime.date(anio, MAY, 24).weekday() == 6:
            self[datetime.date(anio, MAY, 24) + datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, MAY, 24).weekday() in (2,3):
            self[datetime.date(anio, MAY, 24) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(anio, MAY, 24)] = nombre        
        
        # Primer grito de la independencia, las reglas son iguales a las del día del trabajo
        nombre = "Primer Grito de la Independencia"
        if anio > 2015 and datetime.date(anio, AUG, 10).weekday() in (5,1):
            self[datetime.date(anio, AUG, 10)- datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and datetime.date(anio, AUG, 10).weekday() == 6:
            self[datetime.date(anio, AUG, 10) + datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, AUG, 10).weekday() in (2,3):
            self[datetime.date(anio, AUG, 10) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(anio, AUG, 10)] = nombre       
        
        # Independencia de Guayaquil, las reglas son iguales a las del día del trabajo
        nombre = "Independencia de Guayaquil "
        if anio > 2015 and datetime.date(anio, OCT, 9).weekday() in (5,1):
            self[datetime.date(anio, OCT, 9) - datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and datetime.date(anio, OCT, 9).weekday() == 6:
            self[datetime.date(anio, OCT, 9) + datetime.timedelta(days=1)] = nombre
        elif anio > 2015 and  datetime.date(anio, MAY, 1).weekday() in (2,3):
            self[datetime.date(anio, OCT, 9) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(anio, OCT, 9)] = nombre        
        
        # Día de los difuntos
        namedd = "Día de los difuntos" 
        # Independencia de Cuenca
        nameic = "Independencia de Cuenca"
        #(Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906)) 
        # Para festivos nacionales y/o locales que coincidan en días corridos, 
        #Las siguientes reglas se aplicarán:
        if (datetime.date(anio, NOV, 2).weekday() == 5 and  datetime.date(anio, NOV, 3).weekday() == 6):
            self[datetime.date(anio, NOV, 2) - datetime.timedelta(days=1)] = namedd
            self[datetime.date(anio, NOV, 3) + datetime.timedelta(days=1)] = nameic     
        elif (datetime.date(anio, NOV, 3).weekday() == 2):
            self[datetime.date(anio, NOV, 2)] = namedd
            self[datetime.date(anio, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(anio, NOV, 3).weekday() == 3):
            self[datetime.date(anio, NOV, 3)] = nameic
            self[datetime.date(anio, NOV, 2) + datetime.timedelta(days=2)] = namedd
        elif (datetime.date(anio, NOV, 3).weekday() == 5):
            self[datetime.date(anio, NOV, 2)] =  namedd
            self[datetime.date(anio, NOV, 3) - datetime.timedelta(days=2)] = nameic
        elif (datetime.date(anio, NOV, 3).weekday() == 0):
            self[datetime.date(anio, NOV, 3)] = nameic
            self[datetime.date(anio, NOV, 2) + datetime.timedelta(days=2)] = namedd
        else:
            self[datetime.date(anio, NOV, 2)] = namedd
            self[datetime.date(anio, NOV, 3)] = nameic  
            
        # Fundación de Quito, solo aplicará para la provincia de Pichincha
        # Se aplican las mismas reglas que el día de trabajo
        nombre = "Fundación de Quito "        
        if self.prov in ("EC-P"):
            if anio > 2015 and datetime.date(anio, DEC, 6).weekday() in (5,1):
                self[datetime.date(anio, DEC, 6) - datetime.timedelta(days=1)] = nombre
            elif anio > 2015 and datetime.date(anio, DEC, 6).weekday() == 6:
                self[(datetime.date(anio, DEC, 6).weekday()) + datetime.timedelta(days=1)] =nombre
            elif anio > 2015 and  datetime.date(anio, DEC, 6).weekday() in (2,3):
                self[datetime.date(anio, DEC, 6) + rd(weekday=FR)] = nombre
            else:
                self[datetime.date(anio, DEC, 6)] = nombre

class test:
    '''
    Clase para determinar los respectivos crónogramas
        Basado en el cronograma de la SENESCYT: https://admision.senescyt.gob.ec/
    ---
    Atributos
    ------
    fecha: str
        Fecha a ingresar (año, mes y día)
        Sigue el respectivo formado: YYYY-MM-DD
    online: boolean
        if online == True Se utilizará la API de días festivos abstractos
    Métodos
    ------
    __init__(self, fecha, online=false):
        Constructor para todos los atributos
    fecha(self):
        Obtiene el valor del atributo de fecha
    fecha(self, value):
        Establece el valor del atributo de fecha

    '''
    def __init__(self, fecha, online=False):
        self.fecha=fecha
        self.online=online
    
    @property
    def fecha(self):
        return self._fecha
    
    @fecha.setter
    def fecha(self, value):
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe seguir el siguiente fomrato: YYYY-MM-DD (e.g.: 2021-04-02)') from None
        self._fecha = value

    def __esFeriado(self, fecha, online):
        """
        Checks if date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador
        if online == True it will use a REST API, otherwise it will generate the holidays of the examined year
        
        Parameters
        ----------
        date : str
            It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22
        online: boolean, optional
            if online == True the abstract public holidays API will be used        
        Returns
        -------
        Returns True if the checked date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador, otherwise False
        """            
        y, m, d = fecha.split('-')

        if online:
            # abstractapi Holidays API, free version: 1000 requests per month
            # 1 request per second
            # retrieve API key from enviroment variable
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # This means there is a missing API key
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # if there is no holiday we get an empty array
                return False
            # Fix Maundy Thursday incorrectly denoted as holiday
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = FeriadoEcuador(prov='EC-P')
            return fecha in ecu_holidays
        
    def condicionFecha (self):
        # Check if date is a holiday
        if self.__esFeriado(self.fecha, self.online):
            return True
        return False


def main():
    opcion=int 
    while opcion!=5: 
        #menú a mostrar 
        print("╔═══════════════════════════════════╗")
        print("║Proceso de ingreso a la universidad║") 
        print("╚═══════════════════════════════════╝")
        print("1. Iniciar sesión") 
        print("2. Registrarse") 
        print("3. Ver cronogramas de inscripción") 
        print("4. Ver universidades a postular")
        #opciones a ingresar 
        opcion=int(input("Elija una opción: ")) 
        #opcion 1 
        if opcion == 1: 
            opcionInicioSesion() 
        #opcion 2 
        elif opcion == 2:
            opcionRegistroSesion() 
        #opcion 3 
        elif opcion == 3: 
            opcionRegistroSesion() 
        #opción 4 
        elif opcion == 4: 
            opcionMostrarCarrerars()
        elif opcion == 5:
            print("Saliendo...")
            enter=str(input("Presione enter para continuar"))
        else:
            print("[x] Opción invalida, elija una opción correcta")
            enter=str(input("Presione enter para continuar"))

def opcionInicioSesion (): #opción de inicio se sesión
    '''
    Inicio de sesión
    Llamamos a los métodos respectivamente antes comentados 
    para el ingreso de sesión
    '''
    print("\n──────────────────────")
    print("Inicio de sesión")
    #funcioin usuarioContrasena para dar valores al usuario y contraseña y no marcar error
    aspirante.usuarioContrasena()
    #funcion para iniciar sesión
    aspirante.inicioSesion()
    if  aspirante.acceder == True:
        postulacion()
    else:
        enter=str(input("Presione enter para continuar..."))

def opcionRegistroSesion (): #opcion del registro de sesión
    '''
    Registro: 
    Se realiza el respectivo registo de los datos del aspirante mediante 
    los métodos en la clase 
    ingresoDatos=recoplicación de datos; nombre, apellido, cedula. 
    usuarioContrasena=regresa el nombre de usuario y contraseña para poder iniciar sesión 
    '''
    print("\n──────────────────────")
    print("Registro")
    #método ingreso de datos
    aspirante.ingresoDatos()
    #método para la creación del usuario y contraseña
    aspirante.usuarioContrasena()
    #se muestra por pantalla las credenciales para el ingreso de sesión
    print("Usuario:", aspirante.usuarioAspirante)
    print("Contrasena:", aspirante.contrasenaAspirante)
    enter=str(input("Presione enter para continuar")) 

def opcionCronograma (): #opción para mostrar al crónograma 
    print("Cronogramas")
    print("────────────────────")
    print("Tercera postulación") #etapa 9
    print("31 de mayo y 1 de junio\nEtapa 9") 
    print("────────────────────")
    print("Segunda aceptación de cupo\n25 y 26 de mayo\nEtapa 8") #etapa 8 
    print("────────────────────")
    print("Segunda postulación\n20 al 22 de mayo\nEtapa 7") #etapa 7 
    print("────────────────────")
    print("Aceptación de cupo\n10 y 11 de mayo\nEtapa 6") #etapa 6 
    print("────────────────────")
    print("Primera postulación\nDel 4 al 6 de mayo\nEtapa 5") #etapa 5 
    print("────────────────────")
    print("Test Transformar\n23 de marzo\nEtapa 4") #etapa 4 
    print("────────────────────")
    #etapa 3 no considerada
    print("Programa de nivelación general Transformándonos primer periodo 2022\nA partir del 25 de enero\nEtapa 2") #etapa 2
    print("────────────────────")
    print("Retorno al Acceso a la Educación Superior\nDel 2 al 4 de diciembre\nEtapa 1") #etapa 1
    enter=str(input("Presione enter para continuar")) 

def opcionMostrarCarrerars ():
    '''
    Cumple casi con el mismo objetivo de la funcion postulacion 
    pero esta solo se encarga de mostrar la información de las universidades 
    a postular 
    información recopilada de = https://drive.google.com/file/d/1jVqexdOxCfdSbMaX_Qhf0b-Tj4wlnPjo/view 
    nombreCarrera [puntajeCarrear] 
    '''
    opcionPostulacion=int
    print("Carreras")
    while opcionPostulacion!=4:
        print("Universidades:")#universidades a postular
        print("1. Universidad Central del Ecuador") 
        print("2. Universidad de guayaquil") 
        print("3. Universidad Técnica en Ambato") 
        opcionPostulacion=int(input("Ingrese una opción: ")) #carreraas a postular 
        if opcionPostulacion == 1: #carrearas universidad 1 
            print("1. Administración de Empresas [825]") 
            print("2. Administración Pública [802]")
            print("3. Arquitectura [898]")
        elif opcionPostulacion == 2: #carrearas universidad 2
            print("Administración y Suerpvisión Educativa (Ciencias de la Educación) [772]")
            print("Bibliotecología y Archivología [662]")
            print("Biología [732]")
            print("Ciencias de la Educación y Desarrollo Comunitario Ambiental [735]") 
            print("Ciencias Químicas [704]") 
            print("Comercio Exterior [760]") 
        elif opcionPostulacion == 3: #carrearas universidad 3 
            print("Comunicacón Social [792]") 
            print("Contabilidad y Auditoría [819]") 
            print("Derecho [835]") 
            print("Ingeniería Bioquimica [809]") 
            print("Ingeniería Civil [871]") 
            print("Ingenieria Electrónica y Comunicaciones [783]") 
            print("Ingeniería en Alimentos [799]") 
        elif opcionPostulacion == 4: #salir
            print("Saliendo...")
            enter=str(input("Presione enter para continuar"))
    enter=str(input("Presione enter para continuar"))

def postulacion():
    '''
    Función Postulación:
    Función cuyo fin tendrá comparar el puntaje del eestudiante 
    con el de las respectivas universidades a postuarle y retonar como resultado 
    si se postuló correctamente o no 
    información recopilada de: https://drive.google.com/file/d/1jVqexdOxCfdSbMaX_Qhf0b-Tj4wlnPjo/view
    ''' 
    #variable para elegir el menú 
    opcionPostulacion=int 
    #bucle while  
    validacionPostulacion=False
    while opcionPostulacion!=4:
        '''
        Validación opciones dentro del menú
        '''
        print("Bienvenido", aspirante.nombre, aspirante.apellido) 
        #Se pide por pantalla el puntaje alcanzado en el examen de admisión 
        aspirante.puntaje=int(input("Ingrese el puntaje adquirido: ")) 
        '''
        Universidades que se tomaron de ejemplo para la  
        respectiva postulación del aspirante 
        '''
        #Universidades a postular: 
        print("Universidades:")
        print("1. Universidad Central del Ecuador") 
        print("2. Universidad de Guayaquil") 
        print("3. Universidad Técnica en Ambato") 
        while validacionPostulacion==True:
            opcionPostulacion=int(input("Ingrese una opción: ")) 
            if opcionPostulacion<=1000:
                validacionPostulacion=True
            else:
                print("[!] Ingrese un valor menor a 1000")
                enter=str(input("Presione enter para continuar")) 
                validacionPostulacion=False 
        #menú if
        if opcionPostulacion == 1: 
            #carreras postular
            print("1. Administración de Empresas [825]") 
            print("2. Administración Pública [802]") 
            print("3. Arquitectura [898]")
            #puntajes de cada uno de las universidades 
            uceAdminEmpresas=825 
            uceAdminPublica=802 
            uceArquitectura=898 
            opcionUPostulacion=int(input("Elija la opcion a postular: ")) 
            #menu de cada una de las carreras a postular 
            if opcionUPostulacion == 1:  #postulacion carrera 1 
            #menu de cada una de las carreras a postular 
                if aspirante.puntaje>=uceAdminEmpresas:
                    #condicional para determinar si el puntaje es valido para postular o no 
                    print("[+] Correctamente postulado") 
                    break
                else:
                    print("[-] Puntaje no apto para la postulación") 
            elif opcionUPostulacion == 2: #postulacion carrera 2
                if aspirante.puntaje>=uceAdminPublica: 
                    print("[+] Correctamente postulado") 
                    break
                else:
                    print("[-] Puntaje no apto para la postulación")
            elif opcionUPostulacion == 3: #postulacion carrera 3
                if aspirante.puntaje>=uceArquitectura:
                    print("[+] Correctamente postulado")
                    break
                else:
                    print("[-] Puntaje no apto para la postulación")
        elif opcionPostulacion == 2: #postulacion universidad 2
        #universidad 2 
            print("1. Administración y Suerpvisión Educativa (Ciencias de la Educación) [772]")
            print("2. Bibliotecología y Archivología [662]")
            print("3. Biología [732]")
            print("4. Ciencias de la Educación y Desarrollo Comunitario Ambiental [735]")
            print("5. Ciencias Químicas [704]")
            print("6. Comercio Exterior [760]")
            ugAdministracioEducativa=772
            ugBibliotegologia=662
            ugBiologia=732
            ugCienciasEducacion=735
            ugCienciasQuimicas=704
            comercioExterior=760
            opcionUPostulacion=int(input("Elija la opcion a postular"))
            if opcionUPostulacion == 1: #postulacion carrera 1
                if aspirante.puntaje>=ugAdministracioEducativa:
                    print("[+] Correctamente postulado")
                    break
                else:
                    print("[-] Puntaje no apto para la postulación")
            elif opcionUPostulacion == 2: #postulacion carrera 2
                if aspirante.puntaje>=ugBibliotegologia:
                    print("[+] Correctamente postulado") 
                    break
                else:
                    print("[-] Puntaje no apto para la postulación") 
            elif opcionUPostulacion == 3: #postulacion carrera 3 
                if aspirante.puntaje>=ugBiologia:
                    print("[+] Correctamente postulado") 
                    break
                else:
                    print("[-] Puntaje no apto para la postulación") 
            elif opcionUPostulacion == 4: #postulacion carrera 4 
                if aspirante.puntaje>=ugCienciasEducacion: 
                    print("[+] Correctamente postulado")
                    break 
                else:
                    print("[-] Puntaje no apto para la postulación") 
            elif opcionUPostulacion == 5: #postulacion carrera 5 
                if aspirante.puntaje>=ugCienciasQuimicas: 
                    print("[+] Correctamente postulado") 
                    break
                else:
                    print("[-] Puntaje no apto para la postulación") 
            elif opcionUPostulacion == 6: #postulacion carrera 6 
                if aspirante.puntaje>=comercioExterior: 
                    print("[+] Correctamente postulado") 
                    break
                else:
                    print("[-] Puntaje no apto para la postulación")
        elif opcionPostulacion == 3: #postulacion universidad 3 
        #universidad 3
            print("1. Comunicacón Social [792]") 
            print("2. Contabilidad y Auditoría [819]") 
            print("3. Derecho [835]") 
            print("4. Ingeniería Bioquimica [809]") 
            print("5. Ingeniería Civil [871]")
            print("6. Ingenieria Electrónica y Comunicaciones [783]") 
            print("7. Ingeniería en Alimentos [799]")
            opcionUPostulacion=int(input("Elija la opcion a postular: "))
            utaComunicacion=792
            utaContabilidad=819
            utaDerecho=835 
            utaIngeniriaBioquimia=809
            utaIngenieraCivl=871
            utaIngenieraEyC=783
            utaIngenieriaAlimentos=799

            if opcionUPostulacion == 1:
                if aspirante.puntaje>=utaComunicacion: #postulacion carrera 1
                    print("[+] Correctamente postulado") 
                    break
                else: 
                    print("[-] Puntaje no apto para la postulación")
            elif opcionUPostulacion == 2: #postulacion carrera 2
                if aspirante.puntaje>=utaContabilidad: 
                    print("[+] Correctamente postulado")
                    break
                else:
                    print("[-] Puntaje no apto para la postulación") 
            elif opcionUPostulacion == 3: #postulacion carrera 3
                if aspirante.puntaje>=utaDerecho:
                    print("[+] Correctamente postulado") 
                    break
                else: 
                    print("[-] Puntaje no apto para la postulación") 
            elif opcionUPostulacion == 4: #postulacion carrera 4
                if aspirante.puntaje>=utaIngeniriaBioquimia: 
                    print("[+] Correctamente postulado")
                    break
                else:
                    print("[-] Puntaje no apto para la postulación")
            elif opcionUPostulacion == 5: #postulacion carrera 5 
                if aspirante.puntaje>=utaIngenieraCivl:
                    print("[+] Correctamente postulado")
                    break
                else: 
                    print("[-] Puntaje no apto para la postulación")
            elif opcionUPostulacion == 6: #postulacion carrera 6
                if aspirante.puntaje>=utaIngenieraEyC:
                    print("[+] Correctamente postulado")
                    break 
                else:
                    print("[-] Puntaje no apto para la postulación")  
            elif opcionUPostulacion == 7: #postulacion carrera 7
                if aspirante.puntaje>=utaIngenieriaAlimentos: 
                    print("[+] Correctamente postulado")
                    break
                else:
                    print("[-] Puntaje no apto para la postulación") 
        #opcion para salir del programa
        elif opcionPostulacion == 4:
            print("Saliendo...")
        else:
            print("[x] Ingrese una opción correcta")

 
if __name__ == '__main__': #main  
    
    # fecha=input("Ingrese fecha con el siguiente formato YYYY-MM-DD: ")
    # online=False
    # feriados=test(fecha, online)
    # if feriados.condicionFecha():
    #     print("feriado")
    # else:
    #     print("no es feirado?")
    ''' 
    Instancia de la clase estudiante:
    ''' 
    puntaje=int
    aspirante=estudiante("ejemplo","ejemplo","1234512345", puntaje) 
    #opcion=variable para validar opciones en el menú
    opcion=int
    #bucle while, para la validación opciones en el menú 
    main() #menú principal 