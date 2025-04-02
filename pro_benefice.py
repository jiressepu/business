import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

FILENAME = "data.json"

def charger_donnees():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # Retourne une liste vide si le fichier est corrompu
    return []

def sauvegarder_donnees(donnees):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(donnees, file, indent=4, ensure_ascii=False)

def calculer_total_general():
    return sum(entree.get("total", 0) for entree in donnees)

def mettre_a_jour_total_label():
    total_general = calculer_total_general()
    total_label.config(text=f"Total Général: {total_general:.2f}")

def ajouter_donnees():
    nom = simpledialog.askstring("Nom", "Entrez le nom de la personne :")
    if not nom:
        return
    
    try:
        montant = float(simpledialog.askstring("Montant", "Entrez un montant :"))
    except (ValueError, TypeError):
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
        return
    
    date_mise_a_jour = simpledialog.askstring("Date", "Entrez la date de mise à jour (JJ/MM/AAAA) :")
    pourcentage = montant * 0.5
    total = montant + pourcentage
    
    entree = {
        "nom": nom,
        "date": date_mise_a_jour,
        "montant": montant,
        "plus_50%": pourcentage,
        "total": total
    }
    
    donnees.append(entree)
    sauvegarder_donnees(donnees)
    afficher_donnees()

def modifier_donnees():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une entrée à modifier.")
        return
    index = selection[0]
    
    entree = donnees[index]
    nom = simpledialog.askstring("Modifier Nom", "Entrez le nouveau nom :", initialvalue=entree.get("nom", ""))
    try:
        montant = float(simpledialog.askstring("Modifier Montant", "Entrez un nouveau montant :", initialvalue=str(entree.get("montant", 0))))
    except (ValueError, TypeError):
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
        return
    date_mise_a_jour = simpledialog.askstring("Modifier Date", "Entrez une nouvelle date :", initialvalue=entree.get("date", ""))
    pourcentage = montant * 0.5
    total = montant + pourcentage
    
    donnees[index] = {
        "nom": nom,
        "date": date_mise_a_jour,
        "montant": montant,
        "plus_50%": pourcentage,
        "total": total
    }
    sauvegarder_donnees(donnees)
    afficher_donnees()

def supprimer_donnees():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une entrée à supprimer.")
        return
    index = selection[0]
    
    if messagebox.askyesno("Suppression", "Voulez-vous vraiment supprimer cette entrée ?"):
        donnees.pop(index)
        sauvegarder_donnees(donnees)
        afficher_donnees()

def afficher_donnees():
    listbox.delete(0, tk.END)
    for entree in donnees:
        if all(key in entree for key in ["nom", "montant", "total", "date"]):
            listbox.insert(tk.END, f"{entree['nom']} - {entree['montant']} + 50% = {entree['total']} ({entree['date']})")
        else:
            print("⚠️ Entrée invalide trouvée :", entree)  # Débogage
    mettre_a_jour_total_label()

# Chargement des données

donnees = charger_donnees()

# Interface graphique
root = tk.Tk()
root.title("Gestion des Montants")
root.geometry("500x450")

listbox = tk.Listbox(root, width=80, height=15)
listbox.pack(pady=10)

total_label = tk.Label(root, text=f"Total Général: {calculer_total_general():.2f}")
total_label.pack(pady=5)

afficher_donnees()

btn_ajouter = tk.Button(root, text="Ajouter", command=ajouter_donnees)
btn_modifier = tk.Button(root, text="Modifier", command=modifier_donnees)
btn_supprimer = tk.Button(root, text="Supprimer", command=supprimer_donnees)

btn_ajouter.pack(side=tk.LEFT, padx=10)
btn_modifier.pack(side=tk.LEFT, padx=10)
btn_supprimer.pack(side=tk.LEFT, padx=10)

root.mainloop()
