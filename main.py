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
status = cycle(config.cycle) 
@tasks.loop(seconds=5)
async def status_swap(): #fonction pour la lecture de la liste circlique des status.
    await bot.change_presence(activity=discord.CustomActivity(next(status)))
#-------------------------------------------------------------------------------------


#-----------------------------------
# CONFICURATION DES CLIENTS API
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=config.prefix, intents=intents)
client = Groq(api_key=config.api_key)
#------------------------------------


#------------------------------------------------
# EVENEMENTS DE LA MISE EN LIGNE DE L'APPLICATION
slowType("POWERED BY DAILONAS..", 0.1)
time.sleep(1)
efface()
slowType("LUNARIS AI - V1.\n", 0.1)
print("Démarrage de la connexion avec le client discord")
@bot.event
async def on_ready(): #fonction de lancement.
    print(f'\033[92m{bot.user.name} est en ligne ✔ \033[0m')
    status_swap.start() #lancement des status.
    try:
        synced = await bot.tree.sync()
        print(f"\033[92mCommandes synchronisées : {len(synced)} commandes ✔\033[0m")
    except Exception as e:
        print(f"\033[91mErreur lors de la synchronisation des commandes slash et préfixes : {e}\033[0m")
#----------------------------------------------------------------


#--------------------------------------
# EVENEMENT PRINCIPAL DE L'APPLICATION
conversation_manager = memory.memory(max_history=config.max_history) # management de l'historie des conversations.
memory_instance = memory.memory() # instance de la classe memory
memory_instance.clear_inactive_conversations(config.del_history) # nettoyer les conversations inactives après 1 heure (par défaut).

@bot.event
async def on_message(message): #fonction de l'evenement pour l'ineraction avec l'application.
    keyWord = config.keyWord

    if message.author.bot: return #(1) Condition qui verifie que l'utilisateur n'est pas un bot.
    
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

#-------------------------- LES SLASH COMMANDS -----------------------
@bot.tree.command(name="memory", description="Configuration de la memoire.")
async def latency(interaction: discord.Interaction, value1: str, value2: str):
    case_one = value1
    case_two = value2
    if interaction.author.id not in config.admin:
        try:
            await interaction.response.send_message("Vous n'avez pas les permissions pour effectuer cette action.")
            return
        except Exception as e:
            return await f"Une erreur c'est produite: {e}"

        #----------------------------------------------------------------
@bot.tree.command(name="admin", description="Gérer les administrateur du bot.")
async def prompt(interaction: discord.Interaction, value: str, value2: int):
    case_one = value
    case_two = value2
    if interaction.author.id not in config.admin:
        try:
            await interaction.response.send_message("Vous n'avez pas les permissions pour effectuer cette action.")
            return
        except Exception as e:
            return await f"Une erreur c'est produite: {e}"

    await interaction.response.send_message(f"Le promptre est : `{config.api_key}`")

        #--------------------------------------------------------------------
@bot.tree.command(name="config", description="Afficher la configuration de l'application.")
async def prompt(interaction: discord.Interaction):
    thumbnail = bot.user.avatar
    synced = await bot.tree.sync()
    embed = discord.Embed(
        title=f"Informations sur le serveur : {bot.user.name}",
        description=f"Description : bot.user.description",
        color=discord.Color.blue()
    )
    embed.add_field(name="**__API & TOKEN CONFIG__**", value=f"Le token : {config.application_key}\nLa clé API: {config.api_key}\nLe modèle de langue: {config.model}", inline=True)
    embed.add_field(name="**__APP CONFIG__**", value=f"Le préfix: {config.prefix}\nLes admins: {config.admin}", inline=True)
    embed.add_field(name="**__PERSONALITY CONFIG__**", value=f"Prompt: {config.system}\nMots clés: {config.keyWord}\nLes status: {config.cycle}", inline=True)
    embed.add_field(name="**__MEMORY CONFIG__**", value=f"Nombre max de message stocké: {config.max_history}\nCycle de netoyage: {config.del_history}", inline=True)
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text=f"Commandes : {len(synced)}")
    embed.set_image_url("https://media.discordapp.net/attachments/998966700806508684/1096875217101541416/WhiteLine.png?ex=67b23826&is=67b0e6a6&hm=e6a136d1001590987404ff77d0c52628d77f7f97ca11d0d50a47aa964cdb433e&=&format=webp&quality=lossless&width=1441&height=18")
    if interaction.author.id not in config.admin:
        try:
            await interaction.response.send_message("Vous n'avez pas les permissions pour effectuer cette action.")
            return
        except Exception as e:
            return await f"Une erreur c'est produite: {e}"
    elif interaction.author.id in config.admin:
        try:
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            return await f"Une erreur c'est produite: {e}"

#----------------------------------------------------------------------------------


#---------------------------
# LANCEMENT DE L'APPLICATION
bot.run(config.application_key)
#------------------------------
