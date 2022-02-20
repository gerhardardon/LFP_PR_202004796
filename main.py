# Menu principal de la app
from tkinter import Tk
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import webbrowser

data = ""
instrucciones = ""
meses = []
años = []
list_ob = []
list_pr = []
list_ca = []
list_ing = []

diccionario = {}
productos = []


class producto:
    def __init__(self, name, price, units, income):
        self.name = name
        self.price = price
        self.units = units
        self.income = income

    def imprimir(self):
        print(self.name)
        print(self.price)
        print(self.units)
        print(self.income)

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_units(self):
        return self.units

    def get_income(self):
        return self.income


def cargar():
    ############### LEER EL ARCHIVO
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = fd.askopenfilename(title="Select file", filetypes=(("Data Files", "*.data"), ("Lfp F1iles", "*.lfp")))
    print(filename)
    file = open(filename, encoding="utf8")
    contenido = file.read()
    ############## "contenido" es la variable que contiene toda la información leída

    return contenido


def analizarVentas():
    ################ ANALIZAR EL ARCHIVO Y SEPARAR
    texto = data
    texto = texto.lower()
    texto = texto.replace('"', '')
    lexema = ""
    lexema2 = ""

    objeto = precio = cantidad = ""

    for x in texto:
        if x == ":":
            global meses
            meses.append(lexema)
            lexema = ""
            continue
        if x == "=":
            global años
            años.append(lexema)
            lexema = ""
            continue
        if x == '[':
            lexema = ""
            continue
        if x == "]":
            comas = 0
            lexema2 = ""
            lexema = lexema + ","

            for i in lexema:
                if i == "," and comas == 0:
                    objeto = lexema2
                    comas = 1
                    lexema2 = ""
                    global list_ob
                    list_ob.append(objeto)
                    continue
                if i == "," and comas == 1:
                    precio = lexema2
                    comas = 2
                    lexema2 = ""
                    global list_pr
                    list_pr.append(float(precio))
                    continue
                if i == "," and comas == 2:
                    cantidad = lexema2
                    lexema2 = ""
                    global list_ca
                    list_ca.append(cantidad)
                    continue
                lexema2 = lexema2 + i

        lexema = lexema + x


def analizarInstrucciones():
    texto = instrucciones
    lexema = ""
    # titulo, tx y ty son opcionales, no siempre vendran

    # elimina todos los espacios
    texto = texto.replace(" ", "")
    texto = texto.replace("?>", ",")
    texto = texto.replace('"', '')
    texto = texto.replace("\n", "")
    texto = texto.lower()

    for x in texto:
        if x == "¿":
            lexema = ""
            continue
        if x == ",":
            print(lexema)

            (k, v) = lexema.split(":")
            global diccionario
            diccionario[k] = v

            lexema = ""
            continue

        lexema = lexema + x

    if ('nombre' in diccionario) == False or ('grafica' in diccionario) == False:
        print("\n##### ERROR, FALTAN DATOS OBLIGATORIOS EN LAS INSTRUCCIONES (NOMBRE,GRAFICA) #####")


def graficar():
    if diccionario.get("grafica") == 'barras':
        plt.bar(list_ob, list_ing)
        if ('titulox' in diccionario) == True:
            plt.xlabel(diccionario.get("titulox"))
        if ('tituloy' in diccionario) == True:
            plt.ylabel(diccionario.get("tituloy"))
        if ('titulo' in diccionario) == True:
            plt.title(diccionario.get("titulo"))

    if diccionario.get("grafica") == 'pie':
        plt.pie(x=list_ing, labels=list_ob, autopct='%1.2f%%')
        if ('titulo' in diccionario) == True:
            plt.title(diccionario.get("titulo"))

    if diccionario.get("grafica") == 'lineas':
        fig, ax = plt.subplots()
        ax.plot(list_ob, list_ing)
        if ('titulox' in diccionario) == True:
            plt.xlabel(diccionario.get("titulox"))
        if ('tituloy' in diccionario) == True:
            plt.ylabel(diccionario.get("tituloy"))
        if ('titulo' in diccionario) == True:
            ax.set_title(diccionario.get("titulo"))

    plt.savefig(diccionario.get("nombre") + ".png")
    plt.show()


def html():
    ####### Comienza html
    with open('reporte.html', 'w') as f:
        i = 0
        f.write("<!DOCTYPE html>\n"
                "<html>\n"
                "<head>\n"
                "<title>Reporte de mes</title>\n"
                '<link rel="stylesheet" href="estilos.css">\n'
                "</head>\n"
                "<body>\n"
                '<div id="main-container">\n'
                "<h1>Reporte de ventas de mes Febrero</h1>\n"
                "<p>Creado por: Gerhard Benjamin Ardon Valdez 202004796</p>\n"
                "<table>\n"
                "<thead>\n"
                "<tr>\n"
                "<th>Producto</th><th>Precio</th><th>Cantidad</th><th>Ingresos</th>\n"
                "</tr>\n"
                "</thead>\n")

        ####### IMPRIMIR LOS OBJETOS

        while i < len(list_ob):
            f.write("<tr><td>"+str(producto.get_name(productos[i]))+"</td><td>"+str(producto.get_price(productos[i]))+"</td><td>"+str(producto.get_units(productos[i]))+"</td><td>"+str(round(producto.get_income(productos[i]), 2))+"</td>\n</tr>")
            i = i + 1

        productos.sort(key=lambda x: x.units, reverse=True)
        f.write("</table>\n"
                "<p>"
                    "<b>Producto mas vendido: </b>"+producto.get_name(productos[0])+" "
                "</p>"
                "<p>"
                    "<b>Producto menos vendido: </b>"+producto.get_name(productos[-1])+" "
                "</p>"                                                                    
                    "</div>\n"
                    "</body>\n"
                    "</html>")


def init():
    print("=========MENU=========")
    print("1.    Cargar data\n2.    Cargar instrucciones\n3.    Analizar\n4.    Reportes\n5.    Salir")
    print("======================")
    x = input()
    if x == "1":
        global data
        data = cargar()
        print(data)
        init()
    elif x == "2":
        global instrucciones
        instrucciones = cargar()
        print(instrucciones)
        init()
    elif x == "3":
        analizarVentas()
        # lista de ingresos mensuales
        k = 0
        while k < len(list_ob):
            list_ing.append(float(list_pr[k]) * float(list_ca[k]))
            k = k + 1
        # Cargar a los objetos
        i = 0
        while i < len(list_ob):
            productos.append(producto(str(list_ob[i]), float(list_pr[i]), int(list_ca[i]), float(list_ing[i])))
            i = i + 1

        analizarInstrucciones()
        print(diccionario)
        ####### ORDENAR LA LISTA DE OBJ
        productos.sort(key=lambda x: x.income, reverse=True)
        graficar()
        init()
    elif x == "4":

        html()
        webbrowser.open_new_tab('reporte.html')
        init()
    else:
        exit()


init()
