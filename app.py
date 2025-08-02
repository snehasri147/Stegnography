import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from stego_utils import encode_text_in_image, decode_text_from_image

app = Flask(__name__)
app.secret_key = "stegosecret"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = request.files.get("image")
        mode = request.form.get("mode")
        text = request.form.get("text", "")

        if not image or not mode:
            flash("Image and mode are required.", "error")
            return redirect(url_for("index"))

        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

        if mode == "encode":
            if not text:
                flash("Text is required for encoding.", "error")
                return redirect(url_for("index"))
            output_path = os.path.join(UPLOAD_FOLDER, "stego_output.png")
            try:
                encode_text_in_image(image_path, text, output_path)
                return send_file(output_path, as_attachment=True)
            except Exception as e:
                flash(str(e), "error")
                return redirect(url_for("index"))

        elif mode == "decode":
            try:
                hidden_text = decode_text_from_image(image_path)
                flash("Decrypted text: " + hidden_text, "success")
            except Exception as e:
                flash("Error: " + str(e), "error")

            return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
