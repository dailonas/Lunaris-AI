#-------------------------------------- Importations des modules --------------------------------
import discord
import string
import ctypes
import os
import time
import config

from groq import Groq
from itertools import cycle
from discord.ext import commands, tasks
from data.dataHandler import dataHandler
#------------------------------------------------- Configuration des outils ---------------------------
time.sleep(2) # Pause avant le demarrrage du programme

def efface(): # Fonction pour netoyer le terminal
        os.system('cls' if os.name == 'nt' else 'clear')

def slowType(text, delay=0.2): # Fonction qui permet d'afficher du texte de manière lente et progressive
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

data_Handler = dataHandler("database.db") # Permet de faire des requêtes à la base de données

#------------------------------------------------- Configuration des clients ---------------------------
efface() # Clear du terminal !
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = Groq(api_key=config.groq_api_key)
#------------------------------------------------- Programme de fonctionnement ---------------------------

slowType("Démarrage de la connexion avec le client discord\n")

def split_message(message, max_length=2000): # fonction pour la gestion du nombre de caractère max des reponses
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]


def generate_groq_response(prompt): # Gestion de la generation des reponses via un modèle d'ia
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Tu est une intelligente assistante, réaliste et qui donne des reponses brèves mais de qualitées.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.2-11b-vision-preview"  #"llama3-8b-8192", 
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Une erreur c'est produite: {e}"

    
#------------------ Sous programme de lancement  ------------------
status = cycle([ # liste des statuts aléatoire 
    "Tell them I was happy !",
    "Les do this !",
    "The noblest art is that of making others happy !",
    "Add me for help !",
    "Made by landhaven !", 
])
@tasks.loop(seconds=5) # definition du temps d'attente !
async def status_swap():# fonction pour la sélection du statut
    await bot.change_presence(activity=discord.CustomActivity(next(status))) # await bot.change_presence(activity=discord.Game(next(status)))
@bot.event
async def on_ready(): # Lancement du bot !
    slowType(f'\033[92m{bot.user.name} est en ligne ✔ \033[0m')
    status_swap.start()  # Statut du bot du type activité !
    # await bot.change_presence(activity=discord.CustomActivity("L'élégance, c'est quand l'intérieur est aussi joli que l'extérieur ")) # Statut du bot de type message !

#------------------ Sous programme de detection et réponse des messages -----
@bot.event
async def on_message(message): # Detection des messages envoyés aux quelles il faut repondre

    if message.author.bot: return # condition de base pour tout le programme
    
    # Programme pour les messages privés (MP)
    if isinstance(message.channel, discord.DMChannel):
        prompt = message.content.replace(bot.user.mention, "").strip()

        try: # Vérification du contenu du message pour éviter les répliques

            # Génération de la réponse via le modèle d'IA
            response = generate_groq_response(prompt)
            # Séparation de la réponse en parties pour éviter les dépassements de caractères
            response_parts = split_message(response)
            # Envoi de chaque partie de la réponse
            for part in response_parts:
                await message.reply(part)
                return

        except Exception as e: 
            # Gestion des erreurs
            return f"Une erreur s'est produite: {e}"
        
    keyWord = ["Luna","Lunaris","luna","lunaris"] # Mot clé
    # Programme de reponse pour les serveurs !
    if bot.user.mention in message.content or any(keyword in message.content for keyword in keyWord) or message.reference and message.reference.resolved and message.reference.resolved.author == bot.user:
        prompt = message.content.replace(bot.user.mention, "").strip()

        try: # Vérification du contenu du message pour éviter les répliques

            # Génération de la réponse via le modèle d'IA
            response = generate_groq_response(prompt)
            # Séparation de la réponse en parties pour éviter les dépassements de caractères
            response_parts = split_message(response)
            # Envoi de chaque partie de la réponse
            for part in response_parts:
                await message.reply(part)
        except Exception as e:
            return await f"Une erreur c'est produite: {e}"

        UtilisateurId = message.author.id 
        data_Handler.create_message(UtilisateurId, prompt, part)
            # Ajout des messages dans la base de données

#------------------------------------------------- Fin du programme ---------------------------
bot.run(config.token_discord) # Lancement du program
