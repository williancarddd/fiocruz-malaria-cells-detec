#!/usr/bin/env python3
import os
import hashlib
from collections import defaultdict
from pathlib import Path

def calculate_image_hash(image_path):
    hash_md5 = hashlib.md5()
    try:
        with open(image_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Erro ao processar {image_path}: {e}")
        return None

def find_images_in_directory(directory):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    images = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                full_path = os.path.join(root, file)
                images.append(full_path)
    
    return images

def find_duplicate_images():
    base_dir = Path(__file__).parent
    folders = [
        base_dir / "OneDrive_1_12-2-2025",
        base_dir / "OneDrive_1_11-4-2025"
    ]
    
    hash_to_images = defaultdict(list)
    
    print("Procurando imagens...")
    all_images = []
    for folder in folders:
        if folder.exists():
            images = find_images_in_directory(folder)
            all_images.extend(images)
            print(f"Encontradas {len(images)} imagens em {folder.name}")
        else:
            print(f"Pasta não encontrada: {folder}")
    
    print(f"\nTotal de imagens encontradas: {len(all_images)}")
    print("\nCalculando hashes...")
    
    for idx, image_path in enumerate(all_images, 1):
        if idx % 100 == 0:
            print(f"Processando {idx}/{len(all_images)}...")
        
        image_hash = calculate_image_hash(image_path)
        if image_hash:
            hash_to_images[image_hash].append(image_path)
    
    print("\nIdentificando duplicatas...")
    
    duplicates = {}
    for image_hash, image_list in hash_to_images.items():
        if len(image_list) > 1:
            duplicates[image_hash] = image_list
    
    output_file = base_dir / "imagens_repetidas.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("IMAGENS REPETIDAS\n")
        f.write("=" * 80 + "\n\n")
        
        if duplicates:
            total_duplicates = 0
            for image_hash, image_list in duplicates.items():
                total_duplicates += len(image_list)
                f.write(f"Hash: {image_hash}\n")
                f.write(f"Quantidade de cópias: {len(image_list)}\n")
                f.write("-" * 80 + "\n")
                for image_path in image_list:
                    relative_path = os.path.relpath(image_path, base_dir)
                    f.write(f"  {relative_path}\n")
                f.write("\n")
            
            f.write(f"\nTotal de grupos de duplicatas: {len(duplicates)}\n")
            f.write(f"Total de imagens duplicadas: {total_duplicates}\n")
        else:
            f.write("Nenhuma imagem duplicada encontrada.\n")
    
    print(f"\nResultado salvo em: {output_file}")
    print(f"Grupos de duplicatas encontrados: {len(duplicates)}")
    
    if duplicates:
        total_duplicates = sum(len(images) for images in duplicates.values())
        print(f"Total de imagens duplicadas: {total_duplicates}")

if __name__ == "__main__":
    find_duplicate_images()


