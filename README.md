# Lunaris-AI

        userId = message.author.id
        UserMsg = message.content

        # prompt = message.content.replace(bot.user.mention, "").strip()

        try: # Vérification du contenu du message pour éviter les répliques

            # Génération de la réponse via le modèle d'IA
            response = generate_groq_response(prompt)
            # Séparation de la réponse en parties pour éviter les dépassements de caractères
            response_parts = split_message(response)
            # Envoi de chaque partie de la réponse
            for part in response_parts:
                await message.reply(part)