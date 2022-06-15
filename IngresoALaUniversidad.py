import datetime
from sys import settrace
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC, JUN
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
    usuarioContrasena(self)):
        Genera un usuario y contraseña a partir de los datos ingresados
    inicioSesion(self)):
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

    def usuarioContrasena (self):
        '''
        Método usuarioContrasena: 
        Creación tanto del usuario y contraseña con los datos ingresados o asignados en la instancia
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
            print("[+] Ingreso exitoso")
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
    postularUniversidad(self, puntajeEstudiante):
        Condicional para determinar si puede postular a la carrera o no
    """
    def __init__(self, nombre, carrera, ciudad, puntaje):
        self.nombre=nombre
        self.carrera=carrera
        self.ciudad=ciudad
        self.puntaje=int(puntaje)
    def postularUniversidad (self, puntajeEstudiante):
        self.puntajeEstudiante=puntajeEstudiante
        if puntajeEstudiante>=self.puntaje:
            print("[+] Postulación exitosa")
        else:
            print("[-] Lamentablemente no cuentas con el puntaje requirido")


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
        #Cronograma en base a: https://admision.senescyt.gob.ec/
        #3ra Postulación 1ra Fecha:
        self[datetime.date(anio, MAY, 31)] = "Tercera Postulación"

        #3ra Postulación 2da Fecha:
        self[datetime.date(anio, JUN, 1)] = "Tercera Postulación"

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

class fechaEcuador:
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
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador
        si online == True utilizará una API REST, de lo contrario generará los días festivos del año examinado
        
        Parametros
        ----------
        fecha : str
            Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
        online: boolean, opcional
            si online == True se utilizará la API de días festivos abstractos
        Retornos 
        -------
        Retorna True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario False
        """          
        y, m, d = fecha.split('-')

        if online:
            # API de vacaciones abstractapi, versión gratuita: 1000 solicitudes por mes
            # 1 solicitud por segundo
            # recuperar la clave API de la variable de entorno
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # Esto significa que falta una clave de API.
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # si no hay vacaciones, obtenemos una matriz vacía
                return False
            # Arregla el Jueves Santo incorrectamente denotado como feriado
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = FeriadoEcuador(prov='EC-P')
            return fecha in ecu_holidays
        
    def condicionFecha (self):
        # Comprobar si la fecha es un día festivo
        if self.__esFeriado(self.fecha, self.online):
            return True
        return False


def opcionInicioSesion (): #opción de inicio se sesión
    '''
    Validación de datos ingresados dentro de la clase estudiante
    ----
    Valida el usuario y contraseña creada con información que pide por pantalla
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


def opcionCronograma (): #opción para mostrar al crónograma
    '''
    Muestra por pantalla el cronograma correspondiente\n
    Imprime por pantalla las fechas y a que fase del proceso de admisión pertenece
    ----
    Información recopilada de: https://admision.senescyt.gob.ec/
    '''
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
    Muestra por pantalla la posibles universidades a postular \n 
    Información recopilada de = https://drive.google.com/file/d/1jVqexdOxCfdSbMaX_Qhf0b-Tj4wlnPjo/view  
    '''
    opcionPostulacion=int
    while opcionPostulacion!=4:
        print("\n──────────────────────")
        print("Universidades:")#universidades a postular
        print("1. Universidad Central del Ecuador") 
        print("2. Universidad de Guayaquil") 
        print("3. Universidad Técnica de Ambato") 
        print("4. Salir") 
        print("──────────────────────")
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
    Almacenamiento de cada universidad ingresada en el sistema\n
    Información recopilada de: https://drive.google.com/file/d/1jVqexdOxCfdSbMaX_Qhf0b-Tj4wlnPjo/view
    ''' 
    #variable para elegir el menú
    fecha=input("Ingrese la fecha: \nSiga el siguiente formato: YYYY-MM-DD:\n")
    online=False
    feriados=fechaEcuador(fecha, online)
    if feriados.condicionFecha():
        print("feriado")
        print(feriados._fecha) 
        opcionPostulacion=int 
        #bucle while  
        while opcionPostulacion!=4:
            '''
            Universidades que se tomaron de ejemplo para la  
            respectiva postulación del aspirante 
            '''
            #Universidades a postular: 
            print("\n──────────────────────")
            print("Universidades:")
            print("1. Universidad Central del Ecuador") 
            print("2. Universidad de Guayaquil") 
            print("3. Universidad Técnica de Ambato")
            print("4. Salir") 
            print("──────────────────────")
            print(f'Bienvenido(a) {aspirante.nombre} {aspirante.apellido}, antes de postular recuerde que su puntaje es {aspirante.puntaje}.') 
            opcionValidar=(input("Ingrese una opción: "))
            if opcionValidar.isnumeric():
                opcionValidar=int(opcionValidar)
                opcionPostulacion=opcionValidar
            else:
                print("[!] Ingrese un número")
            #menú if
            if opcionPostulacion == 1: #postulación universidad 1
                print("\n──────────────────────")
                subMenuPostulacionUniversidad1()
            elif opcionPostulacion == 2: #postulación universidad 2
                print("\n──────────────────────")
                subMenuPostulacionUniversidad2()
            elif opcionPostulacion == 3: #postulación universidad 3 
                print("\n──────────────────────")   
                subMenuPostulacionUniversidad3()
            else:
                print("[x] Opción invalida, elija una opción correcta")
    else:
        print("¡No nos encontramos en servicio, vuela siguiendo el crónograma!")

#Universidad 1
#Universidad Central del Ecuador
def subMenuPostulacionUniversidad1():
    '''
    Función donde se instancia la clase universidad dependiendo de la universidad, carrera, ciudad y puntaje.
    ---
    nombre: nombre universidad
    carrera: carrera de la universidad
    ciudad: ciudad universidad
    puntaje: puntaje de la carrera
    '''
    opcionUPostulacion=int
    while opcionUPostulacion !=4:
        print("1. Administración de Empresas [825]") 
        print("2. Administración Pública [802]") 
        print("3. Arquitectura [898]")
        print("4. Salir")
        opcionValidar=(input("Ingrese una opción: "))
        if opcionValidar.isnumeric():
            opcionValidar=int(opcionValidar)
            opcionUPostulacion=opcionValidar
        else:
            print("[!] Ingrese un número") 
        #menu de cada una de las carreras a postular 
        if opcionUPostulacion == 1:  #postulacion carrera 1 
            print("1. Administración de Empresas [825]")
            universidadP=universidad("Universidad Central del Ecuador", "Administración de Empresas", "Quito", 825)
            universidadP.postularUniversidad(aspirante.puntaje) 
        elif opcionUPostulacion == 2: #postulacion carrera 2
            print("2. Administración Pública [802]") 
            universidadP=universidad("Universidad Central del Ecuador", "Administración Pública", "Quito", 802)
            universidadP.postularUniversidad(aspirante.puntaje) 
        elif opcionUPostulacion == 3: #postulacion carrera 3
            print("3. Arquitectura [898]")
            universidadP=universidad("Universidad Central del Ecuador", "Arquitectura", "Quito", 898)
            universidadP.postularUniversidad(aspirante.puntaje)
        elif opcionUPostulacion == 4:
            print("Saliendo...")
        else:
            print("[x] Opción invalida, elija una opción correcta")

#Universidad 2
#Universidad de Guayaquil
def subMenuPostulacionUniversidad2():
    opcionUPostulacion=int
    while opcionUPostulacion !=7:
        print("1. Administración y Suerpvisión Educativa (Ciencias de la Educación) [772]")
        print("2. Bibliotecología y Archivología [662]")
        print("3. Biología [732]")
        print("4. Ciencias de la Educación y Desarrollo Comunitario Ambiental [735]")
        print("5. Ciencias Químicas [704]")
        print("6. Comercio Exterior [760]")
        print("7. Salir")
        opcionValidar=(input("Ingrese una opción: "))
        if opcionValidar.isnumeric():
            opcionValidar=int(opcionValidar)
            opcionUPostulacion=opcionValidar
        else:
            print("[!] Ingrese un número") 
        #menu de cada una de las carreras a postular 
        if opcionUPostulacion == 1:  #postulacion carrera 1 
            print("1. Administración y Suerpvisión Educativa (Ciencias de la Educación) [772]")
            universidadP=universidad("Universidad de Guayaquil", "Administración de Empresas", "Guayaquil", 722)
            universidadP.postularUniversidad(aspirante.puntaje) 
        elif opcionUPostulacion == 2: #postulacion carrera 2
            print("2. Bibliotecología y Archivología [662]") 
            universidadP=universidad("Universidad de Guayaquil", "Bibliotecología y Archivología", "Guayaquil", 662)
            universidadP.postularUniversidad(aspirante.puntaje) 
        elif opcionUPostulacion == 3: #postulacion carrera 3
            print("3. Biología [732]")
            universidadP=universidad("Universidad de Guayaquil", "Biología", "Guayaquil", 732)
            universidadP.postularUniversidad(aspirante.puntaje) 
        elif opcionUPostulacion == 4: #postulacion carrera 4
            print("4. Ciencias de la Educación y Desarrollo Comunitario Ambiental [735]")
            universidadP=universidad("Universidad de Guayaquil", "Ciencias de la Educación y Desarrollo Comunitario Ambiental", "Guayaquil", 735)
            universidadP.postularUniversidad(aspirante.puntaje)
        elif opcionUPostulacion == 5: #postulacion carrera 5
            print("5. Ciencias Químicas [704]")
            universidadP=universidad("Universidad de Guayaquil", "Ciencias Químicas", "Guayaquil", 704)
            universidadP.postularUniversidad(aspirante.puntaje)
        elif opcionUPostulacion == 6: #postulacion carrera 6
            print("6. Comercio Exterior [760]")
            universidadP=universidad("Universidad de Guayaquil", "Comercio Exterior", "Guayaquil", 760)
            universidadP.postularUniversidad(aspirante.puntaje)
        elif opcionUPostulacion == 7:
            print("Saliendo...")
        else:
            print("[x] Opción invalida, elija una opción correcta")

#Universidad 3
#Universidad Técnica de Ambato
def subMenuPostulacionUniversidad3():
    opcionUPostulacion=int
    while opcionUPostulacion !=8:
        print("1. Comunicacón Social [792]") 
        print("2. Contabilidad y Auditoría [819]") 
        print("3. Derecho [835]") 
        print("4. Ingeniería Bioquimica [809]") 
        print("5. Ingeniería Civil [871]")
        print("6. Ingenieria Electrónica y Comunicaciones [783]") 
        print("7. Ingeniería en Alimentos [799]")
        print("8. Salir")
        opcionValidar=(input("Ingrese una opción: "))
        if opcionValidar.isnumeric():
            opcionValidar=int(opcionValidar)
            opcionUPostulacion=opcionValidar
        else:
            print("[!] Ingrese un número") 
        #menu de cada una de las carreras a postular 
        if opcionUPostulacion == 1:  #postulacion carrera 1 
            print("1. Comunicacón Social [792]")
            universidadP=universidad("Universidad Técnica de Ambato", "Comunicación Social", "Ambato", 792)
            universidadP.postularUniversidad(aspirante.puntaje) 
        elif opcionUPostulacion == 2: #postulacion carrera 2
            print("2. Contabilidad y Auditoría [819]") 
            universidadP=universidad("Universidad Técnica de Ambato", "Contabilidad y Auditoría", "Ambato", 819)
            universidadP.postularUniversidad(aspirante.puntaje) 
        elif opcionUPostulacion == 3: #postulacion carrera 3
            print("3. Derecho [835]")
            universidadP=universidad("Universidad Técnica de Ambato", "Derecho", "Ambato", 835)
            universidadP.postularUniversidad(aspirante.puntaje) 
        elif opcionUPostulacion == 4: #postulación carrera 4
            print("4. Ingeniería Bioquimica [809]")
            universidadP=universidad("Universidad Técnica de Ambato", "Ingeniería Bioquimica", "Ambato", 809)
            universidadP.postularUniversidad(aspirante.puntaje)
        elif opcionUPostulacion == 5: #postulación carrera 5
            print("5. Ingeniería Civil [871]")
            universidadP=universidad("Universidad Técnica de Ambato", "Ingeniería Civil", "Ambato", 871)
            universidadP.postularUniversidad(aspirante.puntaje)
        elif opcionUPostulacion == 6: #postulación carrera 6
            print("6. Ingenieria Electrónica y Comunicaciones [783]")
            universidadP=universidad("Universidad Técnica de Ambato", "Ingenieria Electrónica y Comunicaciones", "Ambato", 783)
            universidadP.postularUniversidad(aspirante.puntaje)
        elif opcionUPostulacion == 7: #postulación carrera 7
            print("7. Ingeniería en Alimentos [799]")
            universidadP=universidad("Universidad Técnica de Ambato", "Ingeniería en Alimentos", "Ambato", 799)
            universidadP.postularUniversidad(aspirante.puntaje)
        elif opcionUPostulacion == 8:
            print("Saliendo...")
        else:
            print("[x] Opción invalida, elija una opción correcta")

#función main
if __name__ == '__main__': #main  
    
    #Instancia de la clase estudiante
    aspirante=estudiante("nombre", "apellido", "cedula", 792) #Asignación de valores para evitar errores

    #Declaración tipo boolean para validación del puntaje dentro de la opción 2
    validacionPostulacion=False

    #Declaración 'opcion' para navegación por el menú principal
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
        print("5. Salir")
        #opciones a ingresar 
        opcionValidar=(input("Ingrese una opción: "))
        if opcionValidar.isnumeric():
            opcionValidar=int(opcionValidar)
            opcion=opcionValidar
        else:
            print("[!] Ingrese un número")
        #opcion 1 
        if opcion == 1: 
            opcionInicioSesion() 
        #opcion 2 
        elif opcion == 2:
            """ 
            Recopilación de datos
            """
            nombre=str(input("Ingrese su nombre: "))  
            apellido=str(input("Ingrese su apellido: "))
                
            #asignamos un valor a la cédula, para evitar un error.
            cedula="0"
            while len(cedula)!=10:
                cedula=input("Ingrese su número de cédula: ")
                if cedula.isnumeric():
                    #ciclo while para validar que la cédula tenga 10 dígitos 
                    if len(cedula)==10: 
                        print("[+] Ingreso de datos correctos") 
                    else:
                        print("[x] Cédula incorrecta, vuelva a ingresar")
                else:
                    print("[!] ¡Solo se permiten números!")
                    cedula='0'

            #validiación de puntaje 'mayor igual a 100 o menor igual a 1000'        
            while validacionPostulacion==False:
                puntaje=input(f'Bienvendio(a) {nombre} {apellido}, a continuación ingrese su puntaje obtenido: ') 
                if puntaje.isnumeric():
                    puntaje=int(puntaje)
                    if puntaje>=100 and puntaje<=1000:
                        print("[+] Ingreso correcto")
                        validacionPostulacion=True
                    else:
                        print("[!] Ingrese un puntaje de postulación válido")
                else:
                    print("[!] Ingrese un puntaje de postulación válido")
                    validacionPostulacion=False 
            
            #Instancia de la clase estudiante con nuevos datos
            aspirante=estudiante(nombre, apellido, cedula, puntaje)
            aspirante.usuarioContrasena()
            print("Usuario:", aspirante.usuarioAspirante)
            print("Contrasena:", aspirante.contrasenaAspirante)
            enter=str(input("Presione enter para continuar")) 
        #opcion 3 
        elif opcion == 3: 
            opcionCronograma() 
        #opción 4 
        elif opcion == 4: 
            opcionMostrarCarrerars()
        elif opcion == 5:
            print("Saliendo...")
            enter=str(input("Presione enter para continuar"))
        else:
            print("[x] Opción invalida, elija una opción correcta")
            enter=str(input("Presione enter para continuar"))