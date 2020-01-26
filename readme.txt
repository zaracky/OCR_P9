 -------------------------------------------------------------------------
|									  |
|			MANUEL D'INSTRUCTION				  |
|									  |
 --------------------------------------------------------------------------

1. PRE-REQUIS

/!\ Ce Script est � ex�cuter dans le m�me r�pertoire que le fichier variable.py dans le cas d'une ex�cution automatique!

Le fichier variable.py est fourni au meme endroit que le script de sauvegarde. Il permet de configurer les variables les plus utilis�es et les identifiants gmail

Ce manuel d'instruction est �galement disponible au sein du script avec le choix "4" dans le menu.

Une connexion internet est requise pour l'envoi par mail et le t�l�chargement des pr�-requis


--------------------------------------------------------------------------------------------------------------------------------------------------------------

2. SON FONCTIONNEMENT(sauvegarde)

Le script a pour fonction de sauvegarder et restaurer l'�tat d'un site wordpress.
Pour ce faire, il va r�aliser une copie du r�pertoire html, de la base de donn�es et du crontab si il y en a un (le crontab est utilis� pour automatiser l'ex�cution du script).

Ces fichiers vont �tre copi�s dans un repertoire se nommant avec la date du jour de sauvegarde. L'emplacement de la sauvegarde est � definir via le script ou dans variable.py

Une fois cr�ee, une copie sera r�alis�e sur un serveur distant. A nouveau le choix du serveur est � definir

--------------------------------------------------------------------------------------------------------------------------------------------------------------

3. SON FONCTIONNEMENT(sauvegarde_auto)

Une seconde fonction existe dans le cas d'une ex�cution automatique  (choix "3"). 

Comme dit pr�c�demment ce dernier doit �tre ex�cut� en pr�cense du fichier variable.py!!

Il va notamment importer les variables qui s'y trouvent. Il est donc important de bien verifier les informations et de r�aliser un test de fonctionnement avant de l'automatiser via crontab ou autres..

Dans le cas ou le fichier n'est pas pr�sent, un mail est envoy� � l'utilisateur/administrateur pour l'avertir que la sauvegarde a potentiellement pas eu lieu.

Le processus de sauvegarde est le m�me que pour la version manuelle

----------------------------------------------------------------------------------------------------------------------------------------------------------------

4. SON FONCTIONNEMENT(restauration)

Concernant la restauration, le script va demander l'emplacement du repertoire contenant les fichiers necessaires � la restauration mais �galement la date de sauvegarde souhait�e.
Dans un second temps il va verifier la pr�sence des fichiers puis copier/restaurer les fichiers.

Si le dossier n'est pas pr�sent en local, une option permet de le telecharger depuis un serveur distant


Pour plus dinformations, voici le fonctionnement de la restauration:
	-Copie du repertoire html vers /var/www/html (cela permet de ne pas reconfigurer apache par defaut)
	-Cr�ation de la base de donn�es et de l'utilisateur Wordpress (le mot de passe
	-Restauration de la base Wordpress (via le fichier .mysql)
	-Restauration du crontab
	-Redemarrage de apache
	-Enjoy :)

----------------------------------------------------------------------------------------------------------------------------------------------------------------

5. MAIL

Cette fonction n'est utilis�e que lors de la sauvegarde automatique!

L'adresse mail exp�ditrice est � importer via le fichier variable.py

Idem pour le mot de passe.

