import os

def faire_liste_codons(sequence):
    """ Fonction qui sépare une séquence d'ADN en liste de codon.
    
    Args:
        sequence (str): Une séquence d'ADN
        
    Returns:
       list: Ensemble des codons contenus dans la séquence
       
    """
    return [sequence[nuc : nuc + 3] for nuc in range(0, len(sequence), 3) 
            if len(sequence[nuc : nuc + 3]) == 3]

def produire_brin_comp(sequence):
    """ Fonction pour construire le brin complémentaire d'une séquence donnée.
    
    Args:
        sequence (str): une séquence d'ADN
        
    Returns:
        str: la séquence complémentaire et inversée de notre séquence originale
        
    """
    COMPLEMENTS = {"A":"T", "T":"A", "C":"G", "G":"C"}
    return "".join([COMPLEMENTS[base] for base in sequence[::-1]])
    
def segmentation_cadres_lectures(sequence):
    """ Fonction pour modéliser les 6 cadres de lecture d'une séquence d'ADN.
    
    Args:
        sequence (str): une séquence d'ADN
        
    Returns:
        dict_seqs (dict): un dictionnaire renfermant les 6 cadres de lecture 
        
    """
    dict_seqs = {(i+1) : faire_liste_codons(sequence[(i):]) for i in range(3)}
    sequence_comp = produire_brin_comp(sequence)
    dict_seqs_comp = {-(i+1) : faire_liste_codons(sequence_comp[i:]) for i in range(3)}

    dict_seqs.update(dict_seqs_comp)    
    return dict_seqs

def trouver_start(dict_seqs):
    """ Fonction pour trouver l'emplacement du(des) codon(s) "ATG" d'une séquence d'ADN.
    
    Args:
        dict_seqs (dict): six cadres de lecture d'une séquence d'ADN
        
    Returns:
        key_pos (list): clé(s) du dictionnaire comportant un codon "ATG"
        pos_codon (list): position(s) du codon "ATG"
        
    """
    CODON_START = "ATG"
    pos_codon, key_pos = [],[]
    
    for id_seq, codons in dict_seqs.items():
        try:
            pos_codon.append(codons.index(CODON_START))
            key_pos.append(id_seq)
        except: ValueError
        
    return key_pos, pos_codon

def trouver_end(seq):
    """ Fonction pour trouver le codon STOP le plus éloigné d'une séquence.
    
    Args:
        seq (list): une liste de codon d'une séquence donnée
        
    Returns:
        maximum (int): l'index du codon STOP le plus élevé
        
    """
    CODONS_END = ["TAA", "TAG", "TGA"]
    pos_end = []
    
    for end_codon in CODONS_END:
        for codon in range((len(seq) - 1), 0, -1):
            if end_codon == seq[codon]:
                pos_end.append(codon)
                break
    try:
        maximum = max(pos_end)
    except ValueError:
        maximum = 0 
    return maximum

def trouver_max_longueur(seqs, codons_starts, dic_seqs):
    """ Fonction pour trouver la plus longue séquence de codons.
    
    Args:
        seqs (list): Clé(s) du dictionnaire dans la valeur contient un codon START
        codons_starts (list): Positions des codons START
        dic_seqs (dict): Six cadres de lecture d'une séquence d'ADN
        
    Returns:
        bonne_seq (int): Clé de la plus longue séquence de codons
        bon_end (int): position du codon END correspondant
        bon_start (int): position du codon START
        
    """
    codon_end = [trouver_end(dic_seqs[seq]) for seq in seqs]
    diffs = [codon_end[i] - codons_starts[i] for i in range(len(codons_starts))]
    pos = diffs.index(max(diffs))
    
    seq, start, end = seqs[pos], codons_starts[pos], codon_end[pos]
    return seq, end, start
    
def presentation(cod_beg, cod_end, seq, fichier):
    """
    Fonction pour formatter la présentation.
    
    Args:
        cod_beg (int): position du codon START
        cod_end (int): position du codon END
        seq (list): Codons
        fichier (str): nom du fichier contenant la séquence analysée
    """
    sequence = "".join([seq[codon] for codon in range(cod_beg, cod_end)])
    
    present = f"\nNom du fichier: {fichier}\nSequence: {sequence}"\
                f"\nLonguer de l'ORF: {len(sequence)}"\
                f"\nValeur du codon STOP: {seq[cod_end]}"
    print(present)
        
def detection_orf(fichier, nom_fichier):
    """ Fonction pour déterminer la présence d'un ORF au sein d'une séquence d'ADN.
    
    Args:
        fichier (str): directory du fichier contenant la séquence d'ADN
        nom_fichier (str): Nom du fichier
    """
    with open(fichier, "r") as doc:
        seq = doc.readline().strip("\n")
        dict_sequences = segmentation_cadres_lectures(seq)
        
        keys_seq, starts = trouver_start(dict_sequences)
        if keys_seq:
            usable_seq, codon_end, codon_start = trouver_max_longueur(keys_seq, starts, dict_sequences)
            presentation(codon_start, codon_end, dict_sequences[usable_seq], nom_fichier)
        else:
            print(f"\nLa séquence du fichier '{nom_fichier}' ne contient pas d'ORF!")
        
if __name__ == "__main__":    
    dir_this_file = os.path.dirname(__file__)
    
    for i in range(4):
        file_name = f"orf_sequence_{i+1}.txt"
        dir_seq_file = os.path.join(dir_this_file, file_name)
        detection_orf(dir_seq_file, file_name)
    else:   
        name_bonus = "orf_sequence_BONUS.txt"
        bonus_file = os.path.join(dir_this_file, name_bonus)
        detection_orf(bonus_file, name_bonus)