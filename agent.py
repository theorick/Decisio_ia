import subprocess
import sys
import requests
import json
import time
import re
import pyfiglet

MODEL_CHEF = 'deepseek-r1:latest'
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"
TARGET_FILE = "programme.py"

BASE_PROMPT = """
🧱 Éléments du jeu
1. Fenêtre de jeu

Taille fixe (ex: 800x600)

Fond uni (noir ou autre)

Boucle principale de jeu (game loop)

2. Raquette (pong)

Positionnée sur le côté gauche de l’écran

Déplacement vertical uniquement

Ne peut pas sortir de l’écran

Vitesse de déplacement constante

3. Balle

Forme : cercle

Position initiale : centre de l’écran

Vitesse constante en X et Y

Se déplace automatiquement

🔄 Règles de mouvement et collisions
Rebond sur les murs

Si la balle touche :

le mur haut → inversion de la vitesse verticale

le mur bas → inversion de la vitesse verticale

Rebond sur la raquette

Si la balle touche la raquette :

inversion de la vitesse horizontale

la balle repart dans l’autre sens

Sortie de l’écran

Si la balle dépasse le bord gauche ou droit :

le jeu peut soit :

se terminer

soit réinitialiser la balle (au choix de l’implémentation)

🔁 Boucle principale du jeu

La boucle doit :

Lire les événements clavier

Mettre à jour la position de la raquette

Mettre à jour la position de la balle

Gérer les collisions

Rafraîchir l’affichage

Limiter le nombre d’images par seconde (FPS)

🧪 Mode test (optionnel mais recommandé)

Un mode test automatique sans interaction clavier

La raquette peut rester immobile

Permet de vérifier :

déplacement de la balle

rebonds sur les murs

absence de crash

⚠️ Contraintes importantes

Pas de input()

Pas de blocage de la boucle principale

Code simple et lisible

Pas de fonctionnalités inutiles (score, menus, sons non obligatoires)

Une seule raquette (joueur unique)

✅ Critères de validation

Le Pong est valide si :

La fenêtre s’ouvre correctement

La balle bouge en continu

Les rebonds fonctionnent

Les touches z et s contrôlent la raquette

Le programme ne plante pas
"""

#Agent IA
def ask_ollama(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "prompt": prompt,
        "temperature": 0.6,
        "num_ctx": 4096,
        "max_tokens": 2048,
        "stream": True
    }

    response_text = ""

    with requests.post(OLLAMA_URL, json=data, headers=headers, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                try:
                    j = json.loads(line.decode("utf-8"))
                    response_text += j.get("response", "")
                    if j.get("done"):
                        break
                except json.JSONDecodeError:
                    pass

    return response_text.strip()

def agent_logic(prompt):
    prompt += f"""
                Tu es un développeur Python.
                Voici une spécification fonctionnelle :

                {prompt}

                Génère UNIQUEMENT du code Python valide.
                """


    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "prompt": prompt,
        "temperature": 0.6,
        "num_ctx": 4096,
        "max_tokens": 2048,
        "stream": True
    }

    response_text = ""

    with requests.post(OLLAMA_URL, json=data, headers=headers, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                try:
                    j = json.loads(line.decode("utf-8"))
                    response_text += j.get("response", "")
                    if j.get("done"):
                        break
                except json.JSONDecodeError:
                    pass

    return response_text.strip()

def agent_design(prompt):
    prompt += """
            Tu es un architecte logiciel/design.
            À partir du prompt suivant, définis :
            - la structure du programme
            - les fonctions nécessaires
            - les modes (test / normal)
            - les contraintes importantes

            Ne produis PAS de code.

                """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "prompt": prompt,
        "temperature": 0.6,
        "num_ctx": 4096,
        "max_tokens": 2048,
        "stream": True
    }

    response_text = ""

    with requests.post(OLLAMA_URL, json=data, headers=headers, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                try:
                    j = json.loads(line.decode("utf-8"))
                    response_text += j.get("response", "")
                    if j.get("done"):
                        break
                except json.JSONDecodeError:
                    pass

    return response_text.strip()

def chef_orchestre(origine, code, design):
    headers = {"Content-Type": "application/json"}

    prompt = f"""
    SYSTEM:
    Tu es un agent décideur STRICT.
    Tu NE PARLES PAS.
    Tu NE COMMENTES PAS.
    Tu NE FOURNIS PAS DE CODE.
    Tu RÉPONDS UNIQUEMENT EN JSON VALIDE.

    Si tu réponds autre chose que du JSON → tu as échoué.

    FORMAT OBLIGATOIRE (et rien d’autre) :
    {{
      "decision": "ACCEPT" ou "REJECT",
      "reason": "phrase courte"
    }}

    SPECIFICATION :
    {design}

    CODE :
    {code}

    RAPPEL :
    - Aucun texte hors JSON
    - Aucun markdown
    - Aucun commentaire
    - Aucun bloc ```python```
    - JSON strict uniquement
    """

    data = {
        "model": MODEL_CHEF,
        "prompt": prompt,
        "temperature": 0.6,
        "num_ctx": 4096,
        "max_tokens": 2048,
        "stream": True
    }

    response_text = ""

    with requests.post(OLLAMA_URL, json=data, headers=headers, stream=True) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if line:
                try:
                    j = json.loads(line.decode("utf-8"))
                    response_text += j.get("response", "")
                    if j.get("done"):
                        break
                except json.JSONDecodeError:
                    pass

    return response_text.strip()

#Extraction code plus décision
def extract_code(text):
    match = re.search(r"```python(.*?)```", text, re.S)
    if match:
        return match.group(1).strip()
    return text.strip()

def write_code(code):
    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(code)

def run_code():
    return subprocess.run(
        [sys.executable, TARGET_FILE],
        capture_output=True,
        text=True

    )

def extract_json(text):
    # Cherche le bloc ```json ... ```
    match = re.search(r"```json(.*?)```", text)
    if match:
        try:
            return json.loads(match.group(1))  # <-- convertit en dict
        except json.JSONDecodeError:
            return None

    # fallback : JSON isolé sans bloc
    match = re.search(r"(\{[\s\S]*?\})", text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None

    return None

def interpret_decision(decision_text):
    data = extract_json(decision_text)
    print(data)

    if not data:
        return "REJECT", "JSON invalide ou absent"

    decision = data.get("decision", "").upper()
    reason = data.get("reason", "Aucune raison fournie")

    if decision not in ["ACCEPT", "REJECT"]:
        return "REJECT", "Décision inconnue"

    return decision, reason

if __name__ == "__main__":
    prompt = BASE_PROMPT
    iteration = 1
    ascii_banner = pyfiglet.figlet_format('Decisio_ia', font="3d-ascii", width=1500)
    print("\n", "-" * 70, "\n")
    print("" + ascii_banner + "")
    print( "-" * 80, "\n")
    print(f"\n🤖 Itération {iteration}")
    design_response = agent_design(prompt)
    print(f"\nDESIGN :\n{design_response}\n")

    while True:
        print(f"\n🤖 Itération {iteration}")
        iteration += 1
        logic_response = agent_logic(design_response)
        print(f"\nLOGIQUE :\n{logic_response}\n")
        code = extract_code(logic_response)
        decideur_response = chef_orchestre(BASE_PROMPT, code, design_response)
        print(f"\nDECIDEUR :\n{decideur_response}\n")
        decision, reason = interpret_decision(decideur_response)
        print(decision, reason)



        if decision == "ACCEPT":
            write_code(code)
            print("▶️ Exécution du programme...")
            result = run_code()

            if result.returncode == 0:
                print("✅ Aucun crash Python détecté.")
                print("🎉 Programme stable.")
                break
            else:
                print("❌ Erreur détectée :")
                print(result.stderr)

                prompt = f"""
                Voici un programme Python qui contient une erreur.
                
                CODE :
                {code}
                
                ERREUR PYTHON :
                {result.stderr}
                
                Corrige le programme.
                Retourne UNIQUEMENT le code Python corrigé.
                """
                time.sleep(1)

