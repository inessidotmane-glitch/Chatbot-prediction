import csv
import random
import unicodedata
from typing import List, Tuple, Dict, Callable

# -----------------------------
# PARAMÈTRES GÉNÉRAUX
# -----------------------------
RANDOM_SEED = 7  # Fixer pour reproductibilité
TYPO_RATE = 0.03          # Petites fautes de frappe
LOWERCASE_RATE = 0.02     # Tout en minuscule parfois
NO_DIACRITIC_RATE = 0.01  # Sans accents
PREFIX_RATE = 0.25        # Ajout de formules polies
SUFFIX_RATE = 0.18        # Ajout de compléments ("merci d’avance", etc.)
ALT_PUNCT_RATE = 0.12     # Variations de ponctuation (?! … etc.)
ALT_FORM_RATE  = 0.35     # Reformulations interrogatives

N_SAMPLES = 10000  # Nombre total de lignes à générer
OUTPATH = "dataset_universite_fr.csv"

if RANDOM_SEED is not None:
    random.seed(RANDOM_SEED)

# -----------------------------
# LABELS (catégories)
# -----------------------------
LABELS = [
    "emploi_du_temps",
    "reglement",
    "service_campus",
    "formation",
    "procedure_administrative",
]

# -----------------------------
# VOCABULAIRES
# -----------------------------
COURS = [
    "algèbre avancée", "chimie organique", "économie", "programmation Python",
    "analyse de données", "microéconomie", "droit public", "statistiques appliquées",
    "biologie cellulaire", "robotique", "psychologie cognitive", "littérature moderne"
]
PROFS = ["Martin", "Nguyen", "Dubois", "Leroy", "Bennani", "Dupont", "Moreau", "Anderson"]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]
HEURES = ["8h30", "10h00", "14h00", "16h30"]
LIEUX = ["bibliothèque centrale", "service logement", "centre de santé", "bureau des carrières", "gymnase", "maison des étudiants"]
SEMESTRES = ["automne", "printemps", "été"]

PREFIXES = [
    "Bonjour,", "Bonsoir,", "Excusez-moi,", "S'il vous plaît,", "Petite question :", "Pardon,"
]
SUFFIXES = [
    "c’est urgent", "si possible", "merci d’avance", "pour aujourd’hui", "pour la semaine prochaine"
]

# -----------------------------
# FONCTIONS UTILITAIRES
# -----------------------------
def peut(prob: float) -> bool:
    return random.random() < prob

def sans_accents(texte: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')

def petite_faute(texte: str) -> str:
    if len(texte) < 6:
        return texte
    idx = random.randint(1, len(texte)-2)
    op = random.choice(["suppr", "double", "inverse"])
    if op == "suppr":
        return texte[:idx] + texte[idx+1:]
    elif op == "double":
        return texte[:idx] + texte[idx]*2 + texte[idx:]
    else:
        return texte[:idx-1] + texte[idx] + texte[idx-1] + texte[idx+1:]

def ponctuation_variee(texte: str) -> str:
    variantes = ["?", "?!", " ??", "… ?", " !?"]
    if texte.endswith("?"):
        return texte[:-1] + random.choice(variantes)
    return texte

def majuscule(texte: str) -> str:
    if not texte:
        return texte
    return texte[0].upper() + texte[1:]

# -----------------------------
# GÉNÉRATEURS PAR CATÉGORIE
# -----------------------------
def gen_emploi_du_temps():
    cours = random.choice(COURS)
    jour = random.choice(JOURS)
    heure = random.choice(HEURES)
    prof = random.choice(PROFS)
    semestre = random.choice(SEMESTRES)
    formes = [
        f"Quand a lieu le prochain cours de {cours} ?",
        f"Quel est l’horaire du cours de {cours} avec le professeur {prof} ?",
        f"Pouvez-vous me donner l’emploi du temps du semestre de {semestre} pour {cours} ?",
        f"Où et à quelle heure est mon cours du {jour} à {heure} ?",
        f"À quelle heure commencent les TD de {cours} ?",
        f"J’aimerais savoir quand se déroule le cours de {cours}.",
        f"Pourriez-vous m’indiquer le créneau de {cours} ?"
    ]
    return random.choice(formes)

def gen_reglement():
    sujet = random.choice(["plagiat", "retards", "rattrapage d’examen", "probation académique", "absence aux cours"])
    formes = [
        f"Quelle est la politique concernant le {sujet} ?",
        "Combien d’absences sont autorisées avant une sanction ?",
        "Quelles sont les règles pour le retrait d’un cours ?",
        "Existe-t-il un minimum de crédits ou de moyenne par semestre ?",
        "Où consulter le code de conduite des étudiants ?",
        "Y a-t-il un règlement spécifique pour les stages ?",
        "Que se passe-t-il en cas de triche à un examen ?"
    ]
    return random.choice(formes)

def gen_service_campus():
    lieu = random.choice(LIEUX)
    tech = random.choice(["Wi-Fi", "VPN", "ENT", "portail étudiant"])
    formes = [
        f"Où se trouve la {lieu} ?",
        f"Comment me connecter au {tech} de l’université ?",
        f"Quels sont les horaires d’ouverture de la {lieu} ?",
        "J’ai perdu mes clés, où se situe le bureau des objets trouvés ?",
        "Puis-je réserver une salle de travail ou un terrain de sport ?",
        f"Le {tech} ne fonctionne pas, que puis-je faire ?",
        f"Où puis-je imprimer mes documents sur le campus ?"
    ]
    return random.choice(formes)

def gen_formation():
    programme = random.choice(["Master Robotique", "Licence Histoire", "Parcours Data Science", "MBA Finance", "Master Psychologie"])
    domaine = random.choice(["Biologie", "Philosophie", "Informatique", "Psychologie", "Lettres modernes"])
    formes = [
        f"Quels sont les prérequis pour le {programme} ?",
        f"Combien de crédits faut-il pour se spécialiser en {domaine} ?",
        "Puis-je changer de majeure ou de spécialisation en cours d’année ?",
        f"Quelles sont les UE obligatoires pour le {programme} ?",
        "Comment réussir le prochain module de statistiques ?",
        f"Quelles sont les matières principales en {domaine} ?"
    ]
    return random.choice(formes)

def gen_procedure_administrative():
    action = random.choice([
        "payer mes frais de scolarité", "demander un relevé officiel",
        "mettre à jour mon adresse", "candidater pour la remise de diplôme",
        "obtenir une convention de stage", "renouveler ma carte étudiante"
    ])
    deadline = random.choice(["l’inscription aux cours", "la demande d’aide financière", "l’abandon d’une UE"])
    formes = [
        f"Comment {action} ?",
        f"Quelle est la date limite pour {deadline} ?",
        "Où soumettre la demande de carte étudiante ?",
        "Quels documents sont requis pour un changement de parcours ?",
        "Comment demander un report d’admission ?",
        f"Où déposer mon dossier pour {action} ?"
    ]
    return random.choice(formes)

# -----------------------------
# VARIATIONS DE SURFACE
# -----------------------------
def ajouter_prefixe(phrase: str) -> str:
    prefixe = random.choice(PREFIXES)
    if peut(0.5):
        phrase = phrase[0].lower() + phrase[1:]
    return f"{prefixe} {phrase}"

def ajouter_suffixe(phrase: str) -> str:
    suffixe = random.choice(SUFFIXES)
    if phrase.endswith("?"):
        return phrase[:-1] + f", {suffixe} ?"
    return f"{phrase} — {suffixe}"

def reformuler(phrase: str) -> str:
    variantes = [
        lambda s: f"Pourriez-vous me dire : {s}",
        lambda s: f"Est-il possible de savoir {s[0].lower() + s[1:]}",
        lambda s: f"J’aimerais savoir : {s}"
    ]
    t = random.choice(variantes)(phrase)
    return t if t.endswith("?") else t.rstrip(".") + " ?"

def appliquer_bruit(phrase: str) -> str:
    s = phrase
    if peut(ALT_PUNCT_RATE):
        s = ponctuation_variee(s)
    if peut(TYPO_RATE):
        s = petite_faute(s)
    if peut(NO_DIACRITIC_RATE):
        s = sans_accents(s)
    if peut(LOWERCASE_RATE):
        s = s.lower()
    return majuscule(s)

# -----------------------------
# GÉNÉRATION DU DATASET
# -----------------------------
GEN_FONCTIONS: Dict[str, Callable[[], str]] = {
    "emploi_du_temps": gen_emploi_du_temps,
    "reglement": gen_reglement,
    "service_campus": gen_service_campus,
    "formation": gen_formation,
    "procedure_administrative": gen_procedure_administrative,
}

def generer_ligne(categorie: str) -> Tuple[str, str]:
    phrase = GEN_FONCTIONS[categorie]()
    if peut(ALT_FORM_RATE):
        phrase = reformuler(phrase)
    if peut(PREFIX_RATE):
        phrase = ajouter_prefixe(phrase)
    if peut(SUFFIX_RATE):
        phrase = ajouter_suffixe(phrase)
    phrase = appliquer_bruit(phrase)
    if not phrase.endswith("?"):
        phrase += " ?"
    return (phrase, categorie)

def generer_dataset(nb_lignes: int) -> List[Tuple[str, str]]:
    par_categorie = nb_lignes // len(LABELS)
    reste = nb_lignes % len(LABELS)
    compte = {lbl: par_categorie for lbl in LABELS}
    for lbl in random.sample(LABELS, reste):
        compte[lbl] += 1

    lignes = []
    for lbl in LABELS:
        lignes.extend(generer_ligne(lbl) for _ in range(compte[lbl]))
    random.shuffle(lignes)
    return lignes

def enregistrer_csv(lignes: List[Tuple[str, str]], chemin: str):
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Categorie"])
        writer.writerows(lignes)
    print(f"✅ {len(lignes)} lignes générées et enregistrées dans '{chemin}'")

# -----------------------------
# EXÉCUTION
# -----------------------------
if __name__ == "__main__":
    print(f"Génération de {N_SAMPLES} questions variées...")
    dataset = generer_dataset(N_SAMPLES)
    enregistrer_csv(dataset, OUTPATH)
