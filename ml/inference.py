import torch
import torch.nn.functional as F
import numpy as np

def predict(model, img, device, threshold):

    img = img.to(device)

    with torch.no_grad():
        outputs = model(pixel_values=img)
        logits = outputs.logits  # [1, 1, H, W] for binary

        logits = F.interpolate(
            logits,
            size=img.shape[-2:],
            mode="bilinear",
            align_corners=False
        )

        probs = torch.sigmoid(logits)  # confidence map (0–1)

        mask = (probs > threshold).float()

    # Convert to numpy
    probs_np = probs.squeeze().cpu().numpy()
    mask_np = mask.squeeze().cpu().numpy()

    tampered = bool(mask_np.sum() > 0)

    # REAL confidence score
    if tampered:
        confidence = float(probs_np[mask_np > 0].mean())
    else:
        confidence = float(1.0 - probs_np.mean())

    confidence = round(confidence * 100, 2)  # percentage

    return mask_np, confidence, tampered
