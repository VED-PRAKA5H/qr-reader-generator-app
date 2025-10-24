# Barcode & QR Code Master Scanner + Generator

A privacy-focused, full-stack web application built with **Flask** and **OpenCV**. This tool allows users to generate custom QR codes and scan barcodes/QR codes via image upload or webcam, all without using paid third-party APIs.

## 🚀 Features

* **QR Generation:** Create high-quality QR codes instantly with customizable data
* **Dual Scanning:** Upload local image files or use your device's webcam for real-time scanning
* **Privacy First:** All processing happens on the server using open-source libraries; no data is sent to external APIs
* **Responsive UI:** Crafted with Bootstrap 5, featuring a sleek Dark/Light mode toggle
* **Dockerized:** Fully containerized for consistent deployment across environments
* **CI/CD Ready:** GitHub Actions workflow for automated Docker image builds and deployment

## 🛠️ Tech Stack

* **Backend:** Python 3.12, Flask 2.3.2
* **Processing:** OpenCV (`opencv-python-headless`), `qrcode`, Pillow
* **Frontend:** HTML5, CSS3, Bootstrap 5, Jinja2
* **Deployment:** Docker, Gunicorn, Railway
* **DevOps:** Multi-stage Docker builds with non-privileged user security, GitHub Actions CI/CD

## 📦 Installation & Local Setup

### Prerequisites
- Python 3.12+
- Docker (optional, for containerized deployment)

### 1. Clone the repository:
```bash
git clone https://github.com/VED-PRAKA5H/qr-reader-generator-app
cd qr-reader-generator-app
```

### 2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the app:
```bash
flask run
```

Access the app at `http://127.0.0.1:5000`.

## 🐳 Docker Deployment

The project is optimized for production using a `python:3.12-slim` base image with security best practices.

### Build the image:
```bash
docker build -t qrapp .
```

### Run the container:
```bash
docker run -p 8000:8000 qrapp
```

### Push to Docker Hub:
```bash
docker tag qrapp ved4dev/qrapp:latest
docker push ved4dev/qrapp:latest
```

> **Technical Note:** The project uses `opencv-python-headless` instead of the full `opencv-python` package, eliminating the need for GUI-related system dependencies (`libGL`, `libX11`) and resulting in a smaller, more efficient Docker image (~200MB smaller).

## 🔄 CI/CD with GitHub Actions

Automated Docker image building and deployment using GitHub Actions:

### Setup:
1. Add Docker Hub credentials to GitHub Secrets:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD` (or access token)

2. The workflow automatically:
   - Builds Docker images on push to `main`
   - Tags with multiple versions (commit SHA, branch name, `latest`)
   - Pushes to Docker Hub
   - Can be triggered manually via `workflow_dispatch`

### Manual Trigger:
Go to **Actions** → **Docker Image CI** → **Run workflow**

## 📝 Key Technical Decisions & Solutions

### Challenge 1: OpenCV ImportError in Docker
**Problem:** `ImportError: libGL.so.1: cannot open shared object file`

**Solution:** Switched from `opencv-python` to `opencv-python-headless`, which is specifically designed for server environments without display capabilities. This eliminated the need for system graphics libraries and reduced image size.

### Challenge 2: Permission Denied in Railway Deployment
**Problem:** `PermissionError: [Errno 13] Permission denied: '/app/uploads'`

**Solution:** 
- Used `/tmp/uploads` instead of `/app/uploads` (writable by non-privileged users)
- Created directory in Dockerfile as root, then assigned ownership to `appuser`
- Ensured all file operations use `os.path.basename()` for cross-platform compatibility

### Challenge 3: Docker Security Best Practices
**Implementation:**
- Non-privileged user (`appuser` with UID 10001)
- Proper file ownership with `COPY --chown=appuser:appuser`
- Restrictive directory permissions (`755`)
- Minimal base image (`python:3.12-slim`)

### Challenge 4: Stateless File Management
**Strategy:**
- Temporary file storage in `/tmp/uploads`
- Unique filename generation with `tempfile.mktemp()`
- Periodic cleanup mechanism for old files (prevents disk space issues)

## 🏗️ Project Structure

```text
.
├── app.py                 # Main Flask application
├── utils.py              # QR/Barcode processing utilities
├── templates/            # Jinja2 HTML templates
├── static/               # CSS, JS, images
├── requirements.txt      # Python dependencies
├── Dockerfile           # Multi-stage production build
├── .github/
│   └── workflows/
│       └── docker-image.yml  # CI/CD pipeline
└── README.md
```

## 🔒 Security Features

- **No external API calls** - All processing happens locally
- **Input validation** - File type and size restrictions
- **Secure file handling** - `secure_filename()` usage
- **Non-root container execution** - Follows Docker security best practices
- **Environment-based secrets** - `FLASK_SECRET_KEY` from environment variables

## 📈 Future Improvements

* **Client-Side Scanning:** Integrate `jsQR` for instant webcam feedback without server round-trips
* **Persistent Storage:** Add PostgreSQL/SQLite database for scan history and user accounts
* **Batch Processing:** Allow multiple image uploads for bulk QR code scanning
* **Advanced QR Options:** Support for custom colors, logos, and error correction levels
* **API Endpoints:** RESTful API for programmatic QR generation and scanning
* **Rate Limiting:** Implement request throttling to prevent abuse
* **Monitoring:** Add Prometheus/Grafana for performance metrics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV's community for the robust computer vision library
- Flask team for the lightweight web framework
- Railway for seamless deployment platform
- Bootstrap team for the responsive UI components

---

- **Live Demo:** https://qr.vedp.in
- **Docker Hub:** `ved4dev/qrapp`

Built with ❤️ by Ved Prakash