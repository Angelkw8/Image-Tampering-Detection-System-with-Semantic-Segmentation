# Image-Tampering-Detection-System-with-Semantic-Segmentation
Image tampering detection using semantic segmentation to identify copy-move and splicing manipulations. Trained on the DEFACTO dataset with SegFormer-B2 for image forensics applications. Ongoing work focuses on improving cross-dataset generalization and detection accuracy.

# Features
1. Detects copy-move and splicing attacks
2. Generates segmentation masks highlighting tampered regions
3. Uses SegFormer-B2 architecture for efficient image analysis
4. Produces visual overlay for easy interpretation 
5. Designed for image forensics applications

# Model Overview
1. Architecture: SegFormer-B2 (Semantic Segmentation Transformer)
2. Task: Binary image tampering detection  
3. Output: Pixel-level tampering mask
- Note: Model weights are not included in this repository due to file size limitations.
  
# Project Structure
1. models/            # Pretrained model files (not included if large)
2. inference.py       # Run model inference on input images
3. model_loader.py    # Load trained model and configurations
4. preprocess.py      # Image preprocessing pipeline
5. overlay.py         # Generate overlay results for visualization
   
# How It Works
1. Input image is preprocessed (preprocess.py)
2. Model is loaded using (model_loader.py)
3. Tampering is detected via (inference.py)
4. Results are visualized using (overlay.py)
   
# Installation
1. pip install -r requirements.txt
   
# Usage
python inference.py

# Dataset
1. Trained on the DEFACTO dataset for image forgery detection
2. Dataset not included due to size limitations
   
# Model Weights
Download trained model here:
https://www.kaggle.com/datasets/tuesdayblue/segformer-b2-weights

# Future Improvements
1. Improve cross-dataset generalization
2. Enhance detection accuracy on unseen data
3. Optimize model performance
