from datetime import datetime
import sqlite3


class Client:
    def __init__(self, id, nom, prenom, cin, age):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.cin = cin 
        self.age = age 

    def __str__(self):
        return "{}: {} {}".format(self.id, self.nom, self.prenom)



class Reservation:
    def __init__(self, id, dateSortie, dateEntree, prix, id_Client, id_Chambre):
        self.id = id
        self.dateSortie = dateSortie
        self.dateEntree = dateEntree 
        self.prix = prix  
        self.id_Client = id_Client
        self.id_Chambre = id_Chambre

    def __str__(self):
        return "Reservation {}".format(self.id)



class Chambre:
    def __init__(self, numero, types, etat, disponibilite, prixUnitaire):
        self.numero = numero
        self.types = types
        self.etat = etat
        self.disponibilite = disponibilite
        self.prixUnitaire = prixUnitaire

    
    def __str__(self):
        return "Chambre n°{}".format(self.numero)



class Room(Chambre):
    """
        J'aui heriter cette classe de la classe Chambre car J'ai deja creer 
            un objet comme celle ci las haut, donc Pour ne plus le faire, 
            Je fais juste une simple Heritage.
    """
    def __init__(self, numero, types, etat, disponibilite, prixUnitaire):
        Chambre.__init__(self, numero, types, etat, disponibilite, prixUnitaire)


    def insertToDb(self):
        # transfert d'informations
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ROOMS(numero, type, etat, disponibilite, prix)
            VALUES (?, ?, ?, ?, ?)
        """, (self.numero, self.types, self.etat, self.disponibilite, self.prixUnitaire)) 



class Customer(Client):
    """
        J'ai heriter cette classe de la classe CLient car J'ai deja creer 
            un objet comme celle ci las haut, donc Pour ne plus le faire, 
            Je fais juste une simple Heritage.
    """
    def __init__(self, id, nom, prenom, cin, age):
        Client.__init__(self, id, nom, prenom, cin, age)
    

    def insertToDb(self):
        # transfert d'informations
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO CUSTOMERS(nom, prenom, age, cin)
            VALUES (?, ?, ?, ?)
        """, (self.nom, self.prenom, self.age, self.cin))

        conn.commit()

    
    @classmethod # Pour pouvoir être appeler sans instance
    def print_Customer(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM CUSTOMERS
        """)

        print("LISTE DES CLIENTS")
        for val in cursor:
            print("""
                {} - {} {}
            """.format(val[0], val[1], val[2]))



class Booking(Reservation):
    """
        J'ai heriter cette classe de la classe Reservation car J'ai deja creer 
            un objet comme celle ci las haut, donc Pour ne plus le faire, 
            Je fais juste une simple Heritage.
    """
    def __init__(self, id, dateSortie, dateEntree, prix, id_Client, id_Chambre):
        Reservation.__init__(self, id, dateSortie, dateEntree, prix, id_Client, id_Chambre)
    

    def insertToDb(self):
        # transfert d'informations
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO BOOKINGS (dateEntree, dateSortie, id_Client, id_Chambre, prix)
            VALUES (?, ?, ?, ?, ?)
        """, (self.dateEntree, self.dateSortie, self.id_Client, self.id_Chambre, self.prix))

        conn.commit()

    @classmethod # Pour que la fonction peut être appeler sans instance 
    def modifier(self, id, dateEntree, dateSortie, id_Chambre):
        # Modification reservation fait par le client 
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE BOOKINGS 
            SET dateEntree = ?,
            SET dateSortie = ?,
            SET id_Chambre = ?
            WHERE id = ?
        """, (dateEntree, dateSortie, id_Chambre, id))

        conn.commit()

        print("Modifier avec success")
    
    @classmethod
    def supprimer(self, id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM BOOKINGS
            WHERE id = ?
        ''', (id,))

        conn.commit()

        print("Effacer avec succes")




def inserInfo():
   
    print("""
        SAISIE DES INFORMATIONS
    """)
    for i in range(5):
        print("\nPersonne n°",  i+1)
        nom = input("Entrer le nom: ")
        prenom = input("Entrer le prenom: ")
        cin = input("Entrer le CIN: ")
        age = int(input("Entrer l'age: "))

        dateEntree = input("Entrer la date d'entrée: (2019-11-30)\n")
        dateEntree = dateEntree.split("-")
        y, m, d = int(dateEntree[0]), int(dateEntree[1]), int(dateEntree[2])
        dateEntree = datetime(y, m, d)

        dateSortie = input("Entrer la date de sortie: (2019-11-30)\n")
        dateSortie = dateSortie.split("-")
        y, m, d = int(dateSortie[0]), int(dateSortie[1]), int(dateSortie[2])
        dateSortie = datetime(y, m, d)
        
        numero = int(input("Entrer le numero de chambre: "))
        types = input("Entrer le type de chambre: ")
        etat = input("Entrer l'etat de la chambre: ")
        prixUnitaire = float(input("Entrer le prix pour un jour: "))

        personne.append(
            Client(
                id=i+1,
                nom=nom,
                prenom=prenom,
                age=age,
                cin=cin
            )
        )

        chambre.append(
            Chambre(
                numero = numero,
                types = types,
                etat = etat,
                disponibilite = "Non disponible pour {} jours".format((dateSortie - dateEntree).days),
                prixUnitaire = prixUnitaire,
            )
        )

        reservation.append(
            Reservation(
                id = i+1,
                dateSortie = dateSortie,
                dateEntree = dateEntree,
                prix = (dateSortie - dateEntree).days * prixUnitaire,
                id_Client = personne[i].id,
                id_Chambre = numero
            )
        )


def triAndsave():
    for reserv in reservation:
        if (reserv.dateSortie - reserv.dateEntree).days == 3:
            file_customer = open("customer.txt", "a")
            file_bedroom = open("bedroom.txt", "a")
            file_booking = open("booking.txt", "a")

            for pers in personne:
                if pers.id == reserv.id_Client:

                    file_customer.write("""
                    Personne n°{}
                    Nom et Prenom: {} {}
                    Age: {}
                    CIN: {}
                    """.format(pers.id, pers.nom, pers.prenom, pers.age, pers.cin))

                    file_booking.write("""
                    Reservation n°{}
                    date entrée: {}
                    date sortie: {}
                    id client: {}
                    id chambre: {}
                    Prix totale: {} Ar
                    """.format(reserv.id, reserv.dateEntree, reserv.dateSortie, reserv.id_Client, reserv.id_Chambre, reserv.prix))

                    break
            
            for ch in chambre:
                if ch.numero == reserv.id_Chambre:
                    file_bedroom.write("""                        
                        Chambre n°{}
                        Type: {}
                        Etat: {}
                        disponibilite: {}
                        prix unitaire: {} Ar
                    """.format(ch.numero, ch.types, ch.etat, ch.disponibilite, ch.prixUnitaire))
                    break
            
            file_customer.close()
            file_bedroom.close()
            file_booking.close()
            
            customer = Customer(pers.id, pers.nom, pers.prenom, pers.cin, pers.age)
            customer.insertToDb()

            booking = Booking(reserv.id, reserv.dateEntree, reserv.dateSortie, reserv.id_Client, reserv.id_Chambre, reserv.prix)
            booking.insertToDb()

            room = Room(ch.numero, ch.types, ch.etat, ch.disponibilite, ch.prixUnitaire)
            room.insertToDb()

            
            

def createDb():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CUSTOMERS(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     nom TEXT,
     prenom TEXT,
     age INTERGER,
     cin TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ROOMS(
     numero INTEGER PRIMARY KEY,
     type TEXT,
     etat TEXT,
     disponibilite INTERGER,
     prix REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BOOKINGS(
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     dateSortie TEXT,
     dateEntree TEXT,
     id_Client INTERGER,
     id_Chambre INTEGER,
     prix REAL
    )
    """)

    conn.close()



def main():
    inserInfo()
    triAndsave()
    


if __name__ == '__main__':
    personne = []
    chambre = []
    reservation = []
    createDb()

    # main()

    choix = int(input("""

    Taper 1: Inserer Informations
    Taper 2: Afficher Clients
    Taper 3: Modifier Reservation
    Taper 4: Supprimer Reservation

    (Choix)>>>"""))

    if choix == 1:
        main()

    elif choix == 2:
        Customer.print_Customer()
    
    elif choix == 3:
        id = int(input("Entrer id: "))

        dateEn = input("Entrer la date d'entrée: (2019-11-30)\n")
        dateEn = dateEn.split("-")
        y, m, d = int(dateEn[0]), int(dateEn), int(dateEn)
        dateEn = datetime(y, m, d)

        dateSr = input("Entrer la date de sortie: (2019-11-30)\n")
        dateSr = dateSr.split("-")
        y, m, d = int(dateSr[0]), int(dateSr[1]), int(dateSr[2])
        dateSr = datetime(y, m, d)

        id_Chambre = int(input("Entrer le numero de chambre: "))
        
        Booking.modifier(id, dateEn, dateSr, id_Chambre)
    
    elif choix == 4:
        id = int(input("Entrer id: "))
        Booking.supprimer(id)
    
    