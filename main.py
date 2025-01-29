#-------------------------
# IMPORT DES MODULES REQUIS
import discord
import os
import time
import config
import memory
from groq import Groq
from itertools import cycle
from discord.ext import commands, tasks
#-------------------------------------


# ----------------------------------------------------
# CREATION DES FONCTIONS UTILES
def efface(): #fonction pour netoyer le terminal
        os.system('cls' if os.name == 'nt' else 'clear')

def slowType(text, delay=0.2): #fonction qui permet d'afficher du texte de manière lente et progressive.
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def split_message(message, max_length=2000): #fonction pour la gestion du nombre de caractère max des reponses.
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]
# -------------------------------------------------------------------------------------------------------------


#---------------------------------------------
# CONFIGURATION DES AJUSTEMENTS DE L'APPLICA
status = cycle([  
    "Tell them I was happy !",
    "Les do this !",
    "The noblest art is that of making others happy !",
    "Open source project !",
    "Made by lunaris support !", 
]) #une liste circlique qui contient tous les differents status(modifiables) de l'applications.
@tasks.loop(seconds=5)
async def status_swap(): #fonction pour la lecture de la liste circlique des status.
    await bot.change_presence(activity=discord.CustomActivity(next(status)))
#-------------------------------------------------------------------------------------


#-----------------------------------
# CONFICURATION DES CLIENTS API
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = Groq(api_key=config.api_key)
#------------------------------------


#------------------------------------------------
# EVENEMENTS DE LA MISE EN LIGNE DE L'APPLICATION
print("Démarrage de la connexion avec le client discord")
@bot.event
async def on_ready(): #fonction de lancement.
    print(f'\033[92m{bot.user.name} est en ligne ✔ \033[0m')
    status_swap.start() #lancement des status.
#----------------------------------------------------------------


#--------------------------------------
# EVENEMENT PRINCIPAL DE L'APPLICATION
conversation_manager = memory.memory(max_history=5) # modifiable
"""
    NOTE:
    Cette partie du code permet de gérer les interactions entre le bot et les utilisateurs.
    conversation_manager, est la une instance de classe memory qui stocke l'historique
    des conversations de chaque utilisateur pour une melleiur interaction avec
    l'application. le nombre maximum de messages à stocker dans l'historique est de cinq
    (5) par défaut. Vous pouvez le modifier en changeant le cinq (5) par le nombre
    que vous voulez.
"""
@bot.event
async def on_message(message): #fonction de l'evenement pour l'ineraction avec l'application.
    keyWord = ["Luna","Lunaris","luna","lunaris"]
    """
    NOTE:
    Liste des mots clés pour détecter les messages mentionnant le bot dans un serveur.
    Modifiez le avec le nom de votre application en respectant le début de chaque mots clés.
    """

    if message.author.bot: return #(1)
    """
    Condition qui verifie que l'utilisateur n'est pas un bot.
    """
    
    if isinstance(message.channel, discord.DMChannel):#(2)
        """
        Condition qui verifie que l'utilisateur est dans un canal privé (MP).
        """
        userId = message.author.id
        UserMsg = message.content
        #prompt = conversation_manager.manage_chatting(userId, UserMsg)
        prompt = conversation_manager.manage_chatting(userId, UserMsg)

        try: 
            response_parts = split_message(prompt) #séparation de la réponse en parties pour éviter les dépassements de caractères.
            for part in response_parts: #envoi de chaque partie de la réponse.
                await message.reply(part)
                return

        except Exception as e: #gestion des erreurs
            return f"Une erreur s'est produite: {e}"
    
    if bot.user.mention in message.content or any(keyword in message.content for keyword in keyWord) or message.reference and message.reference.resolved and message.reference.resolved.author == bot.user:
        """
        Condition qui permet de détecter les messages mentionnant le bot dans un serveur.
        """
        userId = message.author.id
        UserMsg = message.content
        prompt = conversation_manager.manage_chatting(userId, UserMsg)

        try:
            response_parts = split_message(prompt) #séparation de la réponse en parties pour éviter les dépassements de caractères.
            for part in response_parts: #envoi de chaque partie de la réponse.
                await message.reply(part)

        except Exception as e: #gestion des erreurs.
            return await f"Une erreur c'est produite: {e}"
#-------------------------------------------------------------


#---------------------------
# LANCEMENT DE L'APPLICATION
bot.run(config.application_key)
#------------------------------
