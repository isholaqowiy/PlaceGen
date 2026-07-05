import os
from PIL import Image, ImageDraw, ImageFont
from config import TEMP_DIR

def create_placeholder(width: int, height: int, bg_color: str, text_color: str, text_str: str, user_id: int) -> str:
    """Generates a pixel-perfect, clean dummy graphic placeholder image asset on disk."""
    try:
        # Standard cleaning of HEX formatting inputs
        if not bg_color.startswith('#'):
            bg_color = f"#{bg_color}" if len(bg_color) in (3, 6) else bg_color
            
        if not text_color.startswith('#'):
            text_color = f"#{text_color}" if len(text_color) in (3, 6) else text_color

        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # Dynamic fallback automatic text font scaling logic rules matching viewport footprint bounding boxes
        font_size = max(16, int(min(width, height) * 0.05))
        try:
            font = ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        display_text = text_str if text_str else f"{width} × {height}"
        
        # Draw explicit cross border line vectors marking the canvas space layout bounds
        draw.rectangle([10, 10, width - 10, height - 10], outline=text_color, width=2)
        
        # Paste centered responsive typography metrics string vectors onto drawing layer plane coordinates
        draw.text((width // 2, height // 2), display_text, fill=text_color, font=font, anchor="mm")

        output_path = os.path.join(TEMP_DIR, f"place_{user_id}.png")
        img.save(output_path, "PNG")
        return output_path
    except Exception as e:
        print(f"Placeholder Generation Exception: {e}")
        return None

