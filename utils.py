import base64
from io import BytesIO
import io

from PIL import Image

def get_abs_pos(pos_prct):
    x_prct, y_prct = pos_prct
    x = get_abs_x(x_prct)
    y = get_abs_y(y_prct)
    return (x, y)

def get_abs_x(field_coordinates, x_prct):
    (x1, y1), (x2, y2) = field_coordinates
    return round(x1 + (((x2 - x1) / 100) * x_prct))

def get_abs_y(field_coordinates, y_prct):
    (x1, y1), (x2, y2) = field_coordinates
    return round(y1 + (((y2 - y1) / 100) * y_prct))

# def get_abs_x_distance(field_coordinates, x_prct):
#     (x1, y1), (x2, y2) = field_coordinates
#     return round(((x2 - x1) / 100) * x_prct)

# def get_abs_y_distance(field_coordinates, y_prct):
#     (x1, y1), (x2, y2) = field_coordinates
#     return round(((y2 - y1) / 100) * y_prct)

def to_base64(img) -> str:
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def to_buffer(img) -> str:
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def resize_img(img, max_width=500):
    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((int(w*ratio), int(h*ratio)))
    return img

def load_image(img_path: str):
    return Image.open(img_path)