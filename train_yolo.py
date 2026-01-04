from ultralytics import YOLO
import torch
from pathlib import Path


def train_malaria_detector():
 
    # Configurações
    DATA_YAML = "Malaria.v2-dataset_1_to_7_esquerdo/data.yaml"
    MODEL_NAME = "yolov8n.pt" 
    EPOCHS = 100
    IMG_SIZE = 640
    BATCH_SIZE = 16
    DEVICE = 0 if torch.cuda.is_available() else 'cpu'
    

    
    # Criar diretório de resultados se não existir
    results_dir = Path("runs/detect")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Carregar modelo
    model = YOLO(MODEL_NAME)
    
    # Treinar modelo
    results = model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH_SIZE,
        device=DEVICE,
        plots=True,
        patience=20,  # Early stopping
        project="runs/detect",
        name="malaria_detection",
        exist_ok=True,
        pretrained=True,
        optimizer='Adam',
        verbose=True,
        seed=42,
        augmentations=[]
    )


    with open(f"{results_dir}/training_results.json", 'w') as file:
      results_json = results.to_json()
      file.write(results_json)

    print("Treinamento concluído. Resultados salvos em:", results_dir)


if __name__ == "__main__":
    train_malaria_detector()