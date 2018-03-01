#!/usr/bin/python3
# -*- coding:utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import time, datetime, os, zipfile, mnist_functions
from configparser import ConfigParser, ExtendedInterpolation
from bottle import route, run, template, get, post, error, static_file, request, install, response, redirect

def get_timestamp():
	timestamp=int((datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds())
	return timestamp

def upload(file_origin):
	save_path=["./assets/simulations/simulation_"+str(timestamp)+"/","config_"+str(timestamp)+".ini"]
	full_path=save_path[0]+save_path[1]
	if not os.path.exists(save_path[0]):
		os.makedirs(save_path[0])
	file_origin.save(full_path) #enregistrement du fichier passé en argument sur le serveur
	return full_path

def global_vars_init(filepath):
	#Lecture des variables définies dans le fichier .ini
	io=ConfigParser(interpolation=ExtendedInterpolation())
	io.read(filepath) #lecture du fichier de config.
	vars_dict={}
	print("\nVariables chargées depuis le fichier de config. personnalisée ("+filepath.split("/")[-1]+") :")
	for i in io.sections():
		for j,k in io.items(i):
			if not(i=="default"):
				raw_value=eval(k) #convertion des calculs en résultats (ex: a=1+2 --> a=3)
				if(isinstance(raw_value,float)):
					if((raw_value).is_integer()):
						raw_value=int(raw_value) #convertion float-->int si possible
				vars_dict[j]=raw_value
				print(j+"="+str(raw_value))
	#Initialisation des variables non définies
	default_config="./assets/config/default.ini"
	print("\n"+20*"-"+"\nVariables chargées depuis le fichier de configuration par défaut :")
	if not(filepath==default_config):
		io.read(default_config)
		for i in io.sections():
			for j,k in io.items(i):
				if not j in vars_dict and i!="default":
					raw_value=eval(k)
					if(isinstance(raw_value,float)):
						if((raw_value).is_integer()):
							raw_value=int(raw_value)
					vars_dict[j]=raw_value
					print(j+"="+str(raw_value))
	print("\n"+20*"-")
	return vars_dict

@route('/')
def index():
	return template("bootstrap/index")

@post('/load')
def load():
	#Définition du timestamp
	global timestamp, number_of_img, eta
	timestamp=get_timestamp()
	print("\nInitialisation de la simulation n°"+str(timestamp)+"\n")
	#Remarque : Le timestamp permet d'identifier la simulation

	#Étude paramétrique
	if "file_ep" in request.POST:
		return template("bootstrap/dev")

	#Étude fixe, configuration par fichier .ini
	elif "file" in request.POST:
		print("\nConfiguration via fichier de configuration .ini personnalisé ("+request.files.get("file").filename+")\n")
		config=upload(request.files.get("file"))
		html_vars=global_vars_init(config) #initialisation des variables
		globals().update(html_vars)

	#Étude fixe, configuration par interface web
	else:
		print("\nConfiguration via interface web !\n")
		html_vars=global_vars_init("./assets/config/default.ini") #initialisation des variables
		#Modification des variables définies via l'interface web
		if("learning_type" in request.POST) and (request.POST["learning_type"]!=""):
			learning_type=request.POST["learning_type"]
			html_vars["learning_type"]=learning_type
		if("number_of_img" in request.POST) and (request.POST["number_of_img"]!=""):
			number_of_img=int(request.POST["number_of_img"])
			html_vars["number_of_img"]=number_of_img
		if("number_of_layers" in request.POST) and (request.POST["number_of_layers"]!=""):
			number_of_layers=int(request.POST["number_of_layers"])
			html_vars["number_of_layers"]=number_of_layers
		globals().update(html_vars)

	html_vars["timestamp"]=timestamp

	#Pensez à recalculer l'estimation à chaque fois que vous changez de machine (cf : rapport de projet)
	eta=(125*number_of_img//5000)+7+1 #temps d'apprentissage pour 1000 images + temps de création des résultats (pyplot) + marge

	html_vars["eta"]=eta

	html_vars["html_vars"]=html_vars

	return template("bootstrap/load",html_vars)

@post('/run')
def run_simulation():

	html_vars={}
	for i,j in request.POST.items():
		tmp=str(j)
		try:
			tmp=float(tmp)
		except:
			pass
		if(isinstance(tmp,float)):
			if((tmp).is_integer()):
				tmp=int(tmp)
		exec("html_vars[\'"+i+"\']=tmp")

	globals().update(html_vars)

	begining_time=time.clock() #Début du chrono.

	#Création du dossier de la simulation en cours
	result_path="./assets/simulations/simulation_"+str(timestamp)+"/"
	if not os.path.exists(result_path):
		os.makedirs(result_path)

	g12,g23=mnist_functions.learning(html_vars) #Exécution du programme principal

	#Images
	img_src=[]
	img_src.append(str(mnist_functions.affichage(g12,n11,n12,n21,n22,1,"Memristors conductances between layer1 and layer2",timestamp))) #Enregistrement de l'image 1
	img_src.append(str(mnist_functions.affichage(g23,n21,n22,n31,n32,2,"Memristors conductances between layer2 and layer3",timestamp))) #Enregistrement de l'image 2
	html_vars["img_src"]=img_src

	#Fichier texte
	txt_filename=result_path+"test_results_"+str(timestamp)+".txt"
	with open(txt_filename,"w") as txt:
		txt.write("Insérez les résultats de la simulation n°"+str(timestamp)+" ici !")
	html_vars["text_result"]=txt_filename

	#Archive ZIP
	zip_path=result_path+"simulation_"+str(timestamp)+".zip"
	zip=zipfile.ZipFile(zip_path, "w")
	zip.write(txt_filename,arcname=txt_filename.split("/")[-1])
	default_cfg="./assets/config/default.ini"
	user_cfg=result_path+"config_"+str(timestamp)+".ini"
	if os.path.exists(user_cfg):
		zip.write(user_cfg,arcname=user_cfg.split("/")[-1])
	else:
		zip.write(default_cfg,arcname=default_cfg.split("/")[-1])
	for file in os.listdir(result_path):
		if file.endswith(".png"):
			zip.write(result_path+file,arcname=file)
	zip.close()
	html_vars["zip"]=zip_path

	#Temps écoulé
	t_elapsed=time.clock()-begining_time
	print("\nSimulation terminée !!\n\nTemps d'execution : ", t_elapsed)
	html_vars["t_elapsed"]=int(t_elapsed)

	#Taux d'apprentissage
	html_vars["learning_rate"]=learning_rate

	return template("bootstrap/result",html_vars)

@route('/cancel')
def cancel():
	return redirect('/')

@route('/<file:path>')
def returnFile(file):
	#Ajustez la valeur de 'root' en fonction du serveur
	return static_file(file,root='/var/www/nns')

@error(404)
def error404(code):
	return template("bootstrap/error")

#Lancement du serveur
run(server="gunicorn", host='0.0.0.0', port=8080, workers="4", worker_connections="1024", timeout="3600", reloader=True, debug=True)

