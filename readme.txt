 -------------------------------------------------------------------------
|									  |
|			MANUEL D'INSTRUCTION				  |
|									  |
 --------------------------------------------------------------------------

1. PRE-REQUIS

/!\ Ce Script est à exécuter dans le même répertoire que le fichier variable.py dans le cas d'une exécution automatique!

Le fichier variable.py est fourni au meme endroit que le script de sauvegarde. Il permet de configurer les variables les plus utilisées et les identifiants gmail

Ce manuel d'instruction est également disponible au sein du script avec le choix "4" dans le menu.

Une connexion internet est requise pour l'envoi par mail et le téléchargement des pré-requis


--------------------------------------------------------------------------------------------------------------------------------------------------------------

2. SON FONCTIONNEMENT(sauvegarde)

Le script a pour fonction de sauvegarder et restaurer l'état d'un site wordpress.
Pour ce faire, il va réaliser une copie du répertoire html, de la base de données et du crontab si il y en a un (le crontab est utilisé pour automatiser l'exécution du script).

Ces fichiers vont être copiés dans un repertoire se nommant avec la date du jour de sauvegarde. L'emplacement de la sauvegarde est à definir via le script ou dans variable.py

Une fois créee, une copie sera réalisée sur un serveur distant. A nouveau le choix du serveur est à definir

--------------------------------------------------------------------------------------------------------------------------------------------------------------

3. SON FONCTIONNEMENT(sauvegarde_auto)

Une seconde fonction existe dans le cas d'une exécution automatique  (choix "3"). 

Comme dit précédemment ce dernier doit être exécuté en précense du fichier variable.py!!

Il va notamment importer les variables qui s'y trouvent. Il est donc important de bien verifier les informations et de réaliser un test de fonctionnement avant de l'automatiser via crontab ou autres..

Dans le cas ou le fichier n'est pas présent, un mail est envoyé à l'utilisateur/administrateur pour l'avertir que la sauvegarde a potentiellement pas eu lieu.

Le processus de sauvegarde est le même que pour la version manuelle

----------------------------------------------------------------------------------------------------------------------------------------------------------------

4. SON FONCTIONNEMENT(restauration)

Concernant la restauration, le script va demander l'emplacement du repertoire contenant les fichiers necessaires à la restauration mais également la date de sauvegarde souhaitée.
Dans un second temps il va verifier la présence des fichiers puis copier/restaurer les fichiers.

Si le dossier n'est pas présent en local, une option permet de le telecharger depuis un serveur distant


Pour plus dinformations, voici le fonctionnement de la restauration:
	-Copie du repertoire html vers /var/www/html (cela permet de ne pas reconfigurer apache par defaut)
	-Création de la base de données et de l'utilisateur Wordpress (le mot de passe
	-Restauration de la base Wordpress (via le fichier .mysql)
	-Restauration du crontab
	-Redemarrage de apache
	-Enjoy :)

----------------------------------------------------------------------------------------------------------------------------------------------------------------

5. MAIL

Cette fonction n'est utilisée que lors de la sauvegarde automatique!

L'adresse mail expéditrice est à importer via le fichier variable.py

Idem pour le mot de passe.

