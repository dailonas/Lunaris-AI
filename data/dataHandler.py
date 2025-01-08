import os
import sqlite3 

class dataHandler(): # Class pour la gestion des datas
    def __init__(self, database_name: str): # Fonction d'initialisation
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}") # connection à la base de données
        self.con.row_factory = sqlite3.Row # Permet de dire à sqlite d'envoyer des distionnaire plutôt que des listes
    
    def create_message(self, UserId: int,msgUser: str, msgBot : str): #Permet de créer un objet "message" qui aurat qui correspondra aux message de luna et ceux de l'utilisateur
        cursor = self.con.cursor() # Permet la communication avec la base de donnée
        query = f"INSERT INTO message (UserId, msgUser, msgBot) VALUES (?, ?, ?);" # Permet d'inserer dans la table message "message", le message de l'utilisateur et celui du bot !
        cursor.execute(query, (UserId, msgUser, msgBot,)) # Pour executer les insertions des messages dans la table message !
        cursor.close() # Fermer le curseur après utilisateur ! 'toujours' ! 
        self.con.commit() # Pour sauvegarder les modifications !

    def get_msgUser(self): # Permet de récupérer tous les messages stockés dans la base de données
        cursor = self.con.cursor() # Communication avec la base de données
        query = "SELECT msgUser FROM message;" # Requête SQL pour récupérer tous les messages
        cursor.execute(query) # Execution de la requête
        cursor.close() # Fin de la communication avec la base de données

    def get_msgBot(self): # Permet de récupérer tous les messages stockés dans la base de données
        cursor = self.con.cursor() # Communication avec la base de données
        query = "SELECT msgBot FROM message;" # Requête SQL pour récupérer tous les messages
        cursor.execute(query) # Execution de la requête
        cursor.close() # Fin de la communication avec la base de données