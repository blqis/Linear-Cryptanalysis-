from random import *
import numpy as np

sbox = [9, 11, 12, 4, 10, 1, 2, 6, 13, 7, 3, 8, 15, 14, 0, 5]
xobs = [14, 5, 6, 10, 3, 15, 7, 9, 11, 0, 4, 1, 2, 8, 13, 12]

# sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
# xobs = [5, 14, 15, 8, 12, 1, 2, 13, 11, 4, 6, 3, 0, 7, 9, 10]



def enc (m, key):
    t = sbox[m ^ key[0]]
    c = sbox[t ^ key[1]]
    return c

def dec (c, key):
    t = xobs[c] ^ key[1]
    m = xobs[t] ^ key[0]
    return m

cle = (8, 12)


def generer_paires(cle, n):

    tab = []

    for i in range(n):
        tab.append([i, (enc(i, cle))])

    return sample(tab, k = len(tab))

# print(generate_pairs((5,0), 15))


def parite_bits(bits):

    res = 0
    mask = 1

    for i in range(4):
        res += bits & mask
        bits >> 1

    return res

def parite(X, Y):

    res = 0
    mask = 1
    for i in range(4):

        x = X & mask
        y = Y & mask
        res = res ^ x ^ y 
        X = X >> 1
        Y = Y >> 1

    return res

def compte_linearite():

    tab = [[0 for masko in range(16)] for maski in range(16)]

    for i in range(16):
        for j in range(16):
            for x in range(16):

                if ((parite((x & i), (sbox[x] & j))) == 0):
                    tab[i][j] += 1
    return tab

# print(np.matrix(compte_linearite()))


def meilleure_paire(tab): # retourne les meilleurs masques

    best = [0, 0]
    max = 0
    max_bits = 0

    for i in range(len(tab)):
        for j in range(len(tab[0])): 

            if (tab[i][j] < max):
                continue
            
            if (tab[i][j] > max):
                max_bits = 0

            if ((parite_bits(i) + parite_bits(j)) <= max_bits): # masque a un sur tous les bits, si le + de 1 dans les bits
                continue 

            max = tab[i][j] # nouveau max de la val à cet index
            best[0] = i # index de la meilleure valeur
            best[1] = j
            max_bits = (parite_bits(i) + parite_bits(j))
    
    return best

# print(meilleure_paire(compte_linearite()))


def candidats(paires, mask):

    candi = [0 for masko in range(16)] # tous les candidats possibles et leur score
    abscandi = [] # meilleurs candidats avec absolu appliqué dessus

    for k in range(16): # parcours tout les k clés possibles

        for msg in paires: # pour tous les couples clair / chiffré générés aléatoirement

            t = sbox[msg[0] ^ k] # première transormation

            if (parite((t & mask[0]), (msg[1] & mask[1]) ) == 0): # si le bit de parité entre t & mask0 ET le chiffré avec mask1
                candi[k] += 1

        if ((abs(candi[k] - 8)) >= 4):
            abscandi.append(k)

    return abscandi



# print(candidats(generer_paires(cle, 16), meilleure_paire(compte_linearite())))


def attack(k0_candidats, paires):

    # y = 0 / vérification du nombre d'itérations
    # x = 0

    for k0 in k0_candidats:

        T = True
        i = 0

        t1 = sbox[paires[i][0] ^ k0]
        t2 = xobs[paires[i][1]]
        k1 = t1 ^ t2
        cle = (k0, k1)

        for msg in paires:
            # x+=1

            if (dec(msg[1], cle) != msg[0]):
                # y+=1

                T = False
                break

        i+=1

        # print(x, y)

        if (T == True):
            return (k0, k1)

    return None

print("La clé est :", cle)
paires = generer_paires(cle, 16)
print("La clé retrouvée est :", attack(candidats(paires, meilleure_paire(compte_linearite())), paires))

