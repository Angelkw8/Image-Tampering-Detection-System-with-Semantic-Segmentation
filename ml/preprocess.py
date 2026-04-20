import torch
from PIL import Image
import torchvision.transforms as T


def preprocess_image(image_path, device, preprocessing):
    img = Image.open(image_path).convert("RGB")

    size = preprocessing["image_size"]

    transform = T.Compose([
        T.Resize((size, size)),
        T.ToTensor(),
        T.Normalize(
            mean=preprocessing["mean"],
            std=preprocessing["std"]
        )
    ])

    img = transform(img)          # [3, H, W]
    img = img.unsqueeze(0).to(device)  # [1, 3, H, W]

    return img
