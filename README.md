# 🤖 Agentic AI Code Orchestrator

Un projet **d’IA agentique locale** capable de **concevoir, coder, tester et valider automatiquement** un programme Python à partir d’une spécification fonctionnelle.

Ce système repose sur une **architecture multi-agents** avec séparation stricte des rôles et un **agent décideur final** garantissant la qualité du résultat.

---

## 🎯 Objectif du projet

Construire une pipeline autonome qui reproduit le fonctionnement d’une **équipe logicielle structurée** :

* 🧠 **Analyse & design logiciel**
* 💻 **Génération de code Python**
* 🧪 **Exécution et détection d’erreurs**
* 🧑‍⚖️ **Validation stricte par un agent arbitre**
* 🔁 **Boucle de correction automatique jusqu’à acceptation**

Aucune intervention humaine n’est requise une fois la spécification fournie.

---

## 🧩 Architecture des agents

### 1️⃣ Agent Design (Architecte)

* Analyse la spécification fonctionnelle
* Définit la structure du programme
* Liste les fonctions, modes et contraintes
* ❌ Ne produit **aucun code**

### 2️⃣ Agent Logic (Développeur)

* Génère **uniquement du code Python valide**
* Suit strictement la spécification produite par l’agent design

### 3️⃣ Agent Chef d’Orchestre (Décideur)

* Analyse le code et la spécification
* Répond **exclusivement en JSON strict**
* Décide : `ACCEPT` ou `REJECT`
* N’écrit **jamais de code**

```json
{
  "decision": "ACCEPT",
  "reason": "Conforme à la spécification"
}
```

---

## 🔄 Cycle d’exécution

1. Lecture de la spécification fonctionnelle
2. Génération du design logiciel
3. Génération du code Python
4. Validation par l’agent décideur
5. Exécution automatique du programme
6. En cas d’erreur → correction automatique
7. Boucle jusqu’à obtention d’un programme stable

---

## 🧪 Mode test

Un **mode test automatique** peut être activé afin de :

* Vérifier les déplacements
* Tester les rebonds
* Garantir l’absence de crash

Sans interaction clavier.

---

## 🛠️ Stack technique

* **Python 3.10+**
* **Ollama (local)**
* **LLMs utilisés** :

  * Agent Logic / Design : `huihui_ai/dolphin3-abliterated`
  * Agent Décideur : `llama3.2:1b`

---

## 📦 Installation

### 1️⃣ Cloner le projet

```bash
git clone <repo-url>
cd agentic-ai-orchestrator
```

### 2️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3️⃣ Lancer Ollama

Assurez-vous qu’Ollama est actif localement :

```bash
ollama serve
```

Et que les modèles sont installés :

```bash
ollama pull huihui_ai/dolphin3-abliterated
ollama pull llama3.2:1b
```

---

## ▶️ Exécution

```bash
python main.py
```

Le programme généré sera écrit dans :

```txt
programme.py
```

Et exécuté automatiquement après validation.

---

## ✅ Critères de validation

Un programme est considéré comme valide si :

* Le code est syntaxiquement correct
* Le programme s’exécute sans crash
* La spécification fonctionnelle est respectée
* L’agent décideur retourne `ACCEPT`

---

## 💡 Philosophie

> L’IA agentique devient réellement efficace lorsqu’on lui impose :
>
> * des rôles stricts
> * des responsabilités claires
> * un arbitre final non négociable

Ce projet explore une approche **anti-hallucination**, orientée **qualité logicielle** et **automatisation robuste**.

---

## 🚀 Pistes d’évolution

* Support multi-projets
* Métriques de qualité du code
* Agents spécialisés (QA, sécurité, performance)
* Interface web / dashboard

---

## 📫 Contact

Projet développé dans une démarche R&D autour des **architectures agentiques locales**.

💬 Ouvert aux échanges, retours et collaborations.

#AgenticAI #LocalAI #Python #LLM #SoftwareEngineering #Automation
