import string

SERVER_PUBLIC_RSA_KEY = {"n": 3233, "e": 17}
SERVER_PRIVATE_RSA_KEY = {"n": 3233, "e": 413}
PRIVATE_DH = 17
CHARACTERS_SET = string.ascii_lowercase + "!,.:? "
users_info = {}

async def sayHello(discord_msg):
    await discord_msg.reply("On se fait un TLS ? Tu sais chiffrer ?")


async def sendUserInfo(discord_msg):
    await discord_msg.reply(
                users_info[discord_msg.author.name] 
                if discord_msg.author.name in users_info 
                else "Aucune information enregistrée sur vous pour le moment !"
        )
     
async def cesar(discord_msg, params, encode=1):
    if len(params) == 2:
        secret, key = params
        secret = secret.lower()
        characters_rotated = CHARACTERS_SET[encode *
                                            int(key):] + CHARACTERS_SET[:encode*int(key)]
        dico = {k: v for k, v in zip(CHARACTERS_SET, characters_rotated)}
        secret_decoded = ''.join(list(map(lambda c: dico[c], secret)))
        await discord_msg.reply(secret_decoded)
    else:
        await discord_msg.reply("Nombre de paramètre invalide")



async def vigenere(discord_msg, params, encode=1):
    if len(params) == 2:
        text_msg, pwd = params
        text_msg = str(text_msg).lower()
        pwd = str(pwd)
        pwd = pwd.lower()
        converted_text = []
        for i, c in enumerate(text_msg):
            index_in_characters_set = CHARACTERS_SET.index(c)
            corresponding_charac_in_pwd = pwd[i % len(pwd)]
            if corresponding_charac_in_pwd.isdigit():
                offset = int(corresponding_charac_in_pwd)
            else:
                offset = CHARACTERS_SET.index(corresponding_charac_in_pwd) + 1
            cypher_c = CHARACTERS_SET[(
                index_in_characters_set + encode*offset) % len(CHARACTERS_SET)]
            converted_text.append(cypher_c)
        await discord_msg.reply("".join(converted_text))
    else:
        await discord_msg.reply("Nombre de paramètre invalide")


async def DH_clientHello(discord_msg, params):
    if len(params) == 3:
        generator, modulus, A = params
        B = int(generator)**int(PRIVATE_DH) % int(modulus)
        shared_secret = int(A)**int(PRIVATE_DH) % int(modulus)
        users_info[discord_msg.author.name] = {}
        users_info[discord_msg.author.name]["DH"] = {}
        users_info[discord_msg.author.name]["DH"]["shared_secret"] = shared_secret
        users_info[discord_msg.author.name]["DH"]["generator"] = generator
        users_info[discord_msg.author.name]["DH"]["modulus"] = modulus
        answer = "Les paramètres de Diffie-Hellman ont bien été enregistrés \n" \
        "Le secret partagé a bien été calculé côté serveur\n" \
        f"Voici le nombre Diffie-Hellman intermédiaire qui vous servira à calculer le secret partagé : {B}"
        await discord_msg.reply(answer)
    else:
        await discord_msg.reply("Le nombre de paramètres est non valide.")
        
async def DH_decodeMsg(discord_msg, params):
    vigenere_params = (params[0], users_info[discord_msg.author.name]["DH"]["shared_secret"])
    await vigenere(discord_msg, vigenere_params, encode=-1)


async def proveIdentity(discord_msg):
    message = 42
    ciphered = encrypt_RSA(SERVER_PRIVATE_RSA_KEY, message)
    answer = f"Voici ma clé publique : {SERVER_PUBLIC_RSA_KEY} \n" 
    answer += f"Voici le message non chiffré : {message} \n" 
    answer += f"Voici le message chiffré avec ma clé privée : {ciphered}"
    await discord_msg.reply(answer)


def encrypt_RSA(public_key, msg):
    return int(msg)**int(public_key["e"]) % int(public_key["n"])

# def serverHello(author, server_dh_key):
#     answer = f"-------\n" \
#         "Server Hello\n" \
#         f"Message à destination de  : {author.mention},\n" \
#         "TLS version : 1.3 \n" \
#         "Certificat SSL du serveur : trust me ;) \n" \
#         f"Diffie-Hellman generator parameter : {PUBLIC_GENERATOR_DH} \n" \
#         f"Diffie-Hellman prime parameter : {PUBLIC_PRIME_DH} \n" \
#         f"Diffie-Hellman Server Key : {server_dh_key} \n" \
#         "---------"
#     # users_info[author.id] = UserData(author.name, server_dh_key, "", "")
#     return answer




# def decrypt_RSA(private_key, msg, public_key=SERVER_PUBLIC_RSA_KEY):
#     return int(msg)**int(private_key) % int(public_key["n"])


# def encode_characters(message):
#     return "".join(list(map(lambda c: encoding_dic[c], list(message))))


# def decode_characters(message):
#     split_msg = [message[i:i+2] for i in range(0, len(message), 2)]
#     return "".join(list(map(lambda c: decoding_dic[c], split_msg)))
