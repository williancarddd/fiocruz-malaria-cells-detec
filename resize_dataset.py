import cv2
import numpy as np
from pathlib import Path
import shutil

SOURCE_DIR = "Malaria.v2-dataset_1_to_7_esquerdo"
TARGET_DIR = "Malaria.v2-dataset_1_to_7_esquerdo_640"
TARGET_SIZE = (640, 640)

def resize_dataset():
    source_path = Path(SOURCE_DIR)
    target_path = Path(TARGET_DIR)
    
    for split in ['train', 'valid', 'test']:
        source_images = source_path / split / 'images'
        source_labels = source_path / split / 'labels'
        target_images = target_path / split / 'images'
        target_labels = target_path / split / 'labels'
        
        target_images.mkdir(parents=True, exist_ok=True)
        target_labels.mkdir(parents=True, exist_ok=True)
        
        if not source_images.exists():
            print(f"⚠️  {source_images} não encontrado, pulando...")
            continue
            
        print(f"📁 Processando {split}...")
        
        image_files = list(source_images.glob('*.[jp][pn][g]'))
        for img_path in image_files:
            img = cv2.imread(str(img_path))
            if img is None:
                print(f"⚠️  Erro ao ler {img_path}")
                continue
            
            resized = cv2.resize(img, TARGET_SIZE, interpolation=cv2.INTER_LINEAR)
            cv2.imwrite(str(target_images / img_path.name), resized)
            
            label_path = source_labels / f"{img_path.stem}.txt"
            if label_path.exists():
                shutil.copy2(label_path, target_labels / label_path.name)
        
        print(f"✅ {split}: {len(image_files)} imagens redimensionadas")
    
    # Copiar data.yaml
    source_yaml = source_path / 'data.yaml'
    if source_yaml.exists():
        shutil.copy2(source_yaml, target_path / 'data.yaml')
        print(f"✅ data.yaml copiado")
    
    print(f"\n✅ Dataset redimensionado salvo em: {TARGET_DIR}")

if __name__ == "__main__":
    resize_dataset()
