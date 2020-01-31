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

def loggato():
    if r.url == "https://web.spaggiari.eu/cvv/app/default/genitori_voti.php":
        return True
    else:
        return False
#FINE FUNZIONE
