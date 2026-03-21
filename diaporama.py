import os
import requests
from tqdm import tqdm
import time

# Configuration
QUERY = "travel"  # Thème de recherche
LIMIT = 1000      # Nombre d'images à télécharger
DOWNLOAD_FOLDER = "wikimedia_travel"  # Dossier de destination
USER_AGENT = "DiaporamaScript/1.0 (votre@email.com)"  # Obligatoire pour Wikimedia

# Créer le dossier s'il n'existe pas
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_wikimedia_images(query, limit):
    base_url = "https://commons.wikimedia.org/w/api.php"
    headers = {"User-Agent": USER_AGENT}

    # Étape 1 : Rechercher les images
    search_params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": f"{query} filetype:jpg|png|jpeg",
        "srnamespace": 6,  # Espace "Fichier"
        "srlimit": min(limit, 500),  # Max 500 par requête (limite Wikimedia)
        "srsort": "relevance",
    }

    try:
        response = requests.get(base_url, headers=headers, params=search_params)
        response.raise_for_status()  # Lève une erreur si la requête échoue
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la recherche d'images : {e}")
        return
    except ValueError as e:
        print(f"Erreur de décodage JSON : {e}")
        print(f"Réponse reçue : {response.text}")
        return

    images = data.get("query", {}).get("search", [])
    if not images:
        print("Aucune image trouvée.")
        return

    # Étape 2 : Télécharger les images
    with tqdm(total=min(limit, len(images)), desc="Téléchargement") as pbar:
        for img in images[:limit]:
            title = img["title"]
            # Récupérer l'URL de l'image
            img_params = {
                "action": "query",
                "format": "json",
                "prop": "imageinfo",
                "iiprop": "url",
                "titles": title,
            }

            try:
                img_response = requests.get(base_url, headers=headers, params=img_params)
                img_response.raise_for_status()
                img_data = img_response.json()
                pages = img_data.get("query", {}).get("pages", {})

                for page in pages.values():
                    img_url = page.get("imageinfo", [{}])[0].get("url")
                    if not img_url:
                        print(f"URL introuvable pour {title}")
                        continue

                    # Télécharger l'image
                    filename = os.path.join(DOWNLOAD_FOLDER, f"{title.replace('File:', '').replace(' ', '_')}")
                    try:
                        img_file = requests.get(img_url, headers=headers, stream=True)
                        img_file.raise_for_status()
                        with open(filename, "wb") as f:
                            for chunk in img_file.iter_content(1024):
                                f.write(chunk)
                        pbar.update(1)
                    except Exception as e:
                        print(f"Erreur lors du téléchargement de {title} : {e}")

            except Exception as e:
                print(f"Erreur pour {title} : {e}")

            time.sleep(0.5)  # Éviter de surcharger le serveur

if __name__ == "__main__":
    get_wikimedia_images(QUERY, LIMIT)
