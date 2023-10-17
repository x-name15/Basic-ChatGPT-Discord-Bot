import discord, os, re, json, requests, asyncio
import openai, random
from gtts import gTTS
import youtube_dl
import tempfile
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord import Game, Embed, File
from keep_alive import keep_alive

def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config

config = load_config()
TOKEN = config["token"]
GPT_API_KEY = config["gpt_api_key"]
PREFIX = config["prefix"]
RPC = config["RPC"]
version = config["version"]
openai.api_key = GPT_API_KEY

intents = discord.Intents().all()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("AI listo para su uso!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(RPC))

@bot.command()
async def help(ctx):
    my_image_url = 'discordurl xdxdxd'
    help_embed = discord.Embed(
        title="Ayuda, no se que comandos son!!!1!",
        description=f"¡Bienvenido {ctx.author.mention} al embed de ayuda de WKND-AI potenciado con ChatGPT!",
        color=discord.Color.blue()
    )
    help_embed.add_field(name="**chat**", value=f"Usame para como chatbot | Uso: **{PREFIX}chat [prompt]**", inline=True)
    help_embed.add_field(name="**resumir**", value=f"Te puedo resumir un texto! | Uso: **{PREFIX}resumir** [texto que soporte discord]", inline=True)
    help_embed.add_field(name="**corregir**", value=f"Te puedo corregir gramaticalmente oraciones o texto en general! | Uso: **{PREFIX}corregir** [texto a corregir]", inline=True)
    help_embed.add_field(name="**code**", value=f"Te dare codigo en un archivo TXT! | Uso: **{PREFIX}code** [solicitud] [lenguaje] | Ejemplo: {PREFIX}code algoritmo de ordenamiento en C++", inline=True)
    help_embed.add_field(name="**traducir**", value=f"Te puedo traducir un mensaje! | Uso ejemplo: **{PREFIX}traducir** Salut, comment vas-tu ? al español ", inline=True)
    help_embed.add_field(name="**yonunca**", value=f"Lo dice el nombre no? | Uso: **{PREFIX}yonunca**", inline=True)
    help_embed.add_field(name="**poesia**", value=f"Te genero poesia! |Uso: **{PREFIX}poesia** [palabra que usara]", inline=True)
    help_embed.add_field(name="**recomendar**", value=f"Te puedo recomendar 10 cosas! | Uso: **{PREFIX}recomendar** [libro/peli/musica] [genero/cosa]", inline=True)
    help_embed.add_field(name="**join**", value=f"Comando de uso Voz-Afk | Uso: **{PREFIX}join** | Este solo entrara al canal donde se ha invocado para hablar", inline=True)
    help_embed.add_field(name="**speak**", value=f"Habla a traves del bot con el comando de uso tipo Voz-Afk | Uso: **{PREFIX}speak** [lo que quieres decir]", inline=True)
    help_embed.add_field(name="**explain**", value=f"El bot te dira lo que le consultes a traves del VC! | Uso: **{PREFIX}explain** [Lo que le desees preguntar o decir]", inline=True)
    help_embed.add_field(name="**leave**", value=f"Bota al bot del VC| Uso: **{PREFIX}leave**", inline=True)
    help_embed.set_footer(text=f"AI | Version {version} | wa")
    help_embed.set_image(url=my_image_url)
    await ctx.send(embed=help_embed)

@bot.command(name='chat')
async def chat_command(ctx, *, text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"User: {text}\nAI:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,)
    await ctx.reply(response.choices[0].text)

@bot.command(name='explain')
async def speak_command(ctx, *, text):
    await ctx.reply("Te dare la explicacion en VC, **recuerda que demorare un poco debido a la generacion del archivo MP3 y la reproduccion hablada**")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"User: {text}\nAI:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )
    reply = response.choices[0].text.strip()
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
        tts = gTTS(reply, lang='es', tld="com.mx")
        tts.save(temp_file.name)
    voice_client = ctx.voice_client
    voice_client.play(discord.FFmpegPCMAudio(temp_file.name))
    await asyncio.sleep(voice_client.duration)
    os.remove(temp_file.name)
  
@bot.command()
async def resumir(ctx, *, article):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Resuma el siguiente artículo:\n{article}\n---\n",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        summary = response.choices[0].text.strip()
        if len(summary) > 2000:
            with open("resumen.txt", "w") as file:
                file.write(summary)
            await ctx.reply(file=discord.File("resumen.txt"))
        else:
            await ctx.reply(f"Aquí está el resumen del artículo:\n{summary}")
    except Exception as e:
      await ctx.reply("Lo siento, no pude resumir ese artículo. Intenta con otro artículo.")

@bot.command()
async def traducir(ctx, *, args: str):
    try:
        words = [word.strip("\"") for word in args.split()]
        lang_index = len(words) - 1
        while lang_index >= 0:
            if len(words[lang_index]) == 2 and words[lang_index].isalpha():
                break
            lang_index -= 1
        if lang_index < 0:
            raise ValueError("No se especificó un código de idioma válido.")
        text = " ".join(words[:lang_index]).strip("\"")
        lang_destino = words[lang_index].lower()
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Traduce el siguiente texto al {lang_destino}:\n{text}\n---\n",
            temperature=0.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        translation = response.choices[0].text.strip()
        await ctx.reply(f"Aquí está el texto traducido al {lang_destino}:\n{translation}")
    except Exception as e:
        await ctx.reply(f"No pude traducir el texto. Comprueba que has proporcionado una cadena de texto válida y un código de idioma válido (en formato ISO 6390-1), y vuelve a intentarlo.")


@bot.command()
@commands.has_role("Giveaways")
async def greroll(ctx, message_id: int):
    try:
        msg = await ctx.fetch_message(message_id)
        winner = None
        for reaction in msg.reactions:
            if reaction.emoji == "🎉":
                users = await reaction.users().flatten()
                users.remove(bot.user)
                winner = random.choice(users)
        if winner is not None:
            await ctx.send(f"@here Jackpot!!!1 | Tenemos un **nuevo ganador:** {winner.mention}!")
    except Exception as e:
        await ctx.send("No se pudo realizar el reroll: {}".format(e))

@bot.command()
async def poesia(ctx, *, prompt: str):
    try:
      response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Escribe un poema que empiece con: \{prompt}\\n---\n",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
      poema = response.choices[0].text.strip()
      await ctx.reply(f"Aquí está tu poema:\n{poema}")
    except Exception as a:
        await ctx.reply(f"No pude traducir el texto. Comprueba que has proporcionado una cadena de texto válida y un código de idioma válido (en formato ISO 6390-1), y vuelve a intentarlo.")


@bot.command()
async def recomendar(ctx, tipo, cosa):
    prompt = f"Recomienda {tipo} {cosa}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    await ctx.reply(f"Carnalito te recomienda: {response.choices[0].text}")

@bot.command(name='yonunca')
async def yonunca(ctx):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt='Genera una pregunta para Yo Nunca Nunca:',
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    question = response.choices[0].text.strip()
    await ctx.reply(f'Yo nunca nunca {question}. ¿Quién ha hecho esto?')

@bot.command()
async def corregir(ctx, *, texto):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Corrige los errores gramaticales en la siguiente oración:\n\n{texto}\n\nCorrección:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    await ctx.reply(f"Corrección: {respuesta.choices[0].text.strip()}")

@bot.command(name='code')
async def code_command(ctx, *, query):
    parts = query.split("en")
    system = parts[0].strip()
    language = parts[1].strip()
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Genera código de {system} en {language}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    result = response.choices[0].text.strip()
    with open(f"{system}_en_{language}.txt", "w") as file:
        file.write(result)
    await ctx.reply("Claro, aqui te dejo un archivo TXT con el codigo solicitado!", file=discord.File(f"{system}_en_{language}.txt"))
    os.remove(f"{system}_en_{language}.txt")

@bot.command()
async def texto(ctx, *, tema):
    respuesta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Genera un texto relacionado con el tema {tema}:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    texto_generado = respuesta.choices[0].text
    await ctx.send(texto_generado)

@bot.command()
async def join(ctx):
    global voice_client
    if ctx.author.voice is None:
        await ctx.send("Debes estar en un canal de voz para usar este comando.")
    else:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
        await ctx.send(f"Conectado al canal de voz: {channel}")

@bot.command()
async def leave(ctx):
    global voice_client
    if voice_client is None:
        await ctx.send("No estoy conectado a ningún canal de voz.")
    else:
        await voice_client.disconnect()
        voice_client = None
        await ctx.send(f"Desconectado del canal de voz")

@bot.command()
async def speak(ctx, *, text):
    global voice_client
    if voice_client is None:
        await ctx.send(f"Debes unirme a un canal de voz usando el comando {prefix}join primero.")
    else:
        author_name = ctx.author.nick
        message = f"{author_name} dice: {text}"
        tts = gTTS(message, lang='es', tld="com.mx")  
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            tts.save(temp_file.name)
        voice_client.play(discord.FFmpegPCMAudio(temp_file.name))
        while voice_client.is_playing():
            await asyncio.sleep(1)
        os.remove(temp_file.name)

keep_alive()
bot.run(TOKEN)
