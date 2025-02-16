#------------------------ API & TOKEN CONFIG -------------
application_key = "Le token de ton application discord"
api_key = "Ta API KEY pour le modèle de langue"
model = "llama-3.2-11b-vision-preview" #par défaut vous utilisérez ce modèle de langue.
#---------------------------------------------------------------------------------------------------------------
#------------------------- APP CONFIG --------------------------------------------------------------------------
prefix = "" #préfix pour l'appel des commands (via les slashs commandes).
admin = [] #liste des administrateurs (le votre par defaut) du bot(via les slashs commandes)
#---------------------------------------------------------------------------------------------------------------
#------------------------- PERSONALITY CONFIG ------------------------------------------------------------------
system = "Tu est une ami qui repond toujours vrai, même quand ça fait mal." #il defini le Comportement de votre appllication (bot, via les slashs commandes).
keyWord = ["Luna","Lunaris","luna","lunaris"] #Liste des mots clés utilisables pour discuter avec le bot (à modifier).
cycle = ["Tell them I was happy !", "Les do this !", "The noblest art is that of making others happy !", "Open source project !", "Made by lunaris support !",] #les statuts aléatoire que prend le bot.
#---------------------------------------------------------------------------------------------------------------------
#------------------------- MEMORY CONFIG ------------------------------------------------------------
max_history = 5 #le nombre maximum de messages à stocker dans l'historique est de cinq (5) par défaut.
del_history = 3600 #le cycle de suppresso ou de netoyage de la memoire pour un utilisateur (1h par défaut).
#--------------------------------------------------------------------------------------------------------
# NOTE! --------------------------------------------------------------------------------------------------
"""
Toutes ces imformations sont requisent. Si vous avez des difficulté, veulliez contacter le support !
En cas de modification du code source, vous être entièrement resposable des failles ou erreurs pourvant en résulter.
-- Les slash commande ne sont pas encore prête, veulliez faire les config via ce fichier !
"""
#-------------------------------------------------------------------------------------------------------------