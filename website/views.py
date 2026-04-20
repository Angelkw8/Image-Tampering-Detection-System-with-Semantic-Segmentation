from flask import (
    Blueprint, render_template, request,
    current_app, send_from_directory,
    flash, send_file, session, redirect, url_for
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import numpy as np
from datetime import datetime

from ml.preprocess import preprocess_image
from ml.inference import predict
from ml.overlay import create_overlay
from website.report_generator import generate_report_bytes

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/image')
@login_required
def image_page():
    return render_template('images.html', user=current_user)

@views.route('/upload-image', methods=['POST'])
@login_required
def upload_image():

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # ---------- 1. Validate file ----------
    file = request.files.get('image')

    if not file or file.filename == "":
        flash("No file selected. Please upload an image.", "error")
        return redirect(url_for('views.image_page'))

    if not allowed_file(file.filename):
        flash("Invalid file format. Only JPG and PNG images are allowed.", "error")
        return redirect(url_for('views.image_page'))

    try:
        # ---------- 2. Secure & save file ----------
        filename = secure_filename(file.filename)

        temp_dir = os.path.join(
            current_app.root_path,
            current_app.config['TEMP_UPLOAD_FOLDER']
        )
        os.makedirs(temp_dir, exist_ok=True)

        original_path = os.path.join(temp_dir, filename)
        overlay_path = os.path.join(temp_dir, f"overlay_{filename}")
        mask_path = os.path.join(temp_dir, "mask.npy")

        file.save(original_path)

        # ---------- 3. Load model config ----------
        model = current_app.config.get("MODEL")
        device = current_app.config.get("DEVICE")
        threshold = current_app.config.get("THRESHOLD")
        preprocessing = current_app.config.get("PREPROCESSING")

        if model is None:
            flash("Detection model is not available. Please try again later.", "error")
            return redirect(url_for('views.image_page'))

        # ---------- 4. Prediction ----------
        img_tensor = preprocess_image(original_path, device, preprocessing)
        mask, confidence, tampered = predict(model, img_tensor, device, threshold)

        create_overlay(original_path, mask, overlay_path)
        np.save(mask_path, mask)

        # ---------- 5. Store result ----------
        session['analysis'] = {
            "original": original_path,
            "overlay": overlay_path,
            "mask": mask_path,
            "tampered": tampered,
            "confidence": float(confidence)
        }

        return render_template(
            'images.html',
            user=current_user,
            file_url=url_for('views.temp_file', filename=filename),
            overlay_url=url_for('views.temp_file', filename=f"overlay_{filename}"),
            tampered=tampered,
            confidence=confidence
        )

    except Exception as e:
        # ---------- 6. Catch-all safety ----------
        print("Upload error:", e)
        flash("An unexpected error occurred during image analysis.", "error")
        return redirect(url_for('views.image_page'))

@views.route('/download-report')
@login_required
def download_report():
    data = session.get('analysis')
    if not data:
        flash("No analysis available", "error")
        return redirect(url_for('views.image_page'))

    mask = np.load(data["mask"])
    confidence = data["confidence"]

    pdf = generate_report_bytes(
        original_image=data["original"],
        overlay_image=data["overlay"],
        tampered=data["tampered"],
        mask=mask,
        confidence=confidence
    )

    return send_file(
        pdf,
        as_attachment=True,
        download_name="tamper_report.pdf",
        mimetype="application/pdf"
    )

@views.route('/temp/<filename>')
@login_required
def temp_file(filename):
    temp_dir = os.path.join(
        current_app.root_path,
        current_app.config['TEMP_UPLOAD_FOLDER']
    )
    return send_from_directory(temp_dir, filename)
