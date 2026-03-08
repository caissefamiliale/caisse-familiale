from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")

ADMIN = "MFAUME SADIKI JACQUES"


def get_db():
    return sqlite3.connect("database.db")


# création tables
conn = get_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS membres(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nom TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS paiements(
id INTEGER PRIMARY KEY AUTOINCREMENT,
membre_id INTEGER,
mois TEXT,
annee INTEGER,
type TEXT,
montant INTEGER
)
""")

conn.commit()
conn.close()


# PAGE PRINCIPALE
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    conn = get_db()
    cursor = conn.cursor()

    mois_actuel = datetime.now().strftime("%B")
    annee_actuelle = datetime.now().year

    cursor.execute("SELECT * FROM membres")
    membres = cursor.fetchall()

    cursor.execute("""
    SELECT paiements.id, membres.nom, mois, annee, type, montant
    FROM paiements
    JOIN membres ON paiements.membre_id = membres.id
    """)
    paiements = cursor.fetchall()

    total = 0
    for p in paiements:
        if p[4] == "Depot":
            total += p[5]
        else:
            total -= p[5]

    cursor.execute("""
    SELECT membres.nom, SUM(paiements.montant)
    FROM paiements
    JOIN membres ON paiements.membre_id = membres.id
    GROUP BY membres.nom
    """)

    totaux_membres = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "membres": membres,
        "paiements": paiements,
        "total": total,
        "admin": ADMIN,
        "totaux_membres": totaux_membres
    })


# AJOUT MEMBRE
@app.post("/ajouter_membre")
def ajouter_membre(nom: str = Form(...)):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO membres(nom) VALUES(?)", (nom,))

    conn.commit()
    conn.close()

    return RedirectResponse("/membres", status_code=303)


# PAGE MEMBRES
@app.get("/membres", response_class=HTMLResponse)
def membres_page(request: Request):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM membres")
    membres = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse("membres.html", {
        "request": request,
        "membres": membres
    })


# SUPPRIMER MEMBRE
@app.get("/supprimer_membre/{id}")
def supprimer_membre(id: int):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM membres WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return RedirectResponse("/membres", status_code=303)


# MODIFIER MEMBRE
@app.post("/modifier_membre")
def modifier_membre(id: int = Form(...), nom: str = Form(...)):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE membres SET nom=? WHERE id=?", (nom, id))

    conn.commit()
    conn.close()

    return RedirectResponse("/membres", status_code=303)


# AJOUT PAIEMENT
@app.post("/ajouter_paiement")
def ajouter_paiement(
    membre_id: int = Form(...),
    mois: str = Form(...),
    annee: int = Form(...),
    type: str = Form(...),
    montant: int = Form(...)
):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT nom FROM membres WHERE id=?", (membre_id,))
    nom = cursor.fetchone()[0]

    if type == "Retrait" and nom != ADMIN:
        conn.close()
        return {"message": "Seul l'administrateur peut retirer"}

    cursor.execute("""
    INSERT INTO paiements(membre_id,mois,annee,type,montant)
    VALUES(?,?,?,?,?)
    """, (membre_id, mois, annee, type, montant))

    conn.commit()
    conn.close()

    return RedirectResponse("/", status_code=303)


# SUPPRIMER PAIEMENT
@app.get("/supprimer_paiement/{id}")
def supprimer_paiement(id: int):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM paiements WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return RedirectResponse("/", status_code=303)