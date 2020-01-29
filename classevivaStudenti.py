
            #                                               REGISTRO ELETTRONICO CLASSEVIVA-STUDENTI                                              #

from getpass import getpass
from bs4 import BeautifulSoup as bs
import requests as req

class Materia:
    nome: str
    voti = []
    media: int

    def __init__(self, nome, voti, media):
        self.nome = nome
        self.voti = voti
        self.media = media
#FINE CLASSE

def formatta(voto):
    nuova = ""
    if voto == "o":#ottimo = 10
        voto = "10"
    elif voto == "ds":#distinto = 8
        voto = "8"
    elif voto == "b":#buono = 7
        voto = "7"
    elif voto == "s":#sufficiente = 6
        voto = "6"
    elif voto == "i":#insufficiente = 5
        voto = "5"

    for lettera in voto:
        if lettera == '½':#trasforma il mezzo in .5
            nuova += ".5"
        elif lettera == '+':#trasforma i + in .25
            nuova += ".25"
        elif lettera == '-':#trasforma i - nel voto -0.25
            nuova = str(float(nuova) - 0.25)
        elif lettera != 'Â':#se non è il carattere che si trova nei voti e mezzo aggiunge la lettera
            nuova += lettera

    return nuova
#FINE FUNZIONE

def media(voti):#fa la media dei voti di una data materia
    finale = 0.0
    for voto in voti:
        finale += float(voto)

    finale /= len(voti)
    return finale
#FINE FUNZIONE

def login(email, password):#invia la request per il login a classeviva
    global r
    data = {'cid':'',
    'uid': email,
    'pwd': password,
    'pin':'',
    'target':'' }

    s = req.Session()
    r = s.post("https://web.spaggiari.eu/auth-p7/app/default/AuthApi4.php?a=aLoginPwd", data=data)
    r = s.post("https://web.spaggiari.eu/cvv/app/default/genitori_voti.php")
#FINE FUNZIONE

quadrimestre_uno = []
quadrimestre_due = []

#chiede le informazioni per il login
email = input("Email/Username: ")
password = getpass()
print("\n####################################################################################################")

login(email, password)

pagina = bs(r.text, "html.parser")

mat = pagina.find_all("tr", {"class":"riga_materia_componente"})#trova le materie

if r.url == "https://web.spaggiari.eu/cvv/app/default/genitori_voti.php":
    for i in range(0, len(mat)):
        votoFinale = []
        quadrimestre = mat[i].get("sessione")#trova il quadrimestre della materia
        nome = mat[i].findChild("div", {"class":"materia_desc"}).get_text().upper()#trova il nome della materia
        vot = mat[i].findChildren("p", {"class":"double s_reg_testo cella_trattino"})#trova i voti per ogni materia
        for voto in vot:
            votoFinale.append(formatta(voto.get_text()))

        mediaMateria = media(votoFinale)#trova la media per ogni materia

        questa_materia = Materia(nome, votoFinale, mediaMateria)
        if quadrimestre == "S1":
            quadrimestre_uno.append(questa_materia)#aggiunge alla lista delle materie del primo quadrimestre ogni materia
        else:
            quadrimestre_due.append(questa_materia)#aggiunge alla lista delle materie del secondo quadrimestre ogni materia

    #OUTPUT voti primo quadrimestre e calcolo media generale del quadrimestre
    print("\nPRIMO QUADRIMESTRE\n")
    mediaGenerale = 0
    for materia in quadrimestre_uno:
        print(materia.nome, end = ": ")
        for voto in materia.voti:
            print(voto, end = " ")
        mediaGenerale += materia.media
        print("\tMEDIA: " + str(materia.media))

    mediaGenerale /= len(quadrimestre_uno)
    print("\nMEDIA GENERALE: " + str(mediaGenerale) + "\n")

    print("\n####################################################################################################")

    #OUTPUT voti secondo quadrimestre e calcolo media generale del quadrimestre
    print("\nSECONDO QUADRIMESTRE\n")
    mediaGenerale = 0
    for materia in quadrimestre_due:
        print(materia.nome, end = ": ")
        for voto in materia.voti:
            print(voto, end = " ")
        mediaGenerale += materia.media
        print("\tMEDIA: " + str(materia.media))

    mediaGenerale /= len(quadrimestre_due)
    print("\nMEDIA GENERALE: " + str(mediaGenerale) + "\n")
else:
    print("\nValori login errati\n")

print("####################################################################################################\n")
input("PREMERE IL TASTO INVIO PER USCIRE")
