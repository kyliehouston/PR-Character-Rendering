from PIL import Image # type: ignore

input_haley = "haley.png"
output_haley = "rescaled_haley.png"
haley_scale_factors = {
    "head": 1.121,
    "shoulder/chest": 1.176,
    "chest to crotch": 1.176,
    "crotch to knee": 1.265,
    "knee to toe": 1.265
    # on a 5'8" scale
}



# load image
img_h = Image.open(input_haley)
width, height = img_h.size
# Haley is 84x170

# define regions. Top left to bottom right
# ((startx, starty, width, height))
# might need to divide to waist, shoulders, etc
regions = {
    "head": (0, 0, 83, 73),
    "shoulder/chest": (0, 74, 83, 16),
    "chest to crotch": (0, 91, 83, 22), #to bottom of hands
    "crotch to knee": (0, 114, 83, 20), 
    "knee to toe": (0, 134, 83, 28)
}

# scale and divide into parts
parts = []
for part, (x, y, w, h) in regions.items():
    crop = img_h.crop((x, y, x + w, y + h))
    scale = haley_scale_factors[part]
    new_h = int(h * scale)
    resized = crop.resize((w, new_h), resample=Image.NEAREST)
    parts.append(resized)

# stack em up
total_height = sum(part.height for part in parts)
output = Image.new("RGBA", (width, total_height))

y_offset = 0
for part in parts:
    output.paste(part, (0, y_offset))
    y_offset += part.height

output.save(output_haley)
output.show()
