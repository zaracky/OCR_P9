#On commence par importer les librairies necessaires au fonctionnement
import sys, os, os.path
import smtplib
import subprocess 
from os import chdir, mkdir
import datetime

#Ces librairies permettent l'envoie par mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


#Début de la fonction menu
def menu():
	os.system('clear')
	print("--------------------------------------------------------------------")
	print("Bienvenue à travers mon script de sauvegarde \n Voici les differentes options:")
	print(" 1.Créer une sauvegarde du site Wordpress \n 2.Restaurer le site Wordpress à partir d'un fichier \n 3.Sauvegarde automatique \n 4.Manuel d'instruction \n 5.Quitter")
	print("-------------------------------------------------------------------")

	print(" \n Votre choix:")
#Si un argument est entrée on le selectionne en tant que choix (par exemple pour automatiser l'exécution)
	if len( sys.argv ) > 1:
		choice = sys.argv[1]
	else:
#Sinon le choix est laissé à l'utilisateur
		choice = input(" >>")
	if choice=="1":
		sauvegarde()
	elif choice=="2":
		restauration()
	elif choice=="3":
		sauvegarde_auto()
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
#On demande à l'utilisateur d'entrer les differents paramètres
	print(" \n Entrer le repertoire ou la sauvegarde aura lieu:")
	localisation= input("[exemple: /home/user/sauvegarde] >>")
	print(" \n Entrer l'adresse Ip du serveur vers laquelle copier la sauvegarde: ")
	ip = input(" >>")

#On lui demande confirmation avant d'executer le script
	print("\n--------------------------------------------------------------------")
	print("Recapitulatif des informations: \n Repertoire de sauvegarde: ",localisation,"\n Ip du serveur distant:",ip,"\n Date:",heure2)
	print("--------------------------------------------------------------------")
	print(" \n Etes vous sur?(y/n)")
	choice = input(" >>")
#Si oui on débute la sauvegarde
	if choice=="y":
		print("Début de la sauvegarde...")
#On crée le repertoire destinataire si ce dernier n'est pas present
		if not os.path.exists(localisation):
 			os.makedirs(localisation)
		os.chdir(localisation)
		if not os.path.exists(str(heure2)):
#On crée un repertoire avec la date de la sauvegarde
 			os.makedirs(str(heure2))
		os.chdir(str(heure2))
#On sauvegarde la base de données et le fichier wordpress et le crontab
		os.system('sudo mysqldump  -u root   wordpress > sauv.sql')
		os.system('sudo cp -r /var/www/html '+localisation+'/'+str(heure2))
		os.system('crontab -u administrateur -l > crontab')

#On indique l'emplacement de la sauvegarde
		print("Fichiers sauvegardé à l'emplacement suivant:",localisation)
#On réalise ensuite une copie vers un serveur distant
		print("\n Copie vers le serveur distant en cours..")
		os.chdir(localisation)
		print(" \n Ou souhaiter vous copier la sauvegarde sur le serveur distant? ")
		access = input(" >>")
		os.system('scp -r '+str(heure2)+'/ administrateur@'+ip+':'+access)
		print("\n Copie réalisée")
#Verification des fichiers supérieur à 7jours
		print("\n Analyse de la presence de sauvegarde superieur à 7jours..")
		os.system('ssh administrateur@'+ip+' find '+access+' -type d -mtime +7 -exec rm -fr {} \;')

		print("\n Retour vers le menu principal")
		input(" >>")
		menu()
#Sinon retour à la fonction
	else:
		sauvegarde()
	return


####################################################################################



#Debut de la fonction de sauvegarde créer pour l'automatisation
def sauvegarde_auto():

	global expediteur,mdp,mail

#On verifie la précense du fichier variable.py
	print("Verification de la présence du fichier variable.py en cours.. \n")
	if os.path.isfile('variable.py'):
		print("Le fichier variable.py est présent :) Début de la procédure...")
#Si le fichier est présent on importe les variable
		from variable import expediteur,mdp,localisation,ip,access
#Sinon on fait appel a la fonction mail pour avertir l'administrateur
	else:
		envoimail()
#On definit le jour dans une variable qui sera utilise plus tard dans la fonction
	heure= datetime.datetime.now()	
	heure2= heure.date()
#A la difference de la premier fonction aucune question ne vas etre posé
	localisation="/home/administrateur/Bureau/sauvegarde"
	ip="192.168.1.1"

	#os.system('ssh administrateur@'+ip+' find /home/administrateur/test -type d -mtime +1 -exec echo {} \;')
	print("Début de la sauvegarde...")
	if not os.path.exists(localisation):
 		os.makedirs(localisation)
	os.chdir(localisation)
	if not os.path.exists(str(heure2)):
 		os.makedirs(str(heure2))
	os.chdir(str(heure2))
#Meme proceder de sauvegarde que la fonction manuel
	os.system('sudo mysqldump  -u root   wordpress > sauv.sql')
	os.system('sudo cp -r /var/www/html '+localisation+'/'+str(heure2))
	os.system('crontab -u administrateur -l > crontab')


	print("Fichiers sauvegardé à l'emplacement suivant:",localisation)
	print("\n Copie vers le serveur distant en cours..")
	os.chdir(localisation)
	os.system('scp -r '+str(heure2)+'/ administrateur@'+ip+':/home/administrateur')
	print("\n Copie réalisé")
	print("\n Analyse de la presence de sauvegarde superieur à 30jours..")
	os.system('ssh administrateur@'+ip+' find /home/administrateur/test -type d -mtime +20 -exec rm -fr {} \;')
	os.system('find /home/administrateur/Bureau/sauvegarde -type d -mtime +20 -exec rm -fr {} \;')
#ssh login@Host 'find /home/exploit/ -size 0 -exec rm -i  {} \;'
#find -type d -mtime +10

	print("\n Retour vers le menu principal")
	return



####################################################################################


#Debut de la fonction restauration
def restauration() :
	heure= datetime.datetime.now()	
	heure2= heure.date()
#On verifie/télécharge les pré-requis au fonctionnement du site
	print("\n Téléchargement des pré-requis...")
	os.system('sudo apt-get install mysql-server mysql-client')
	os.system('sudo apt-get install apache2 php7.2 php7.2-mysql libapache2-mod-php7.2')
	os.system('sudo service apache2 start ')
#On avertit l'utilisateur du résultat
	print("\n Telechargement de tout les pré-requis réussis\n")

#Pour procéder à la restauration de nombreuses informations sont utiles:
	print(" \n Entrer le repertoire ou la sauvegarde a eu lieu:")
	localisation= input("[exemple: /home/user/sauvegarde] >>")
	print(" \n A quel date voulez-vous restaurez le site?")
	jour= input("[exemple: 2019-12-16 pour 16 decembre 2019 ] >>")	

#On verifie la présence des fichiers necessaires à la restauration
	print("\n Verification de la présence des fichiers en cours..\n")
	if os.path.isfile(localisation+'/'+jour+'/sauv.sql') and os.path.isdir(localisation+'/'+jour+'/html') and os.path.isfile(localisation+'/'+jour+'/crontab'):
		print("Fichiers présents :) \n")
#Si ils sont présent on peut débuter la restauration
		print("Debut de la restauration...\n")
		os.chdir(localisation+'/'+jour)
		os.system('sudo mysql -u root   wordpress < sauv.sql')
		os.system('sudo crontab crontab ')
		os.system('sudo cp -r html/* /var/www/html/')
		os.system('sudo service apache2 restart ')
#manque création bdb
		print("Restauration terminée! \n Retour au menu principal")
		input(" >>")
		menu()

#Sinon on laisse la posibilité de le récuperer depuis un serveur distant
	else:
		print("\033[31m \n /_\ Erreur tout les fichiers ne sont pas présent!\n\033[0m")
		print("Voulez-vous le recuperer à partir d'un serveur distant?(y/n)")
		choice = input(" >>")
		if choice=="y":
#Si c'est le cas on demande les informations de connexion
			print(" \n Entrer l'adresse Ip du serveur vers laquelle recuperer la sauvegarde: ")
			ip = input(" >>")
			print(" \n Entrer le repertoire ou se trouve la sauvegarde sur le serveur distant: ")
			repertoire = input(" >>")
			print(" \n A quel date souhaitez-vous restaurer le site? ")
			date2 = input("[exemple: 2019-12-16 pour 16 decembre 2019 ] >>")	

	print("\n--------------------------------------------------------------------")
			print("Recapitulatif des informations: \n Repertoire de sauvegarde: ",repertoire,"\n Ip du serveur distant:",ip,"\n Date de restauration:",date2)
			print("--------------------------------------------------------------------")
#On demande confirmations des informations
			print(" \n Etes vous sur?(y/n)")
			choice = input(" >>")
			if choice=="y":
#Si oui début du telechargement et de la restauration
				print(" \n Recuperation du repertoire en cours..")
				os.system('scp -r administrateur@'+ip+' '+repertoire+'/'+date2+' ' +localisation)
				print("\n Recuperation terminée. Debut de la restauration..")
				print("\n Verification de la présence des fichiers en cours..\n")
#On verifie que tout les fichiers necessaires sont présent
				if os.path.isfile(localisation+'/'+jour+'/sauv.sql') and os.path.isdir(localisation+'/'+jour+'/html') and os.path.isfile(localisation+'/'+jour+'/crontab'):
#Si c'est le cas on commence la restauration
					print("Fichiers présents :) \n Debut de la restauration...\n")
					os.chdir(localisation+'/'+date2)
					os.system('sudo mysql -u root   wordpress < sauv.sql')
					os.system('sudo crontab crontab ')
					os.system('sudo cp -r html/* /var/www/html/')
					os.system('sudo service apache2 restart ')
					print("\n Restauration terminée! \n Retour au menu principal")
					input(" >>")
					menu()
#Sinon on avertit l'utilisateur
				else:
					print("\033[31m \n /_\ Erreur les fichiers necessaires à la restauration ne sont pas présent!\n Retour au menu principal \n \033[0m")
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
	
########################################################################################

def envoimail():

	print("\nPréparation du mail pour l'envoie..")
#On l'integre ensuite à une variable
	mail= input(" >>")

	msg = MIMEMultipart()
#On definit ici le corps du mail. Ce dernier sera a adapter en fonction du type de destinataire (technique ou non)
	msg['From'] = expediteur
	msg['To'] = mail
	msg['Subject'] = '/!\ Alerte sauvegarde impossible' 
	message = u"""\
		Bonjour,
		Une erreur est survenue concernant la sauvegarde du site web. Merci de lancer une sauvegarde manuelle afin d'analyser le message d'erreur
		
		Cordialement,
		Le système d'information"""
	msg.attach(MIMEText(message))
#§§§§§§§§§§§§§§§ Serveur mail à modifier si l'on ne souhaite pas utiliser gmail
	mailserver = smtplib.SMTP('smtp.gmail.com', 587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()
#On indique les identifiants de connexion
	mailserver.login(expediteur, mdp)
	mailserver.sendmail(expediteur, mail, msg.as_string())
	mailserver.quit()
	print("\nEnvoie du mail terminé! Retour au menu principal")
	return



#################################################################################



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
