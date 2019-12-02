#On commence par importer les librairies necessaires au fonctionnement
import sys, os, os.path
import smtplib
import subprocess 
from os import chdir, mkdir


def menu():
	os.system('clear')
	print("--------------------------------------------------------------------")
	print("Bienvenue à travers mon script de sauvegarde \n Voici les differentes options:")
	print(" 1.Créer une sauvegarde du site Wordpress \n 2.Restaurer le site Wordpress à partir d'un fichier \n 3.Manuel d'instruction \n 4.Quitter")
	print("-------------------------------------------------------------------")

	print(" \n Votre choix:")
	choice = input(" >>")
	if choice=="1":
		sauvegarde()
	elif choice=="2":
		restauration()
	elif choice=="3":
		readme()
	elif choice=="4":
		return
	else:
		menu()

	return


def sauvegarde():
	heure= os.popen("date +'%d-%m-%Y'")
	heure2=heure.read()
	if os.path.isfile('variable5.py'):
		print("Le fichier variable.py est présent :) Début de la procédure...")
#Si le fichier est présent on importe les variable
		from variable import expediteur,mdp,localisation,ip,port,protocol

#Sinon on indique un message d'erreur avec la possibilité de basculer sur la version non automatiser
	else:
		print(" \n Entrer le repertoire ou la sauvegarde aura lieu:")
		localisation= input("[exemple: /home/user/sauvegarde] >>")
		print(" \n Entrer l'adresse Ip du serveur")
		ip = input(" >>")	
		print("Recapitlatif des informations: \n Repertoire de sauvegarde: ",localisation,"\n Ip du serveur:",ip,"\n Date:",heure2)
		print(" \n Etes vous sur?(y/n)")
		choice = input(" >>")

		if choice=="y":
			print("Début de la sauvegarde")
			#if not os.path.exists(localisation):
 			#	os.makedirs(localisation)
			nom = heure2+".mysql"
			os.system('sudo mysqldump  -u root   wordpress > sauv.sql')
			os.rename("sauv.sql",heure2+".sql")
			print(heure2,".sql",nom)
		else:
			sauvegarde()
		return
	return

def restauration() :
#on stock dans une variable le mdp et le compte mail utilisé
	localisation = "/home/administrateur/easy-rsa"
	nom="goku"
	expediteur = "loic.esparon.ocr@gmail.com"
	mdp = subprocess.check_output(['cat', '/home/administrateur/mdp.txt'])
#On demande le mail de l'utilisateur à qui est destiner les fichiers
	print("Quel est le mail utilisateur?")
#On l'integre ensuite à une variable
	mail= input(" >>")
#Demande de confirmation
	print("Etes vous sur qu'il s'agit de cette adresse:",mail," ? (y/n)")



def readme():
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
