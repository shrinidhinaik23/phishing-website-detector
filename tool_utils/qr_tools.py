import qrcode
from io import BytesIO

def generate_qr(data):
    qr = qrcode.make(data)
    img_buffer = BytesIO()
    qr.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer