application_key = "Le token de ton application discord"
api_key = "Ta API KEY pour le modèle de langue"
model = "llama-3.2-11b-vision-preview" #par défaut vous utilisérez ce modèle de langue.
system = "Tu est une intelligente assistante, réaliste et qui donne des reponses brèves mais de qualitées." #par défaut, votre application se comporteras comme suite.
keyWord = ["Luna","Lunaris","luna","lunaris"]
"""
    NOTE:
    Liste des mots clés pour détecter les messages mentionnant le bot dans un serveur.
    Modifiez le avec le nom de votre application en respectant le début de chaque mots clés.
    """
max_history = 5
"""
    NOTE:
    Cette partie du code permet de gérer les interactions entre le bot et les utilisateurs.
    conversation_manager, est la une instance de classe memory qui stocke l'historique
    des conversations de chaque utilisateur pour une melleiur interaction avec
    l'application. le nombre maximum de messages à stocker dans l'historique est de cinq
    (5) par défaut. Vous pouvez le modifier en changeant le cinq (5) par le nombre
    que vous voulez.
"""
del_history = 3600

# NOTE! --------------------------------------------------------------------------------------------------
"""
Toutes ces imformations sont requisent. Si vous avez des difficulté, veulliez contacter le support !
En cas de modification du code, vous être entièrement resposable des failles ou erreurs pourvant en résulter.
"""
#-------------------------------------------------------------------------------------------------------------