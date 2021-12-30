import telebot
from telebot import types
import random
import time
from PIL import Image
from io import BytesIO

bot = telebot.TeleBot("5070337936:AAHHXOY6t8WgbrN8cwkPlESpkLybLcDrP8k")

@bot.message_handler(commands=['eu'])

def hizk_eu(message):
    
    global jokoan
    
    jokoan[message.chat.id]["hizkuntza"] = "eu"
    
@bot.message_handler(commands=['es'])

def hizk_es(message):
    
    global jokoan
    
    jokoan[message.chat.id]["hizkuntza"] = "es"

@bot.message_handler(commands=['hasi'])

def eskoba(message):
    
    global testuak
    
    global jokoan
    
    testuak = {
        "agurra": {"eu": "Kaixo {}, partida hastera doa. Zorte on!",
                   "es": "Hola {}, arranca la partida. ¡Suerte!"},
        "eskuandago": {"eu": "Hau da zure eskua:",
                       "es": "Ésta es tu mano:"},
        "mahaiandago": {"eu": "Hau da mahai gainean dagoena:",
                        "es": "Ésto es lo que hay sobre la mesa:"},
        "zeinkarta": {"eu": "Zein karta jokatuko duzu?",
                      "es": "¿Qué carta quieres jugar?"},
        "zermahaitik": {"eu": "Eta zer hartuko duzu mahaitik?",
                        "es": "¿Y qué vas a coger de la mesa?:"},
        "mahaiagarbi": {"eu": "Ez dago ezer ere mahai gainean.",
                        "es": "No hay nada sobre el tapete."},
        "zure eskoba": {"eu": "ESKOBA!",
                        "es": "¡ESCOBA!"},
        "botak eskoba": {"eu": "Botak eskoba egin du.",
                         "es": "Escoba del bot."},
        "jokatu": {"eu": "Jokatu",
                   "es": "Jugar"},
        "jok_urrezko7bai": {"eu": "Urrezko zazpia daukazu.",
                            "es": "Tienes el 7 de oros."},
        "jok_urrezko7ez": {"eu": "Ez daukazu urrezko zazpia.",
                           "es": "No tienes el 7 de oros."},
        "bot_urrezko7bai": {"eu": "Botak urrezko 7a dauka.",
                            "es": "El Bot tiene el 7 de oros."},
        "bot_urrezko7ez": {"eu": "Botak ez dauka urrezko 7a.",
                           "es": "El Bot no tiene el 7 de oros."},
        "irabazi": {"eu": "Zorionak, irabazi duzu.",
                    "es": "Enhorabuena, has ganado la partida."},
        "berdindu": {"eu": "Partida berdindurik bukatu da.",
                     "es": "Habéis empatado la partida."},
        "galdu": {"eu": "Botak irabazi du oraingoan.",
                  "es": "Esta vez ha ganado el Bot."},
        "botakjaurti":{"eu": "Botak karta jaurti du, hau dago mahai gainean:",
                       "es": "El bot ha echado una carta, queda sobre la mesa:"},
        "botjokaldia":{"eu": "Botak jokaldia egin du, {}, mahai gainean dago:",
                       "es": "El bot ha hecho jugada, {}, queda sobre la mesa:"},
        "banatu": {"eu": "Karta berriak banatu dizkizut.",
                   "es": "Te he repartido nuevas cartas."},
        "jok emaitza": {"eu": """{} puntu batu dituzu:
            {} karta.
            {} urrezko karta: {}
            {} zazpiko.
            {}
            {} eskoba partidan zehar.
        ""","es": """Has sumado {} punto(s):
            {} carta(s).
            {} carta(s) de oros: {}
            {} siete(s).
            {}
            Has logrado {} escoba(s) durante la partida.
                        """},
        "bot emaitza": {"eu": """Botak {} puntu batu ditu:
            {} karta.
            {} urrezko karta: {}
            {} zazpiko.
            {}
            {} eskoba partidan zehar.
        ""","es": """El Bot ha sumado {} punto(s):
            {} carta(s).
            {} carta(s) de oros: {}
            {} siete(s).
            {}
            Ha logrado {} escoba(s) durante la partida.
                        """},
        }
    
    try:
        jokoan
    except NameError:
        jokoan = {}
        
    txat_id = message.chat.id
    
    aurreko_hizk = "es"
    
    if txat_id in jokoan:
        aurreko_hizk = jokoan[txat_id]["hizkuntza"]
    
    jokoan[txat_id]={"baraja":[],"nire_eskua": [],"bot_eskua": [], "eskuak_irabazi":[],
                     "botak_irabazi":[],"mahaia": [],"jok_puntuak":0,
                     "bot_puntuak":0,"azkena":False,"hizkuntza":aurreko_hizk,"jokaldia":[]}
    
    jokoan[txat_id]["baraja"] = barajasortu()
    jokoan[txat_id]["nire_eskua"] = banatu(3, txat_id)
    jokoan[txat_id]["bot_eskua"] = banatu(3, txat_id)
    jokoan[txat_id]["mahaia"] = banatu(4, txat_id)
    
    bot.send_message(txat_id, testuak["agurra"][jokoan[txat_id]["hizkuntza"]].format(message.from_user.first_name))
    
    print(f"{message.from_user.first_name} jolasten hasi da.")
    
    bot.send_message(txat_id, testuak["eskuandago"][jokoan[txat_id]["hizkuntza"]], disable_notification=(True))
    kartakbidali(jokoan[txat_id]["nire_eskua"], txat_id)
    
    bot.send_message(txat_id, testuak["mahaiandago"][jokoan[txat_id]["hizkuntza"]], disable_notification=(True))
    kartakbidali(jokoan[txat_id]["mahaia"], txat_id)
    
    hurrengojokaldia(jokoan[txat_id]["nire_eskua"], "eskua", txat_id)
    hurrengojokaldia(jokoan[txat_id]["mahaia"], "mahaia", txat_id)
     
      
def barajasortu():
    
    # Baraja ordenatu bat sortzen du
    
    baraja = []
    paloak = list("OCEB")
    for p in paloak:
        for i in range(10):
            baraja.append(str(i+1)+"-"+p)
    
    return baraja

def banatu(n,txata):
    
    # Barajatik n elementu ateratzen ditu ausaz
    global jokoan
        
    kartakatera = []
    
    for i in range(n):
        karta = jokoan[txata]["baraja"].pop(random.randrange(0,len(jokoan[txata]["baraja"])))
        kartakatera.append(karta)
        
    return kartakatera

def kartakbidali(kartak, txat):
    
    # Mahai gainean dauden kartak eta jokalariak eskuan dituenak irudi bidez bidaltzen ditu txatera
    if len(kartak) != 0:
        karta_irudiak = []
            
        for karta in kartak:
            karta_irudiak.append(f"/home/mikel/Documentos/Escoba/irudiak/{karta}.png")
        while len(karta_irudiak)<3:
            karta_irudiak.append("/home/mikel/Documentos/Escoba/irudiak/hutsik.png")
        
        tempImage = BytesIO()
        tempImage .name = 'kartak.png'
        mergedImages = elkartuKartak(karta_irudiak)
        mergedImages.save(tempImage,'png')
        tempImage.seek(0)
        bot.send_photo(txat, photo=tempImage)
    
def elkartuKartak(kartak,colsmax=3):
    
    # zerrenda bezala pasatako irudiak batean elkartzen ditu eta irudi berria itzultzen du
    
    n = len(kartak)
    margina = 5  # bi karten arteko margina
    
    if n != 0:
        if n < colsmax:
            colsmax = n
        rows = n // colsmax
        lastrowcols = n % colsmax
        if lastrowcols != 0:
            rows += 1
        else:
            if n < colsmax:
                lastrowcols = n
            else:
                lastrowcols = colsmax
            
        images = [Image.open(file) for file in kartak]
        img_w, img_h = images[0].size
        mergedImages = Image.new('RGBA',(colsmax*(img_w+margina)+margina, rows*(img_h+margina)+margina), (16, 60, 46, 255))
        bg_w, bg_h = mergedImages.size
        
        for i in range(rows):
            for j in range(colsmax):
                if i*colsmax+j < n:
                    offset = (j*(img_w+margina)+margina, i*(img_h+margina)+margina)
                    mergedImages.paste(images[i*colsmax+j], offset)
        
        return mergedImages
    
    

def hurrengojokaldia(kartak, nork, txat, colsmax = 3):
    
    # Mahaiko edo eskuko karten araberako botoiak sortzen ditu jokalariak zer bota aukera dezan
    
    global jokoan
    global testuak
    
    markup = types.InlineKeyboardMarkup()
    
    
    if len(kartak) != 0:
        n = len(kartak)
           
        if n < colsmax:
            colsmax = n
        rows = n // colsmax
        lastrowcols = n % colsmax
        if lastrowcols != 0:
            rows += 1
        else:
            if n < colsmax:
                lastrowcols = n
            else:
                lastrowcols = colsmax
            
    if nork == "mahaia":
        if len(kartak) != 0:
            for i in range(rows):
                
                if i < rows-1:
                    
                    markup.add(types.InlineKeyboardButton(text=kartak[0+3*i],callback_data=(f"{kartak[0+3*i]},{nork}")),
                               types.InlineKeyboardButton(text=kartak[1+3*i],callback_data=(f"{kartak[1+3*i]},{nork}")),
                               types.InlineKeyboardButton(text=kartak[2+3*i],callback_data=(f"{kartak[2+3*i]},{nork}")))
                elif lastrowcols == 3:
                    
                    markup.add(types.InlineKeyboardButton(text=kartak[0+3*i],callback_data=(f"{kartak[0+3*i]},{nork}")),
                               types.InlineKeyboardButton(text=kartak[1+3*i],callback_data=(f"{kartak[1+3*i]},{nork}")),
                               types.InlineKeyboardButton(text=kartak[2+3*i],callback_data=(f"{kartak[2+3*i]},{nork}")))
                elif lastrowcols == 2:
                    
                    markup.add(types.InlineKeyboardButton(text=kartak[0+3*i],callback_data=(f"{kartak[0+3*i]},{nork}")),
                               types.InlineKeyboardButton(text=kartak[1+3*i],callback_data=(f"{kartak[1+3*i]},{nork}")))
                else:
                    
                    markup.add(types.InlineKeyboardButton(text=kartak[0+3*i],callback_data=(f"{kartak[0+3*i]},{nork}")))
                
            markup.add(types.InlineKeyboardButton(text=testuak["jokatu"][jokoan[txat]["hizkuntza"]],callback_data=(f"amaitu,{nork}")))
            galdera = testuak["zermahaitik"][jokoan[txat]["hizkuntza"]]
        else:
            markup.add(types.InlineKeyboardButton(text=testuak["jokatu"][jokoan[txat]["hizkuntza"]],callback_data=(f"amaitu,{nork}")))
            galdera = testuak["mahaiagarbi"][jokoan[txat]["hizkuntza"]]
    else:
        if len(kartak) == 3:
            markup.add(types.InlineKeyboardButton(text=kartak[0],callback_data=(f"{kartak[0]},{nork}")),
                       types.InlineKeyboardButton(text=kartak[1],callback_data=(f"{kartak[1]},{nork}")),
                       types.InlineKeyboardButton(text=kartak[2],callback_data=(f"{kartak[2]},{nork}")))
        elif len(kartak) == 2:
            markup.add(types.InlineKeyboardButton(text=kartak[0],callback_data=(f"{kartak[0]},{nork}")),
                       types.InlineKeyboardButton(text=kartak[1],callback_data=(f"{kartak[1]},{nork}")))
        else:
            markup.add(types.InlineKeyboardButton(text=kartak[0],callback_data=(f"{kartak[0]},{nork}")))
        galdera = testuak["zeinkarta"][jokoan[txat]["hizkuntza"]]
    
    bot.send_message(txat, text = galdera, reply_markup = markup, parse_mode='HTML', disable_notification=(True))
   

def jokaldia_kalk(saioa,nork,txata,deia):
    
    # Jokaldiak 15 punto batzen duen aztertzen du
    
    global jokoan
    global testuak
    
    kartabatura = 0
    txat_id = txata
    
    if saioa == "Ez daukazu aukerarik":
        pass
    else:
        for i in saioa:
            
            balionum = int(i.split("-")[0])
            kartabatura += balionum
            
        if kartabatura == 15 and nork == "bot":
            
            jokoan[txat_id]["azkena"] = False
            for karta in saioa:
                jokoan[txat_id]["botak_irabazi"].append(karta)
            if len(jokoan[txat_id]["mahaia"]) == 0:
                bot.answer_callback_query(deia,show_alert=(True), text = testuak["botak eskoba"][jokoan[txat_id]["hizkuntza"]])
                jokoan[txat_id]["bot_puntuak"] += 1
            
        elif kartabatura == 15 and nork == "jokalaria":
            
            jokoan[txat_id]["azkena"] = True
            for karta in saioa:
                jokoan[txat_id]["eskuak_irabazi"].append(karta)
            if len(jokoan[txat_id]["mahaia"]) == 0:
                bot.answer_callback_query(deia,show_alert=(True), text = testuak["zure eskoba"][jokoan[txat_id]["hizkuntza"]])
                jokoan[txat_id]["jok_puntuak"] += 1
                
        else:
            jokoan[txat_id]["mahaia"].extend(saioa)
            
        
def jokaldi_balioa(kartak, sobran):
    
    balioa = 0.0
    if "7-O" in kartak:
        balioa += 1
    if len(kartak) == len(sobran)+1:
        balioa += 1
    for i in kartak:
        if i.split("-")[0] == "7" and i.split("-")[1] != "O":
            balioa += 0.35
        if i.split("-")[1] == "O":
            balioa += 0.2
        balioa += 0.05
    return round(balioa, 2)

def aukerak_aztertu(ditut,daude):
    aukerak = []        
    for i in ditut:
        zenbakia_i = int(i.split("-")[0])
        for j in daude:
            zenbakia_j = int(j.split("-")[0])
            if zenbakia_i + zenbakia_j == 15:
                jok_hau = []
                jok_hau.append(i)
                jok_hau.append(j)
                aukerak.append([jok_hau, jokaldi_balioa(jok_hau,daude)])
                
            for k in daude[daude.index(j)+1:]:
                zenbakia_k = int(k.split("-")[0])
                if zenbakia_i + zenbakia_j + zenbakia_k == 15:
                    jok_hau = []
                    jok_hau.append(i)
                    jok_hau.append(j)
                    jok_hau.append(k)
                    aukerak.append([jok_hau, jokaldi_balioa(jok_hau,daude)])
                    
                for m in daude[daude.index(k)+1:]:
                    zenbakia_m = int(m.split("-")[0])
                    if zenbakia_i + zenbakia_j + zenbakia_k + zenbakia_m == 15:
                        jok_hau = []
                        jok_hau.append(i)
                        jok_hau.append(j)
                        jok_hau.append(k)
                        jok_hau.append(m)
                        aukerak.append([jok_hau, jokaldi_balioa(jok_hau,daude)])
                        
    aukerak.sort(key = lambda x: x[1])
    aukerak.reverse()
    if len(aukerak)==0:
        return "Ez daukazu aukerarik"
    else:
        return aukerak[0][0]
    
def irabazlea(jok_kartak, bot_kartak, txat_id):
    
    global jokoan
    global testuak
    
    jok_eskobak = jokoan[txat_id]["jok_puntuak"]
    jok_urreak = []
    jok_zazpiak = []
    jok_7O = testuak["jok_urrezko7ez"][jokoan[txat_id]["hizkuntza"]]
    
    bot_eskobak = jokoan[txat_id]["bot_puntuak"]
    bot_urreak = []
    bot_zazpiak = []
    bot_7O = testuak["bot_urrezko7ez"][jokoan[txat_id]["hizkuntza"]]
    
    for karta in jok_kartak:
        if karta.split("-")[1] == "O":
            jok_urreak.append(karta)
        if karta.split("-")[0] == "7":
            jok_zazpiak.append(karta)
        if karta == "7-O":
            jok_7O = testuak["jok_urrezko7bai"][jokoan[txat_id]["hizkuntza"]]
    
    if len(jok_kartak) > 20:
        jokoan[txat_id]["jok_puntuak"] += 1
    if len(jok_zazpiak) > 2:
        jokoan[txat_id]["jok_puntuak"] += 1
    if len(jok_urreak) > 5:
        jokoan[txat_id]["jok_puntuak"] += 1
    if jok_7O:
        jokoan[txat_id]["jok_puntuak"] += 1
        
    
    jok_testua = testuak["jok emaitza"][jokoan[txat_id]["hizkuntza"]].format(jokoan[txat_id]["jok_puntuak"],
                                                                  len(jok_kartak),
                                                                  len(jok_urreak),jok_urreak,
                                                                  len(jok_zazpiak),
                                                                  jok_7O,
                                                                  jok_eskobak)
    
    
    bot.send_message(txat_id, jok_testua, disable_notification=(True))
    
    for karta in bot_kartak:
        if karta.split("-")[1] == "O":
            bot_urreak.append(karta)
        if karta.split("-")[0] == "7":
            bot_zazpiak.append(karta)
        if karta == "7-O":
            bot_7O = testuak["bot_urrezko7bai"][jokoan[txat_id]["hizkuntza"]]
    
    if len(bot_kartak) > 20:
        jokoan[txat_id]["bot_puntuak"] += 1
    if len(bot_zazpiak) > 2:
        jokoan[txat_id]["bot_puntuak"] += 1
    if len(bot_urreak) > 5:
        jokoan[txat_id]["bot_puntuak"] += 1
    if bot_7O:
        jokoan[txat_id]["bot_puntuak"] += 1
        
    
    bot_testua = testuak["bot emaitza"][jokoan[txat_id]["hizkuntza"]].format(jokoan[txat_id]["bot_puntuak"],
                                                                  len(bot_kartak),
                                                                  len(bot_urreak),bot_urreak,
                                                                  len(bot_zazpiak),
                                                                  bot_7O,
                                                                  bot_eskobak)
    
    bot.send_message(txat_id, bot_testua, disable_notification=(True))
    
    if jokoan[txat_id]["jok_puntuak"] > jokoan[txat_id]["bot_puntuak"]:
        bot.send_message(txat_id, testuak["irabazi"][jokoan[txat_id]["hizkuntza"]], disable_notification=(True))
    elif jokoan[txat_id]["jok_puntuak"] < jokoan[txat_id]["bot_puntuak"]:
        bot.send_message(txat_id, testuak["galdu"][jokoan[txat_id]["hizkuntza"]], disable_notification=(True))
    else:
        bot.send_message(txat_id, testuak["berdindu"][jokoan[txat_id]["hizkuntza"]], disable_notification=(True))
            
    

@bot.callback_query_handler(func=lambda call: True)

def erantzunajaso(call):
        
    global jokoan
    global testuak
    
    botoi_edukia = call.data.split(",")[0]
    txat_id = call.message.chat.id
        
    if botoi_edukia == "amaitu":
        
        jokaldia_kalk(jokoan[txat_id]["jokaldia"],"jokalaria",txat_id,call.id)
        
        time.sleep(0.3)
        
        if len(jokoan[txat_id]["nire_eskua"]) != 0:
            
            bot.send_message(txat_id, testuak["mahaiandago"][jokoan[txat_id]["hizkuntza"]], disable_notification=(True))
            kartakbidali(jokoan[txat_id]["mahaia"], txat_id)
            
        jokoan[txat_id]["jokaldia"].clear()
        
        time.sleep(0.3)
        
        
        if aukerak_aztertu(jokoan[txat_id]["bot_eskua"],jokoan[txat_id]["mahaia"]) == "Ez daukazu aukerarik":
            deskartea=[]
            deskartea.append(jokoan[txat_id]["bot_eskua"].pop(random.randint(0, len(jokoan[txat_id]["bot_eskua"])-1)))
            jokaldia_kalk(deskartea,"bot",txat_id,call.id)
            bot.send_message(txat_id, testuak["botakjaurti"][jokoan[txat_id]["hizkuntza"]], disable_notification=(True))
            kartakbidali(jokoan[txat_id]["mahaia"], txat_id)
            if len(jokoan[txat_id]["nire_eskua"]) != 0:
                bot.send_message(txat_id, testuak["eskuandago"][jokoan[txat_id]["hizkuntza"]], disable_notification=(True))
                kartakbidali(jokoan[txat_id]["nire_eskua"], txat_id)
            
        else:
            bot_jokaldia = aukerak_aztertu(jokoan[txat_id]["bot_eskua"], jokoan[txat_id]["mahaia"])
            for k in bot_jokaldia:
                if k in jokoan[txat_id]["bot_eskua"]:
                    jokoan[txat_id]["bot_eskua"].remove(k)
                else:
                    jokoan[txat_id]["mahaia"].remove(k)
                    
            jokaldia_kalk(bot_jokaldia,"bot",txat_id,call.id)
             
            bot.send_message(txat_id, testuak["botjokaldia"][jokoan[txat_id]["hizkuntza"]].format(bot_jokaldia), disable_notification=(True))
            kartakbidali(jokoan[txat_id]["mahaia"], txat_id)
            
            
        if len(jokoan[txat_id]["bot_eskua"]) != 0:
            hurrengojokaldia(jokoan[txat_id]["nire_eskua"], "eskua", txat_id)
            hurrengojokaldia(jokoan[txat_id]["mahaia"], "mahaia", txat_id)
        elif len(jokoan[txat_id]["baraja"]) !=0 and len(jokoan[txat_id]["bot_eskua"])==0:
            jokoan[txat_id]["nire_eskua"] = banatu(3, txat_id)
            jokoan[txat_id]["bot_eskua"] = banatu(3, txat_id)
            bot.send_message(txat_id, testuak["banatu"][jokoan[txat_id]["hizkuntza"]])
            kartakbidali(jokoan[txat_id]["nire_eskua"], txat_id)
            hurrengojokaldia(jokoan[txat_id]["nire_eskua"], "eskua", txat_id)
            hurrengojokaldia(jokoan[txat_id]["mahaia"], "mahaia", txat_id)
        elif len(jokoan[txat_id]["baraja"]) == 0 and len(jokoan[txat_id]["bot_eskua"]) == 0:
            if jokoan[txat_id]["azkena"]:
                for karta in jokoan[txat_id]["mahaia"]:
                    jokoan[txat_id]["eskuak_irabazi"].append(karta)
            else:
                for karta in jokoan[txat_id]["mahaia"]:
                    jokoan[txat_id]["botak_irabazi"].append(karta)
            irabazlea(jokoan[txat_id]["eskuak_irabazi"], jokoan[txat_id]["botak_irabazi"], call.message.chat.id)
            
        
    else:
        jokoan[txat_id]["jokaldia"].append(botoi_edukia)
            
        if botoi_edukia in jokoan[txat_id]["nire_eskua"]:
            jokoan[txat_id]["nire_eskua"].remove(botoi_edukia)
            if len(jokoan[txat_id]["jokaldia"]) > 1:
                jokoan[txat_id]["nire_eskua"].append(jokoan[txat_id]["jokaldia"].pop(0))
        elif botoi_edukia in jokoan[txat_id]["mahaia"]:
            jokoan[txat_id]["mahaia"].remove(botoi_edukia)
    
        
bot.polling()
