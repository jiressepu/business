import json

# Nom du fichier JSON pour stocker les données
fichier_json = "montants.json"

# Charger les données existantes si le fichier existe
try:
    with open(fichier_json, "r") as file:
        data = json.load(file)
        montants = data.get("montants", [])  # Récupérer la liste des montants
        total = data.get("total", 0)  # Récupérer le total
except (FileNotFoundError, json.JSONDecodeError):
    montants = []  # Liste vide si le fichier n'existe pas
    total = 0  # Total initial

while True:
    montant = input("Entrer un montant (ou 'q' pour quitter) : ")
    
    if montant.lower() == 'q':  # Quitter si l'utilisateur entre 'q'
        break

    try:
        montant = float(montant)  # Convertir l'entrée en nombre
        montants.append(montant)  # Ajouter le montant à la liste
        total += montant  # Mettre à jour le total
        
        # Sauvegarder les données dans le fichier JSON (avec le total affiché)
        data = {"montants": montants, "total": total, "total_affiché": f"{total}$"}
        with open(fichier_json, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Total actuel : {total}$")
    except ValueError:
        print("Veuillez entrer un nombre valide.")

print(f"Montant total additionné : {total}$")

