class memory:
    def __init__(self, max_history=10): # Initialise le gestionnaire de conversations.
        # max_history: Le nombre maximum de messages à conserver dans l'historique.
        
        self.conversations = {}
        self.max_history = max_history

    def gerer_conversation(self, user_id, message_content): # Gère la conversation avec l'utilisateur.
        # message_content: Le contenu du message de l'utilisateur.
        
        if user_id not in self.conversations: # Récupérer l'historique de la conversation ou l'initialiser
            self.conversations[user_id] = []

        self.conversations[user_id].append(message_content) # # Ajouter le nouveau message à l'historique
        
        reponse = self.generer_reponse(self.conversations[user_id]) # Générer une réponse
        
        # Mettre à jour l'historique de la conversation avec la réponse générée
        self.conversations[user_id].append(reponse) # Ajouter la réponse à l'historique
        self.conversations[user_id] = self.conversations[user_id][-self.max_history:] # Limiter l'historique
        return reponse

    def generer_reponse(self, historique): #  Génère une réponse en utilisant l'historique de la conversation.
        # historique: La liste des messages de l'historique.
    
        # Ici, vous pouvez implémenter votre logique de génération de réponse
        # Par exemple, en utilisant un modèle de langage ou une autre méthode
        # Pour l'instant, nous retournons une réponse factice
        return f"Voici une réponse générée basée sur l'historique de {len(historique)} messages."

    def obtenir_historique(self, user_id): # Récupère l'historique de la conversation pour un utilisateur donné.
        return self.conversations.get(user_id, []) # Une liste des messages de l'historique.