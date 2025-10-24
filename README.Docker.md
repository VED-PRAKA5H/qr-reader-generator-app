# 🐳 Flask QR & Barcode Tool (Headless OpenCV)

This image provides a fully containerized, production-ready web application for generating and scanning QR codes/Barcodes. It is built on **Python 3.12-slim** and optimized for minimal footprint while including all necessary C-libraries for **OpenCV**.

## 🚀 Quick Start

Run the container immediately using:

```bash
docker run -d \
  -p 8000:8000 \
  --name qr-scanner \
  ved4dev/qrapp:latest

```

Once running, the application is available at `http://localhost:8000`.

## ⚙️ Configuration

### Environment Variables

You can pass these variables using the `-e` flag:

| Variable | Default | Description |
| --- | --- | --- |
| `SECRET_KEY` | *random* | Required for Flask session security and CSRF protection. |
| `PORT` | `8000` | The port Gunicorn will bind to inside the container. |

### Volumes

While the app cleans up files after scanning, you can map the upload directory to your host for debugging:

* `/app/uploads`: Temporary storage for images being processed.

```bash
docker run -d -p 8000:8000 -v $(pwd)/logs:/app/uploads ved4dev/qrapp

```

## 🛠️ Image Features

* **Production Grade:** Uses **Gunicorn** as the WSGI HTTP Server.
* **Security:** Runs as a **non-privileged user** (`appuser` with UID 10001).
* **OpenCV Support:** Pre-configured with `libgl1-mesa-glx` and `libglib2.0-0` to support headless image processing.
* **Lightweight:** Built on Debian-slim to keep image size small while maintaining compatibility.

## 🏗️ Technical Specifications

* **Base Image:** `python:3.12.1-slim`
* **Exposed Ports:** `8000`
* **Working Directory:** `/app`

## 🛡️ Security Note

This image follows the principle of least privilege. The filesystem is writable only in the `/app/uploads` directory by the `appuser`. It is recommended to run the container with `--read-only` and a tmpfs mount on `/app/uploads` for maximum security in sensitive environments.
