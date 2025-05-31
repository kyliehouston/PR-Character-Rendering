from PIL import Image # type: ignore

input_file = "alex.png"
output_file = "rescaled_alex.png"
scale_factors = {
    "head": 1.125,
    "neck": 1,
    "shoulder/chest": 1.125,
    "chest to crotch": 1.25,
    "crotch to knee": 1.25,
    "knee to toe": 1.25
    # on a 6 foot scale
}

# Load image
img = Image.open(input_file)
# width, height = img.size
width = 84
height = 191
# Alex is 84x191

# Define regions. Top left to bottom right
# ((startx, starty, width, height))
# might need to divide to waist, shoulders, etc
regions = {
    "head": (0, 0, 83, 70),                # height = 70 (0 to 69)
    "shoulder/chest": (0, 70, 83, 26),     # height = 95 - 70 = 25 (or 26 to include row 95)
    "chest to crotch": (0, 96, 83, 38),    # 133 - 96 + 1
    "crotch to knee": (0, 134, 83, 21),    # 154 - 134 + 1
    "knee to toe": (0, 155, 83, 37),       # 191 - 155 + 1
}

# Divide into parts and scale
parts = []

for part, (x, y, w, h) in regions.items():
    crop = img.crop((x, y, x + w, y + h))
    scale = scale_factors[part]
    new_h = int(h * scale)
    resized = crop.resize((w, new_h), resample=Image.NEAREST)
    parts.append(resized)

# Stack em up
total_height = sum(part.height for part in parts)
output = Image.new("RGBA", (width, total_height))

y_offset = 0
for part in parts:
    output.paste(part, (0, y_offset))
    y_offset += part.height

# output
output.save(output_file)
output.show()