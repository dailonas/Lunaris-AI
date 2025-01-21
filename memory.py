import config # Importation de la config
import discord # Importation de la bibliotheque discordpy

from groq import Groq # Importation du module groq
client = Groq(api_key=config.api_key) # Création du client pour l'interaction avec l'api groq
def generate_groq_response(prompt): # Gestion de la generation des reponses via un modèle d'ia
    try:
        # Concaténer tous les éléments de la liste (l'historique de la conversation) en une seule chaîne
        prompt = " ".join(prompt)

        # Utiliser l'API Groq pour générer une réponse à partir du prompt
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
            model="llama-3.2-11b-vision-preview"  # le modèl de langue utilisé 
        )
        
        # Retourner la réponse générée
        return chat_completion.choices[0].message.content
    except Exception as e: # Retourner un message d'erreur si une exception se produit
        return f"Une erreur c'est produite: {e}"

# Classe pour gérer les conversations
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