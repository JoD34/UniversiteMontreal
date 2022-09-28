import os
for i in range(1,5):
    dir_this = os.path.dirname(__file__)
    dir_seq = os.path.join(dir_this,f"orf_sequence_{i}.txt")

    f = open(dir_seq, "r")
    my_seq = f.readline()
    f.close()

    index_seq = my_seq.find("ATG")
    if index_seq != -1:
        list_codon = [my_seq[codon:codon+3] for codon in range(index_seq, len(my_seq), 3) 
                    if len(my_seq[codon:codon+3]) == 3]
        CODON_STOP = ["TAG", "TGA", "TAA"]

        list_stops = [] 

        for stop in CODON_STOP:
            for pos, codon in enumerate(reversed(list_codon)):
                if stop == codon:
                    list_stops.append(len(list_codon) - pos)

        seq_show = ""
        for codon in range(max(list_stops)-1):
            seq_show += list_codon[codon]
            
        print(f"séquence:{seq_show}\nLongeur de ma Séquence:{len(seq_show)}\nCodon Stop: {list_codon[max(list_stops)-1]}\n")
    else:
        print("Il n'y a pas d'ORF!\n")    