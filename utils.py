import os
import shutil
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


def generate_qr(text_data: str, directory):
    """:return image namae"""
    path = tempfile.mktemp(prefix="qr-", suffix=".png", dir=directory)
    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    clear_folder_contents(directory)
    img.save(path)
    return path.split('\\')[-1]


def clear_folder_contents(folder_path):
    """
    Deletes all files and subdirectories within the specified folder,
    but leaves the folder itself intact.
    """
    # Ensure the folder exists before attempting to clear it
    if not os.path.exists(folder_path):
        print(f"Error: Folder not found at {folder_path}")
        return

    # Loop through all items in the folder
    for item_name in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item_name)

        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                # If it's a file or a symbolic link, delete it
                os.remove(item_path)
                print(f"Deleted file: {item_name}")
            elif os.path.isdir(item_path):
                # If it's a subdirectory, recursively delete it and all its contents
                shutil.rmtree(item_path)
                print(f"Deleted subdirectory: {item_name}")
        except Exception as e:
            # Catch errors like permissions issues
            print(f"Failed to delete {item_path}. Reason: {e}")


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
