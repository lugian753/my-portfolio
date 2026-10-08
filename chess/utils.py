import os
#pulisce il terminale dagli output precedenti
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

#gestione errore input non valido sugli interi, il parametro viene stampato
def int_input(cout):
    while True:
        try:
            #prova la conversione, se non ci sono errori ritorno il valore intero
            inp = input(cout) #stampa di cout, contenente stringa per l'input
            return int(inp)
        except ValueError:
            #stampo errore, si resta dento al while True e viene chiesto nuovamente l'intero
            print("***Errore, richiesto intero.")
