import os
import torch
from transformers import SegformerForSemanticSegmentation


def load_model(device):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "models", "segformer_rgb_flask.pth")

    checkpoint = torch.load(model_path, map_location=device)
    cfg = checkpoint["model_config"]

    # 1. Load SegFormer (RGB only)
    model = SegformerForSemanticSegmentation.from_pretrained(
        cfg["model_name"],
        num_labels=cfg["num_labels"],
        ignore_mismatched_sizes=True
    )

    # 2. Load trained weights
    model.load_state_dict(
        checkpoint["model_state_dict"],
        strict=True
    )

    # 3. Finalize
    model.to(device)
    model.eval()

    print("SegFormer loaded successfully")
    print("   Input channels : 3")
    print("   Output classes :", cfg["num_labels"])
    print("   Threshold      :", cfg["prediction_threshold"])

    return (
        model,
        cfg["prediction_threshold"],
        checkpoint["preprocessing"]
    )
