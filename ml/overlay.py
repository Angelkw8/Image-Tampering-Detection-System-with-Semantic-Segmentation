import cv2
import numpy as np

def create_overlay(image_path, mask, save_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    h, w = image.shape[:2]
    mask = cv2.resize(mask, (w, h))

    overlay = image.copy()

    # Red color for tampered area
    overlay[mask > 0] = [255, 0, 0]

    # Blend original and overlay
    blended = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)

    cv2.imwrite(save_path, cv2.cvtColor(blended, cv2.COLOR_RGB2BGR))
