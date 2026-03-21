import os
import json

def generate_image_json(image_folder, output_json):
    # Extensions d'images acceptées
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif')
    
    # Vérifier si le dossier existe
    if not os.path.exists(image_folder):
        print(f"Erreur : Le dossier '{image_folder}' n'existe pas.")
        return

    # Lister les fichiers et filtrer par extension
    images = [
        f for f in os.listdir(image_folder) 
        if f.lower().endswith(valid_extensions)
    ]

    # Trier par nom (facultatif)
    images.sort()

    # Créer le fichier JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(images, f, indent=4, ensure_ascii=False)

    print(f"Succès ! {len(images)} images ont été listées dans '{output_json}'.")

# --- CONFIGURATION ---
# Nom du dossier où se trouvent vos images
DOSSIER_IMAGES = 'images' 
# Nom du fichier de sortie
FICHIER_SORTIE = 'images.json'

if __name__ == "__main__":
    generate_image_json(DOSSIER_IMAGES, FICHIER_SORTIE)
