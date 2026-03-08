#ici on demende le nom 
nom = ""
while nom == "":

    nom = input("Quel est votre nom ? ")
#ici on demende l'age

age_prochain = 0
while age_prochain == 0:
    age = input("Quel est votre age ? ")

    try:
        age_prochain = int(age) + 1
    except:
        print("ERREUR: vous devez entre un nombre pour l'age")
else:

#affiche les resultats

    print("Vous avez appelez " + nom + " ,Vous avez " + age +   "ans")
    print("je suis revi de vous connaitre " + nom )


    print("l'annee prochain vous aurez " + str(age_prochain) + "ans")
