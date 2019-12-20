import random

player = []
score = []
tentative = 2

file = open("./expressions.txt", "r", encoding="utf-8")
reponse = ["16 19", "17", "Jonathan"]
data  = []
for line in file:
    data.append(line)

jr = int(input("Entrer le nombre de joueur: "))

while jr > 0:
    nom = input("Entrer votre nom: ")
    player.append(nom)
    tentative = 2
    val = random.randint(0, len(data)-1)

    print(data[val])

    while tentative > 0:
        rep = input("Votre reponse.. : ")
        
        if rep == reponse[val]:
            break

        print("Erreur, {} tentaives restantes".format(tentative))

        tentative -= 1

    if tentative > 0:
        print('trouver..')
    else:
        print("perdu")
    score.append(tentative)
    jr -= 1

gg = max(score)

gg_p = score.index(gg)

print("Le gagnant est", player[gg_p], "avec ", gg, "points")




