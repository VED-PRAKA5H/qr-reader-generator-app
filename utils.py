import os
import time
import tempfile
import cv2
import qrcode
from qrcode.main import QRCode


def scan_qr_from_image(image_path: str):
    """Example usage:
    scan_qr_from_image("path/to/your/qrcode_image.png")"""
    # Open the image file
    img = cv2.imread(image_path)

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)

    if data:
        return data
    else:
        return None


def clear_folder_contents(folder, max_age_seconds=300):
    """Deletes all files and subdirectories inside a folder."""
    now = time.time()

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            if now - os.path.getmtime(path) > max_age_seconds:
                os.remove(path)


def generate_qr(text_data: str, directory: str) -> str:
    """Generate QR code and return image filename."""
    if not text_data:
        raise ValueError("QR data cannot be empty")

    os.makedirs(directory, exist_ok=True)

    # Clear old files first
    clear_folder_contents(directory)

    with tempfile.NamedTemporaryFile(
        dir=directory,
        prefix="qr-",
        suffix=".png",
        delete=False
    ) as tmp:
        file_path = tmp.name

    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

    return os.path.basename(file_path)


def live_qr_scan():
    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Cannot access camera")
        return

    detector = cv2.QRCodeDetector()

    print("📷 QR Code scanner activated.")
    print("Point a QR code at the camera. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        # Decode QR from current frame
        data, points, _ = detector.detectAndDecode(frame)

        if data:
            print("✅ QR Code detected:", data)

            # Draw bounding box if QR detected
            if points is not None:
                points = points.astype(int)
                cv2.polylines(frame, [points], True, (0, 255, 0), 2)

                # Put decoded text
                cv2.putText(
                    frame,
                    data,
                    (points[0][0][0], points[0][0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        # Show video feed
        cv2.imshow("Live QR Scanner", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
