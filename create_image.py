from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(path):
    img = Image.new('RGB', (300, 300), color = (56, 189, 248))
    d = ImageDraw.Draw(img)
    try:
        # distinct colors for gradient-like effect
        for i in range(300):
            r = int(56 + (i/300)*100)
            g = int(189 - (i/300)*50)
            b = 248
            d.line([(i, 0), (i, 300)], fill=(r, g, b))
    except Exception:
        pass
        
    img.save(path)
    print(f"Created placeholder image at {path}")

if __name__ == "__main__":
    os.makedirs("static/images", exist_ok=True)
    create_placeholder_image("static/images/profile.png")
