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

/!\ Ce Script est à exécuter dans le même répertoire que le fichier variable.py dans le cas d'une exécution automatique!

Le fichier variable.py est fourni au meme endroit que le script de sauvegarde. Il permet de configurer les variables les plus utilisées et les identifiants gmail

Ce manuel d'instruction est également disponible au sein du script avec le choix "4" dans le menu.

Une connexion internet est requise pour l'envoi par mail et le téléchargement des pré-requis

--------------------------------------------------------------------------------

2. SON FONCTIONNEMENT(sauvegarde)

Le script a pour fonction de sauvegarder et restaurer l'état d'un site wordpress. Pour ce faire, il va réaliser une copie du répertoire html, de la base de données et du crontab si il y en a un (le crontab est utilisé pour automatiser l'exécution du script).

Ces fichiers vont être copiés dans un repertoire se nommant avec la date du jour de sauvegarde. L'emplacement de la sauvegarde est à definir via le script ou dans variable.py

Une fois créee, une copie sera réalisée sur un serveur distant. A nouveau le choix du serveur est à definir


---------------------------------------------------------------------------------

3. SON FONCTIONNEMENT(sauvegarde_auto)

Une seconde fonction existe dans le cas d'une exécution automatique (choix "3").

Comme dit précédemment ce dernier doit être exécuté en précense du fichier variable.py!!

Il va notamment importer les variables qui s'y trouvent. Il est donc important de bien verifier les informations et de réaliser un test de fonctionnement avant de l'automatiser via crontab ou autres..

Dans le cas ou le fichier n'est pas présent, un mail est envoyé à l'utilisateur/administrateur pour l'avertir que la sauvegarde a potentiellement pas eu lieu.

Le processus de sauvegarde est le même que pour la version manuelle

--------------------------------------------------------------------------------

4. SON FONCTIONNEMENT(restauration)

Concernant la restauration, le script va demander l'emplacement du repertoire contenant les fichiers necessaires à la restauration mais également la date de sauvegarde souhaitée. Dans un second temps il va verifier la présence des fichiers puis copier/restaurer les fichiers.

Si le dossier n'est pas présent en local, une option permet de le telecharger depuis un serveur distant

Pour plus dinformations, voici le fonctionnement de la restauration: -Copie du repertoire html vers /var/www/html (cela permet de ne pas reconfigurer apache par defaut) -Création de la base de données et de l'utilisateur Wordpress (le mot de passe -Restauration de la base Wordpress (via le fichier .mysql) -Restauration du crontab -Redemarrage de apache -Enjoy :)

5. MAIL

Cette fonction n'est utilisée que lors de la sauvegarde automatique!

L'adresse mail expéditrice/destinataire est à importer via le fichier variable.py

Idem pour le mot de passe.

""")

	return



menu()
