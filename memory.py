#--------------------------
# IMPORT DES FICHIER REQUIS
import config
import discord 
from groq import Groq 
#--------------------


#--------------------------------
# CLIENT POU INTERAGIR AVEC GROQ
client = Groq(api_key=config.api_key)
#-------------------------------------


#---------------------------------------------------
# FONCTION PRINCIPALE POUR LA CONFIGURATION DE L'IA
def generate_groq_response(prompt): #fonction de gestion de la generation des reponses via un modèle d'ia
    try:
        prompt = " ".join(prompt) #concaténer tous les éléments de la liste (l'historique de la conversation) en une seule chaîne.

        chat_completion = client.chat.completions.create( #utiliser l'API Groq pour générer une réponse à partir du prompt.
            messages=[
                {
                    "role": "system",
                    "content": config.system
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=config.model
        )
           
        return chat_completion.choices[0].message.content #retourner la réponse générée.
    except Exception as e: #gestion des erreurs.
        return f"Une erreur c'est produite: {e}"
#-------------------------------------------------


#-------------------------------------
# CLASSE DE GESTION DE LA CONVERSATION
class memory:
    def __init__(self, max_history=5): # Initialise le gestionnaire de conversations.
        # max_history: Le nombre maximum de messages à conserver dans l'historique.
        
        self.conversations = {}
        self.max_history = max_history

    def manage_chatting(self, user_id, message_content): # Gère la conversation avec l'utilisateur.
        # message_content: Le contenu du message de l'utilisateur.
        
        if user_id not in self.conversations: # Récupérer l'historique de la conversation ou l'initialiser
            self.conversations[user_id] = []

        self.conversations[user_id].append(message_content) # # Ajouter le nouveau message à l'historique
        
        #reponse = self.generer_reponse(self.conversations[user_id]) # Générer une réponse
        reponse = generate_groq_response(self.conversations[user_id])

        # Mettre à jour l'historique de la conversation avec la réponse générée
        self.conversations[user_id].append(reponse) # Ajouter la réponse à l'historique
        self.conversations[user_id] = self.conversations[user_id][-self.max_history:] # Limiter l'historique à la taille maximale
        return reponse

    def get_history(self, user_id): # Récupère l'historique de la conversation pour un utilisateur donné.
        return self.conversations.get(user_id, []) # Retourner une liste vide si aucune conversation n'est disponible
#----------------------------------------------------------------------------------------------------------------------