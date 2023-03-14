from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pathlib import Path


CR_PATH = Path(__file__).parent / 'cr'
DICE_PATH = Path(__file__).parent / "dices"


def centered_text(text, img, pos, rgb):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str((CR_PATH / 'Supercell-Magic_1.ttf').resolve()), 24)
    _, _, size_w, size_h = draw.textbbox((0, 0), text, font=font)
    draw.text((pos[0] - size_w // 2, pos[1] - size_h // 2),
              text, (rgb[0], rgb[1], rgb[2]), font=font)
    return size_w, size_h


def add_text(text, img, pos, rgb):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(str((CR_PATH / 'Supercell-Magic_1.ttf').resolve()), 24)
    _, _, size_w, size_h = draw.textbbox((0, 0), text, font=font)
    draw.text(pos, text, rgb, font=font)
    return size_w, size_h


def add_chest(chest, x, y, background, number):
    background.paste(chest, box=(x, y), mask=chest)
    add_text(str(number), background, (x + 40, y + 100), (255, 255, 255))


chests = {}


def get_chests():
    if not chests:
        for i in range(len(chest_names)):
            _chest = Image.open(CR_PATH / f'{list(chest_names)[i]}.png', 'r')
            _chest.thumbnail((100, 100))
            chests[list(chest_names)[i]] = _chest
    return chests
        

chest_names = {
    'Wooden Chest': 'wooden_chest', 'Silver Chest': 'silver_chest', 'Golden Chest': 'golden_chest',
    'Magical Chest': 'magical_chest', 'Giant Chest': 'giant_chest', 'Mega Lightning Chest': 'mega_lightning_chest',
    'Epic Chest': 'epic_chest', 'Legendary Chest': 'legendary_chest', 'Gold Crate': 'gold_crate',
    'Plentiful Gold Crate': 'plentiful_gold_crate', 'Overflowing Gold Crate': 'overflowing_gold_crate',
    'Royal Wild Chest': 'royal_wild_chest'}
