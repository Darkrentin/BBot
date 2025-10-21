import discord
from discord.ext import commands

# --- CONFIGURATION ---
# Mets le token de ton bot ici (gardes-le secret !)
TOKEN = "METS_TON_TOKEN_DE_BOT_ICI"

# Remplace les zéros par les IDs que tu as copiés
ID_DE_TON_POTE = 517015355768438804  # !!! REMPLACE ÇA !!!
TON_PROPRE_ID = 481080387389489173  # !!! REMPLACE ÇA !!!

# La phrase que le bot enverra
PHRASE_A_ENVOYER = "Test" 
# --- FIN CONFIGURATION ---


# On définit les "Intents" (permissions) dont le bot a besoin
intents = discord.Intents.default()
intents.messages = True      # Pour recevoir des messages
intents.message_content = True # Pour LIRE le contenu des messages
intents.guilds = True        # Pour savoir sur quels serveurs il est
intents.dm_messages = True   # Pour les commandes en MP

# On crée le bot avec un préfixe de commande (ex: !toggle)
bot = commands.Bot(command_prefix='!', intents=intents)

# Variable globale pour savoir si la blague est active
prank_active = False

@bot.event
async def on_ready():
    """S'affiche dans la console quand le bot est connecté."""
    print(f'Connecté en tant que {bot.user}')
    print('-------------------------')

@bot.event
async def on_message(message):
    """Cette fonction se déclenche à CHAQUE message."""
    
    # 1. On ignore les messages du bot lui-même (pour éviter les boucles)
    if message.author == bot.user:
        return

    # 2. On vérifie si la blague est active ET si l'auteur est ton pote
    global prank_active
    if prank_active and message.author.id == ID_DE_TON_POTE:
        # On s'assure qu'il n'est pas en train de nous parler en MP
        if message.guild:
            try:
                # On envoie la phrase dans le même salon
                await message.channel.send(PHRASE_A_ENVOYER)
            except discord.Forbidden:
                print(f"Je n'ai pas la permission d'envoyer un message dans {message.channel.name}")

    # 3. Important : On laisse les commandes (comme !toggle) fonctionner
    await bot.process_commands(message)


@bot.command()
async def toggle(ctx):
    """La commande pour activer/désactiver la blague."""
    
    # On vérifie si c'est bien TOI qui envoie la commande
    # ET si c'est bien en Message Privé (MP)
    if ctx.author.id == TON_PROPRE_ID and isinstance(ctx.channel, discord.DMChannel):
        global prank_active
        
        # On inverse l'état (True -> False, False -> True)
        prank_active = not prank_active
        
        status = "ACTIVÉ" if prank_active else "DÉSACTIVÉ"
        await ctx.send(f'**Mode blague pour ton pote est maintenant : {status}**')
        
    elif ctx.author.id == TON_PROPRE_ID:
        # Si tu essaies depuis un serveur
        await ctx.send('Psst... Envoie-moi cette commande en message privé !')


# On lance le bot
try:
    bot.run(TOKEN)
except discord.LoginFailure:
    print("ERREUR: Le token du bot est invalide. Vérifie-le !")