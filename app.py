from flask import (Flask, render_template, request, redirect, url_for, session,
                   flash, jsonify, send_from_directory)
import os
from utils import scan_qr_from_image, live_qr_scan, generate_qr
from flask_bootstrap import Bootstrap5

# --- Configuration ---

# Always use /tmp for uploads (writable by non-privileged users)
UPLOAD_FOLDER = '/tmp/uploads'

# Permissions for directory creation
UPLOAD_DIR_PERMISSIONS = 0o755

# FOR PRODUCTION: Use environment variable
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', os.urandom(32))

# --- Application Setup ---

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    try:
        os.makedirs(UPLOAD_FOLDER, mode=UPLOAD_DIR_PERMISSIONS)
        print(f"Created upload directory: {UPLOAD_FOLDER}")
    except PermissionError as e:
        print(f"Warning: Could not create upload directory: {e}")
        # Directory should already exist from Dockerfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max
bootstrap = Bootstrap5(app)


@app.route('/image/<name>', methods=['POST', 'GET'])
def serve_image(name):
    if request.method == "POST":
        return send_from_directory(
            app.config["UPLOAD_FOLDER"],
            name,
            as_attachment=True
        )
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/")
def index():
    return render_template("index.html", active='home')


@app.route("/generate", methods=["GET", "POST"])
def generate_page():
    if request.method == "POST":
        try:
            data = request.form.get("data", "").strip()
            image_name = generate_qr(text_data=data, directory=UPLOAD_FOLDER)

            flash("QR code generated successfully!", "success")
            return render_template(
                "generate.html",
                image=image_name,
                active="generate"
            )

        except Exception as e:
            # print(f"Error: {e}")
            flash(str(e), "danger")
            return redirect(url_for("generate_page"))

    return render_template("generate.html", image=None, active="generate")


@app.route("/scan", methods=["GET", "POST"])
def scan_page():
    scanned_text = None

    if request.method == "POST":
        # 1. Check if the file part is in the request and has a filename
        if 'barcode_file' in request.files and request.files['barcode_file'].filename != '':
            file = request.files['barcode_file']
            # Use file.filename for the original name
            filename = file.filename
            path = os.path.join(UPLOAD_FOLDER, filename)

            try:
                # 2. Save the file temporarily
                file.save(path)

                # 3. Process the file
                result = scan_qr_from_image(path)
                scanned_text = result

            except Exception as e:
                # Handle potential errors during save or scan
                # print(f"An error occurred: {e}")
                scanned_text = "Error processing image."

            finally:
                # 4. CRITICAL: Clean up the file after processing
                if os.path.exists(path):
                    os.remove(path)
                    # print(f"File deleted: {path}")
            if scanned_text and scanned_text != "Error processing image.":
                flash("Barcode or QR code successfully scanned!", "success")
            else:
                flash("Could not detect any barcode or QR code in the image.", "danger")

    return render_template("scan.html", scanned_text=scanned_text, active='scan')


@app.route("/history")
def history_page():
    if "user_id" not in session:
        flash("Please login to view history", "warning")
        return redirect(url_for("login_page"))

    rows = ''

    return render_template("history.html", rows=rows)


# -----------------------
# AUTH ROUTES
# -----------------------

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = {'': ""}

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials", "danger")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:

            return redirect(url_for("login_page"))
        except:
            flash("Username already exists", "danger")

    return render_template("signup.html")


@app.route("/clear-history", methods=["POST"])
def clear_history():
    pass


@app.route("/reuse/<int:id_>")
def reuse(id_):
    pass


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False, port=8000)
