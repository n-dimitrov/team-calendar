import pytesseract
from pytesseract import Output
from PIL import Image

image_path = "2024.04.png"

image = Image.open(image_path)
custom_config = r'--oem 3 --psm 6'  # Configuration for better table recognition
text = pytesseract.image_to_string(image, config=custom_config)
lines = text.strip().split('\n')

print("Lines: ", len(lines))
with open("text.txt", "w") as f:
    for line in lines[1:]:
        f.write(line + '\n')

print("Saved to text.txt")
