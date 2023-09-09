from PIL import Image

def pillow_draw(char, w, h):
    w = int(w)
    h = int(h)
    img = Image.open(f"pillow_bot/{char}.png")
    img_w, img_h = img.size


    background = Image.open('pillow_bot/bg.png')
    bg_w, bg_h = background.size
    offset = (bg_w // 7 * w - img_w // 3 * 2, bg_h // 10 * (1 + h))
    background.paste(img, offset, img)
    background.save('pillow_bot/bg.png')
