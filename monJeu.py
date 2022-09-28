from random import randint

def give_clue(essai, plus_grand_que):
    """Fonction donnant un indice
    Args:
        essai (int): nombre d'essai restant
        plus_grand_que (bool): evaluation de l'énoncé 
            "ma supposition est plus grande que le nombre mystère"
    """
    ortographe = "essais" if essai > 2 else "essai"
    indice = "Plus grand!" if not plus_grand_que else "Plus petit!"
    print(indice + f" Il te reste {essai - 1} {ortographe}...\n")
        
def resultat_jeu(resultat, nbre_secret):
    """Fonction donnant l'énoncé de clôture du jeu
    Args:
        resultat (bool): evaluant si le joueur à deviné le nombre mystère
        nbre_secret (int): le nombre mystère
    """
    mes_win = "Bravo! Tu as gagné!!"
    mes_loss = f"Tu as perdu! Je pensais au nombre {nbre_secret}"
    good_message = mes_win if resultat else mes_loss
    print(good_message)
        
def jouer():
    """Fonction pour le déroulement du jeu
    """
    nombre_secret = randint(1,10)
    victoire = False
    ESSAIS = 5
    
    for essai in range(ESSAIS, 0, -1):
        while True:
            try:
                ma_supposition = int(input("Je pense à un chiffre de 1 à 10, devine lequel! Essai: "))
                assert (ma_supposition <= 10 and ma_supposition >= 1)
                break
            except ValueError: print("J'ai besoin d'un nombre entier...\n")
            except AssertionError: print("J'ai besoin d'un nombre entre 1 et 10...\n")
        
        if ma_supposition == nombre_secret:
            victoire = True
            break
        elif ma_supposition != nombre_secret and essai > 1:
            give_clue(essai, ma_supposition > nombre_secret)
            
    resultat_jeu(victoire, nombre_secret)
    
jouer()
