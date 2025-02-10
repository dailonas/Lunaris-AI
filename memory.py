#--------------------------
# IMPORT DES FICHIER REQUIS
import config
import discord 
import datetime
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
        self.last_message_time = {} # attribut pour enregistrer l'heure du dernier message reçu pour chaque utilisateur.

    def manage_chatting(self, user_id, message_content): # Gère la conversation avec l'utilisateur.
        # message_content: Le contenu du message de l'utilisateur.
        
        if user_id not in self.conversations: # Récupérer l'historique de la conversation ou l'initialiser
            self.conversations[user_id] = []

        self.conversations[user_id].append(message_content) # # Ajouter le nouveau message à l'historique
        self.last_message_time[user_id] = datetime.datetime.now() # Time de la conversation ou l'initialiser
 
 #------------------------------------- A voir
        if user_id in self.conversations and len(self.conversations[user_id]) > 10:
         del self.conversations[user_id][:10] 

        if len(self.conversations[user_id]) > self.max_history:
         del self.conversations[user_id][:self.max_history]
#-----------------------------------------
        reponse = generate_groq_response(self.conversations[user_id]) # Générer une réponse à partir de l'historique de la conversation ou non.

        # Mettre à jour l'historique de la conversation avec la réponse générée
        self.conversations[user_id].append(reponse) # Ajouter la réponse à l'historique
        self.conversations[user_id] = self.conversations[user_id][-self.max_history:] # Limiter l'historique à la taille maximale.
        return reponse
    
    def clear_inactive_conversations(self, inactive_time_threshold=3600):
            current_time = datetime.datetime.now()
            inactive_users = [user_id for user_id, last_message_time in self.last_message_time.items()
                if (current_time - last_message_time).total_seconds() > inactive_time_threshold]

            for user_id in inactive_users:
               del self.conversations[user_id]
               del self.last_message_time[user_id]

    def get_history(self, user_id): # Récupère l'historique de la conversation pour un utilisateur donné.
        return self.conversations.get(user_id, []) # Retourner une liste vide si aucune conversation n'est disponible
#----------------------------------------------------------------------------------------------------------------------