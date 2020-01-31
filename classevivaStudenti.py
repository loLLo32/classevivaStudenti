
            #                                               REGISTRO ELETTRONICO CLASSEVIVA-STUDENTI                                              #

from getpass import getpass
from flask import Flask, request, render_template
from bs4 import BeautifulSoup as bs
from colorama import Fore
from colorama import Style
import colorama
import clsF as cf

colorama.init()

quadrimestre_uno = []
quadrimestre_due = []

#chiede le informazioni per il login
email = input("Email/Username: ")
password = getpass()
print(f"{Fore.BLUE}\n####################################################################################################{Style.RESET_ALL}")

cf.login(email, password)

pagina = bs(cf.r.text, "html.parser")

mat = pagina.find_all("tr", {"class":"riga_materia_componente"})#trova le materie

if cf.loggato():
    for i in range(0, len(mat)):
        votoFinale = []
        quadrimestre = mat[i].get("sessione")#trova il quadrimestre della materia
        nome = mat[i].findChild("div", {"class":"materia_desc"}).get_text().upper()#trova il nome della materia
        vot = mat[i].findChildren("p", {"class":"double s_reg_testo cella_trattino"})#trova i voti per ogni materia
        for voto in vot:
            votoFinale.append(cf.formatta(voto.get_text()))

        mediaMateria = cf.media(votoFinale)#trova la media per ogni materia

        questa_materia = cf.Materia(nome, votoFinale, mediaMateria)
        if quadrimestre == "S1":
            quadrimestre_uno.append(questa_materia)#aggiunge alla lista delle materie del primo quadrimestre ogni materia
        else:
            quadrimestre_due.append(questa_materia)#aggiunge alla lista delle materie del secondo quadrimestre ogni materia

    #OUTPUT voti primo quadrimestre e calcolo media generale del quadrimestre
    print(f"{Fore.RED}\nPRIMO QUADRIMESTRE\n{Style.RESET_ALL}")
    mediaGenerale = 0
    for materia in quadrimestre_uno:
        print(f"{Fore.GREEN}" + materia.nome + f"{Style.RESET_ALL}", end = ": ")
        for voto in materia.voti:
            print(voto, end = " ")
        mediaGenerale += materia.media
        print(f"{Fore.YELLOW}\tMEDIA: " + str(materia.media) + f"{Style.RESET_ALL}")

    mediaGenerale /= len(quadrimestre_uno)
    print(f"{Fore.YELLOW}\nMEDIA GENERALE: " + str(mediaGenerale) + f"{Style.RESET_ALL}\n")

    print(f"{Fore.BLUE}\n####################################################################################################{Style.RESET_ALL}")

    #OUTPUT voti secondo quadrimestre e calcolo media generale del quadrimestre
    print(f"{Fore.RED}\nSECONDO QUADRIMESTRE\n{Style.RESET_ALL}")
    mediaGenerale = 0
    for materia in quadrimestre_due:
        print(f"{Fore.GREEN}" + materia.nome + f"{Style.RESET_ALL}", end = ": ")
        for voto in materia.voti:
            print(voto, end = " ")
        mediaGenerale += materia.media
        print(f"{Fore.YELLOW}\tMEDIA: " + str(materia.media) + f"{Style.RESET_ALL}")

    mediaGenerale /= len(quadrimestre_due)
    print(f"{Fore.YELLOW}\nMEDIA GENERALE: " + str(mediaGenerale) + f"{Style.RESET_ALL}\n")
else:
    print("\nValori login errati\n")

print(f"{Fore.BLUE}####################################################################################################\n{Style.RESET_ALL}")
input("PREMERE IL TASTO INVIO PER USCIRE")
