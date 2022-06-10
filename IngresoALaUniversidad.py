class estudiante:
    '''
    Clase estudiante:
    La clase estudiante dentro de este programa tendrá como objetivo
    guardar la información de los aspirantes a la educación superior
    entre los principales atributos:
        nombre=str
        apellido=str
        cedula=str
    Es así que con esta información se tomará como referencia usar 
    los reglamentos que dispone la SENESCYT (Secretaría de Educación Superior, Ciencia, Tecnología e Innovación)
    Reglamentos Senescyt https://admision.senescyt.gob.ec/media/2021/06/acuerdo-_reglamento_del_snna-_21_junio_2021.pdf
    Admisión elnace: https://admision.senescyt.gob.ec/
    '''

    def __init__(self, nombre, apellido, cedula, puntaje):
        '''
        Construsctores para los respectivos atributos de la clase estudiante
        '''
        self.nombre=nombre
        self.apellido=apellido
        self.cedula=cedula
        self.puntaje=puntaje
    def ingresoDatos (self):
        '''
        Método ingresoDatos
        Ingreso de datos.
        Este método tiene como objetivo la recopilación de datos del 
        aspirante, mediante esta información se generará automáticamente 
        el nombre de usuario y la contraseña (método 'usuuarioContrasena')
        '''
        self.nombre=str(input("Ingrese su nombre: "))
        self.apellido=str(input("Ingrese su apellido: "))
        #asignamos un valor a la cédula, pues da un error.
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
                '''
                En caso de que la contraseña no tenga los respectivos 10 dígitos
                Le volverá a pedir al usuario el ingreso de la misma
                '''
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
        #En el usuario concatenamos ciertos caracteres del nombre y el apellido
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
        Método inicioSesion
        Método el cual se encarga de la validación de los datos para el respectivo ingreso de sesisón
        '''
        #Usamos una variable boolean para después poder usarla al momento de hacer el ingreso a otra parte del programa
        self.acceder=False
        #Pedir al usuario por pantallal los respectivos datos
        self.user=str(input("Usuario: "))
        self.password=str(input("Contraseña: "))
        '''
        Dentro del if encontramos 3 condiciones:
            1. Iniciamos sesión como ejemplo, para ahorrar tiempo con el ingreso de datos
            2. Se inicia sesión con los datos del usuario y contraseña creada en la anterior función
            3. Estas condiciones las tenemos dentro de un "or" quiere decir, o se cumple una condición, o se cumple la otra
        '''
        if ((self.user == "grupo3" and self.password == "contrasenagrupo3") or (self.user == self.usuarioAspirante and self.password == self.contrasenaAspirante)):
            print("Ingreso correcto")
            #Si hay un inicio de sesión correcto cambiamos la variable boolean y usarla respectivamente en las siguientes funciones
            self.acceder=True
        else:
            '''
            En caso de que que el usuario o contraseña esté mal
            lanzará este mensaje
                No se usa un ciclo repetitivo respectivamente, puesto que
                en un hipotetico caso alguien no tenga un usuario y contraseña
            '''
            print("[x] Usuario o contraseña incorrecta")

class universidad:
    '''
    Clase universidad:
    Esta clase respectivamente tratará de obtener la información
    de universidades que se usarán como EJEMPLO dentro de este programa
        nombre: str
        carrera: str
        ciudad: str
    '''
    def __init__(self, nombre, carrera, ciudad, puntaje):
        self.nombre=list(nombre)
        self.carrera=list(carrera)
        self.ciudad=list(ciudad)
        self.puntaje=list(puntaje)

'''
instanciamos la clase estudiante
'''
#variable puntaje, (instanciar para uso en la funcion de postulacion)
puntaje=int
aspirante=estudiante("ejemplo","ejemplo","1234512345", puntaje)
#opcion=variable para validar opciones en el menú
opcion=int
#bucle while, para la validación opciones en el menú

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
        opcionPostulacion=int(input("Ingrese una opción: "))
        #menú if
        '''
        Menú respectivo para cada universidad
        en cada uno de estos estarán las respectivas carreras de cada universidad
        así como también las notas de postulación
        '''
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
            '''
            Condicional if
                Condicional para determinar si
                la contraseña está correcta nos permitá
                ir al portal de postulación de lo contrario 
                nos regresará al menú principal
            '''
            if  aspirante.acceder == True:
                postulacion()
            else:
                enter=str(input("Presione enter para continuar..."))
        #opcion 2
        elif opcion == 2:
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
        #opcion 3
        elif opcion == 3:
            '''
            Esta opción se base simplemente en el cronograma
            que usa la SENESCYT para el respectivo proceso
            antes y después del ingreso a la educación 
            superior
            recopilado de: https://admision.senescyt.gob.ec/
            '''
            #cronograma a mostrar 
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
        #opción 4
        elif opcion == 4:
            '''
            Cumple casi con el mismo objetivo de la funcion postulacion
            pero esta solo se encarga de mostrar la información de las universidades
            a postular
            información recopilada de = https://drive.google.com/file/d/1jVqexdOxCfdSbMaX_Qhf0b-Tj4wlnPjo/view
            nombreCarrera [puntajeCarrera]
            '''
            opcionPostulacion=int
            print("Carreras")
            while opcionPostulacion!=3:
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
            enter=str(input("Presione enter para continuar"))
        elif opcion == 5:
            print("Saliendo...")
            enter=str(input("Presione enter para continuar"))
        else:
            print("[x] Opción invalida, elija una opción correcta")
            enter=str(input("Presione enter para continuar"))

#Invocación del menú main
main()