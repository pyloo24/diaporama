import os
import json
from PIL import Image

# Configuration
folder_path = 'images'
thumb_folder = 'vignettes'
hd_folder = 'hd'
thumb_size = (500, 500) # Taille suffisante pour la mosaïque
hd_size = (1920, 1920)  # Taille max pour la lightbox (Full HD)

# Créer les dossiers s'ils n'existent pas
for folder in [thumb_folder, hd_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

image_list = []
extensions = ('.jpg', '.jpeg', '.png', '.webp')

print("Début du traitement des images...")

for filename in os.listdir(folder_path):
    if filename.lower().endswith(extensions):
        try:
            img = Image.open(os.path.join(folder_path, filename))
            
            # Convertir en RGB (pour éviter les erreurs avec les PNG transparents ou CMJN)
            img = img.convert('RGB')

            # 1. Créer la version HD optimisée (WebP)
            hd_filename = os.path.splitext(filename)[0] + '.webp'
            img.thumbnail(hd_size, Image.Resampling.LANCZOS)
            img.save(os.path.join(hd_folder, hd_filename), 'WEBP', quality=80)

            # 2. Créer la vignette carrée (WebP)
            # On recadre au centre pour faire un carré parfait
            width, height = img.size
            min_dim = min(width, height)
            left = (width - min_dim)/2
            top = (height - min_dim)/2
            right = (width + min_dim)/2
            bottom = (height + min_dim)/2
            thumb = img.crop((left, top, right, bottom))
            thumb.thumbnail(thumb_size, Image.Resampling.LANCZOS)
            thumb.save(os.path.join(thumb_folder, hd_filename), 'WEBP', quality=70)

            image_list.append(hd_filename)
            print(f"OK : {filename}")
        except Exception as e:
            print(f"Erreur sur {filename}: {e}")

# Sauvegarder la liste
with open('images.json', 'w') as f:
    json.dump(image_list, f)

print(f"\nTerminé ! {len(image_list)} images traitées.")
