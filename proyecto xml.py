"""
1. Partidos ganados por equipo

2. Nombres de los equipos sin repetir ninguno.

3. Partidos en los que se han sacado más de X tarjetas amarillas. (Pide un valor para X y muestra los partidos en los que se han sacado más de X tarjetas amarillas)

4. Salir

Para realizar lo anterior debéis implementar y utilizar las siguientes funciones:

menu() -> Muestra el menú y devuelve la opción seleccionada por el usuario.

leerPartidos() -> Función que lee el XML y devuelve una lista con los partidos siendo cada partido un diccionario con los siguientes datos:

partido { local: "Celtic", visitante: "Hearts", "Amarillas": "4", "GolesLocal": "4", “GolesVisitante”: “1”}

numeroPartidos(numeroAmarillas) -> Recibe un número de tarjetas amarillas y devuelve el número de partidos en los que se han sacado más de ese número de amarillas.

partidosGanados(equipo) : Recibe un equipo y devuelve el número de partidos que ha ganado.

"""
from lxml import etree
doc = etree.parse('LeagueAndSeason.xml')
from pprint import pprint
import os
partidos=doc.findall('Match')
salir="no"

def menu():
	print("\n=========== Menú liga Escocesa ===========\n")
	print("1. Partidos ganados por equipo.")
	print("2. Nombres de los equipos sin repetir ninguno.")
	print("3. Partidos en los que se han sacado más de X amarillas.")
	print("4. Salir.")
	opcion = input("\nSelecciona una opción  del menú: ") 
	return opcion 

def amarillas(partido):
	amarillasL=partido.findtext("HomeTeamYellowCardDetails")
	amarillasV=partido.findtext("AwayTeamYellowCardDetails")
	if type(amarillasL) == str:
		amarillasL=amarillasL.count(":")
	else:
		amarillasL=0
	if type(amarillasV) == str:
		amarillasV=amarillasV.count(":")
	else:
		amarillasV=0
	totalamarillas=amarillasL+amarillasV
	return totalamarillas

def leerPartidos():
	listapartidos=[]
	for partido in partidos:
		local=partido.findtext("HomeTeam")
		visitante=partido.findtext("AwayTeam")
		golesLoc=partido.findtext("HomeGoals")
		golesVis=partido.findtext("AwayGoals")
		numeroamarillas=amarillas(partido)
		partidosdic=dict(zip(["local","visitante","Amarillas","GolesLocal","GolesVisitante"], [local,visitante,numeroamarillas,golesLoc,golesVis]))
		listapartidos.append(partidosdic)
	return listapartidos

def numeroPartidos(numeroAmarillas):
	contador=0
	listapar=leerPartidos()
	for partido in listapar:
		amarillaporpartido=int(partido["Amarillas"])
		if amarillaporpartido>numeroAmarillas:
			contador=contador+1
	return contador

def partidosGanados(equipo):
	contador=0
	error=0
	listapar=leerPartidos()
	for partido in listapar:
		if partido["local"] == equipo:
			goleslocal=int(partido["GolesLocal"])
			golesvisitante=int(partido["GolesVisitante"])
			if goleslocal>golesvisitante:
				contador=contador+1
				error+=1
		elif partido["visitante"] == equipo:
			goleslocal=int(partido["GolesLocal"])
			golesvisitante=int(partido["GolesVisitante"])
			if golesvisitante>goleslocal:
				contador=contador+1
				error+=1
	if error<2:
		input("\nNombre incorrecto! \nPulse Intro para continuar: ")
		menu()
	return contador	

while salir == "no":
	opcion=menu()
	if opcion=="1":
		os.system("cls")
		equipo=(input("Dime el nombre de un equipo: "))
		numpartido=partidosGanados(equipo)
		print('\nEl número de partidos que ha ganado este equipo es de: ', numpartido)
	elif opcion=="2":
		listapar=leerPartidos()
		equipos=[]
		for elemento in listapar:
			if elemento["local"] not in equipos:
				equipos.append(elemento["local"])
		print ("\nEstos son los equipos de la liga Escocesa: \n")
		for nombre in equipos:
			print(nombre)
	elif opcion=="3":
		os.system("cls")
		amarilla=int(input("Introduce un número de tarjetas amarillas: "))
		NumPartidos=numeroPartidos(amarilla)
		print('\nEl número de partidos que superan ese número de amarillas son: ', NumPartidos)

	elif opcion=="4":
		print("Hasta pronto!")
		salir="si"
	else:
		print("Dato incorrecto.")
