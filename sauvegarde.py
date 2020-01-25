#On commence par importer les librairies necessaires au fonctionnement
import sys, os, os.path
import smtplib
import subprocess 
from os import chdir, mkdir
import datetime
import sys

#Début de la fonction menu
def menu():
	os.system('clear')
	print("--------------------------------------------------------------------")
	print("Bienvenue à travers mon script de sauvegarde \n Voici les differentes options:")
	print(" 1.Créer une sauvegarde du site Wordpress \n 2.Restaurer le site Wordpress à partir d'un fichier \n 3.Installation de Wordpress \n 4.Manuel d'instruction \n 5.Quitter")
	print("-------------------------------------------------------------------")

	print(" \n Votre choix:")
#Si un argument est entrée on le selectionne en tant que choix (par exemple pour automatiser l'exécution
	if len( sys.argv ) > 0:
		choice = sys.argv[1]
	else:
#Sinon le choix est laissé à l'utilisateur
		choice = input(" >>")
	if choice=="1":
		sauvegarde()
	elif choice=="2":
		restauration()
	elif choice=="3":
		installation()
	elif choice=="4":
		readme()
	elif choice=="5":
		return
	else:
		menu()

	return

###################################################################################

#Debut de la fonction de sauvegarde
def sauvegarde():
	#On definit le jour dans une variable qui sera utilise plus tard dans la fonction
	heure= datetime.datetime.now()	
	heure2= heure.date()

#heure2=heure.read()
	print(" \n Entrer le repertoire ou la sauvegarde aura lieu:")
	localisation="/home/administrateur/Bureau/sauvegarde"
	#localisation= input("[exemple: /home/user/sauvegarde] >>")
	print(" \n Entrer l'adresse Ip du serveur vers laquelle copier la sauvegarde: ")
	ip = input(" >>")
	print("\n--------------------------------------------------------------------")
	print("Recapitulatif des informations: \n Repertoire de sauvegarde: ",localisation,"\n Ip du serveur distant:",ip,"\n Date:",heure2)
	print("--------------------------------------------------------------------")
	#os.system('ssh administrateur@'+ip+' find /home/administrateur/test -type d -mtime +1 -exec echo {} \;')
	print(" \n Etes vous sur?(y/n)")
	choice = input(" >>")

	if choice=="y":
		print("Début de la sauvegarde...")
		if not os.path.exists(localisation):
 			os.makedirs(localisation)
		os.chdir(localisation)
		if not os.path.exists(str(heure2)):
 			os.makedirs(str(heure2))
		os.chdir(str(heure2))
		os.system('sudo mysqldump  -u root   wordpress > sauv.sql')
		os.system('sudo cp -r /var/www/html '+localisation+'/'+str(heure2))


		print("Fichiers sauvegardé à l'emplacement suivant:",localisation)
		print("\n Copie vers le serveur distant en cours..")
		os.chdir(localisation)
		os.system('scp -r '+str(heure2)+'/ administrateur@'+ip+':/home/administrateur')
		print("\n Copie réalisé")
		print("\n Analyse de la presence de sauvegarde superieur à 30jours..")
		os.system('ssh administrateur@'+ip+' find /home administrateur/test -type d -mtime +10 -exec rm -fr {} \;')
#ssh login@Host 'find /home/exploit/ -size 0 -exec rm -i  {} \;'
#find -type d -mtime +10

		print("\n Retour vers le menu principal")
		input(" >>")
		menu()
	else:
		sauvegarde()
	return


####################################################################################

def restauration() :
	heure= datetime.datetime.now()	
	heure2= heure.date()
	print(" \n Entrer le repertoire ou la sauvegarde a eu lieu:")
	localisation="/home/administrateur/Bureau/sauvegarde"	
	print(" \n A quel date voulez-vous restaurez le site?")
	jour= input("[exemple: 2019-12-16 pour 16 decembre 2019 ] >>")	
	#localisation= input("[exemple: /home/user/sauvegarde] >>")
	print("\n Verification de la présence des fichiers en cours..\n")
	if os.path.isfile(localisation+'/'+jour+'/sauv.sql') and os.path.isdir(localisation+'/'+jour+'/wp-content'):
		print("Fichiers présents :) \n")
		print("Debut de la restauration..\n")
		os.chdir(localisation+'/'+jour)
		os.system('sudo mysql -u root   wordpress < sauv.sql')
		os.system('sudo cp -r www.example.com/* /var/www/html/')
		os.system('sudo service apache2 restart ')
		print("Restauration terminée :) \n Retour au menu principal")
		input(" >>")
		menu()


	else:
		print("\033[31m \n /_\ Erreur le repertoire de sauvegarde n'est pas présent!\n\033[0m")
		print("Voulez-vous le recuperer à partir d'un serveur distant?(y/n)")
		choice = input(" >>")
		if choice=="y":
			print(" \n Entrer l'adresse Ip du serveur vers laquelle recuperer la sauvegarde: ")
			ip = input(" >>")
			print(" \n Entrer le repertoire ou se trouve la sauvegarde sur le serveur distant: ")
			repertoire = input(" >>")
			print(" \n A quel date souhaitez-vous restaurer le site? ")
			date2 = input("[exemple: 2019-12-16 pour 16 decembre 2019 ] >>")	

			print("\n--------------------------------------------------------------------")
			print("Recapitulatif des informations: \n Repertoire de sauvegarde: ",repertoire,"\n Ip du serveur distant:",ip,"\n Date de restauration:",date2)
			print("--------------------------------------------------------------------")
			print(" \n Etes vous sur?(y/n)")
			choice = input(" >>")
			if choice=="y":
				print(" \n Recuperation du fichier en cours..")
				os.system('scp -r administrateur@'+ip+' '+repertoire+'/'+date2+' ' +localisation)
				print("\n Recuperation terminée. Debut de la restauration..")

				os.chdir(localisation+'/'+date2)
				os.system('sudo mysql -u root   wordpress < sauv.sql')
	
				os.system('sudo cp -r www.example.com/* /var/www/html/ ')
				os.system('sudo service apache2 restart ')
				print("\n Restauration terminée :) \n Retour au menu principal")
				input(" >>")
				menu()
#sudo scp -r administrateur@192.168.1.1:/home/administrateur/2019-12-07 /home/administrateur/Bureau/sauvegarde/
			else  :	
				os.system('clear')
				restauration()
			

		else:
			print("Retour au menu principal")
			input(" >>")
			menu()


	return

	#os.chdir(localisation)
	
########################################################################################


def installation():
	print("\n Début du téléchargement...")
	os.system('sudo apt-get install mysql-server mysql-client ;echo valeur=$?>> erreur.py')
	from erreur import valeur
	if valeur != 0 :
		print("\n\n\n /!\ Impossible de telecharger mysql (voir ligne ci dessus) \nMerci de verifier votre connexion internet.")

		os.system('rm erreur.py ')	
		print(" \n Voulez-vous continuer?(y/n)")
		choice = input(" >>")
		if choice=="y":
			print("\n Reprise du processus...")
		else:
			menu()
	else:

		print("Telechargement de Mysql réussi\n")
		os.system('rm erreur.py ')

	os.system('sudo apt-get install apache2 php7.2 php7.2-mysql libapache2-mod-php7.2 ;echo valeur=$?>> erreur.py')
	from erreur import valeur
	if valeur != 0 :
		print("\n\n\n /!\ Impossible de telecharger apache (voir ligne ci dessus) \nMerci de verifier votre connexion internet.")
		os.system('rm erreur.py ')	
		print(" \n Voulez-vous continuer?(y/n)")
		choice = input(" >>")
		if choice=="y":
			print("\n Reprise du processus...")
		else:
			menu()
	else:
		print("Telechargement de Apache réussi\n")
		os.system('rm erreur.py ')
		os.system('sudo service apache2 restart ')
		print("Telechargement de tout les logiciels réussi\n")
		print("Retour au menu principal")
		input(" >>")
		menu()
	return



###################################################################################

def readme():
	mydb = mysql.connector.connect(
  	host="localhost",
  	user="root",
  	passwd=""
)

	mycursor = mydb.cursor()

	mycursor.execute("CREATE DATABASE hola")
	print("""  -------------------------------------------------------------------------
|									  |
|			MANUEL D'INSTRUCTION				  |
|									  |
 --------------------------------------------------------------------------

1. PRE-REQUIS

/!\ Ce Script est à exécuter en tant que root sur un serveur OPENVPN sous GNU LINUX!

Pour le bien de son exécution, les fichiers nécessaires à la création des clés client (ca.key ,ca.crt et build.key) doivent être présents dans un dossier sous la forme suivante:
Le dossier (qui contient build.key) et un sous dossier qui se nomme keys (contenant ca.key et ca.crt du serveur VPN)

Cette configuration est celle par défaut lors de l'installation de OPENVPN sur un serveur. Il ne devrait donc avoir aucune modification à réaliser.

Pour plus de sécurité, nous mettrons le mot de passe de la boite mail utilisé pour les envois dans un fichier texte (cf partie 4)

Le chemin sera à indiquer au sein du script sous la variable :"mdp" (cf envoimail())

Pour faciliter la configuration, le fichier vars devra être configuré au préalable avec les informations de l'entreprise

Une connexion internet peut être requise pour l'envoi par mail.

--------------------------------------------------------------------------------

2. SON FONCTIONNEMENT

Le script a pour fonction de créer automatiquement les fichiers de configurations nécessaires à la connexion des utilisateurs. 
Pour ce faire, des informations seront demandées à l'utilisateur du script telles que : le nom du client, l'adresse IP du serveur, le port utilisé, et le protocole.

Une fois le fichier créer, il est possible de les envoyer par mail à un utilisateur avec en corps du mail une procédure détailler de l'utilisation et des actions à réaliser avec les fichiers envoyés.
. Le mail est adapté en fonction de s’il s'agit d'un client Linux ou Windows.

Ce manuel d'instruction est également disponible au sein du script avec le choix "2" dans le menu.

/!\ Attention à bien respecter les réponses attendues aux afin de ne pas avoir à répondre aux mêmes questions plusieurs fois d'affilée.

---------------------------------------------------------------------------------

3. OPTIMISATION

Dans le cadre d'une utilisation fréquente au sein d'un même environnement, le script prévoit des variables préenregistrées.

Ils sont disponibles sous forme de commentaires et se distinguent de manière suivante : «/*Le commentaire »

Ces variables permettent de configurer les champs les plus utilisés afin de ne pas avoir a les entrées à chaque exécution.
Exemple : l'IP du serveur, le port, le protocole...

Bien entendu si on utilise ces variables il faudra veiller à commenter les lignes demandant l'interaction avec l'utilisateur afin de ne pas avoir de conflit.

--------------------------------------------------------------------------------

4. MAIL

L'adresse mail expéditeur est à définir dans la fonction envoimail() au sein de la variable "expéditeur"

Comme mentionner précédemment, le mot de passe de ce dernier sera mis au sein d'un fichier texte ou la localisation sera stocker dans la variable "mdp"

Un corps de mail avec une procédure générique a été mis en place. Ce dernier sera à adapter en fonction du contexte.

Les fichiers seront envoyés en pièce jointe sous la forme d'une archive .zip

""")

	return



menu()
