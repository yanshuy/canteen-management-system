from PIL import Image, ImageDraw

def create_default_image(size=(200, 200), bg_color="#EEEEEE", text="No Image", text_color="#999999"):
    """Create a default placeholder image when an image is not found"""
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a border
    draw.rectangle([(0, 0), size], outline="#CCCCCC", width=2)
    
    # Draw an X across the image
    draw.line([(0, 0), size], fill="#CCCCCC", width=2)
    draw.line([(0, size[1]), (size[0], 0)], fill="#CCCCCC", width=2)
    
    # Note: For proper text rendering we would need a font, but for simplicity
    # we'll skip that since ImageDraw requires a font file
    
    return img
