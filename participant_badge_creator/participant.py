# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Participant badge creator
# %% [markdown]
# ```
# import sys  
# !{sys.executable} -m pip install --user fpdf
# ```
# %% [markdown]
# ## Импорты

# %%
import time, os, sys, subprocess
start = time.time()

import matplotlib.font_manager as fm
import math 

from PIL import Image, ImageDraw, ImageFont, ImageOps
from fpdf import FPDF

# %% [markdown]
# ## Константы и размеры

# %%
PIXEL_IN_MM = 2.8 # сколько пикселей в 1 миллиметре (2.8 оптимально)

BADGES_FOLDER = os.path.join('output', 'badges') # папка для сохранения файлов

font = ImageFont.truetype(fm.findfont(fm.FontProperties(family='DejaVu Sans')), size = 100) # шрифт бейджей

pdf = FPDF(orientation='P', format='A4') # параметры .pdf-файла

pdf_name = os.path.join(BADGES_FOLDER, 'badges_binder.pdf') # имя .pdf-файла


# %%
# размер бейджика 90 на 55

badge_h = 55 # mm
badge_w = 90 # mm

bx_px = math.floor(badge_w*PIXEL_IN_MM)
by_px = math.floor(badge_h*PIXEL_IN_MM)

print('Высота бейджа в пикселях =', bx_px, '| Ширина бейджа в пикселях =', by_px)
print()


# %%
# размер а4 297 на 210 мм

list_w = 210 #mm
list_h = 297 #my 

aw = math.floor(list_h/badge_w)
ah = math.floor(list_w/badge_h)
album_total = aw*ah

print('По ширине:', aw, '| По высоте:', ah)
print('Альбомная ориентация, вмещается бейджей: ', album_total)
print()

bw = math.floor(list_w/badge_w)
bh = math.floor(list_h/badge_h)
book_total = bw*bh

print('По ширине:', bw, '| По высоте:', bh)
print('Книжная ориентация, вмещается бейджей: ', book_total)
print()

per_x = 0
per_y = 0

if book_total > album_total:
    per_x = bw
    per_y = bh
else:
    per_x = aw
    per_y = ah

# %% [markdown]
# ## Функции

# %%
x_px = bx_px - 2 #free extra pixels for borders
y_px = by_px - 2

# функции

def badges_block(first_number):
    x = 0
    y = 0
    background = Image.new('RGB', (bx_px*per_x, by_px*per_y), color='white')
    for i in range(first_number, first_number+10):
        if os.path.exists(os.path.join('sources', 'badge_pattern.png')):
            piece = Image.open(os.path.join('sources', 'badge_pattern.png'))
        elif os.path.exists('badge_pattern.png'):
            piece = Image.open('badge_pattern.png')
        else:
            piece = Image.new('RGB', (x_px, y_px), color=(255,255,102)) # тут будет создаваться желтый фон
        number = ImageDraw.Draw(piece)
        w, h = number.textsize(str(i), font=font)
        number.text(((bx_px-w)/2,(((by_px-h)/2)-10)), str(i), font=font, fill='white')
        #number.text((50,30),'additional')
        piece = ImageOps.expand(piece, border=1, fill='black')
    
        background.paste(piece, (x, y))
        x += piece.size[0]
        #print(piece.size)
        if x > x_px+2:
            x = 0
            y += piece.size[1]
    return background

def blocks_list(pages):
    images_list = []
    for i in range(1, pages*10, 10):
        images_list.append(badges_block(i))
    return images_list

def saver(images_list):
    if os.path.exists(BADGES_FOLDER) == False:
        os.makedirs(BADGES_FOLDER)
    filenames = []
    for element in images_list:
        enum = str((images_list.index(element))*10+1) + '_' + str((images_list.index(element))*10+10)
        filename = os.path.join(BADGES_FOLDER, 'badges_' + enum + '.png')
        filenames.append(filename)
        try:
            element.save(filename)
        except:
            os.mkdir(BADGES_FOLDER)
            element.save(filename)
    return filenames
    
def create_pdf_binder(files_list, open, remove):
    pdf.add_page()
    for file in files_list:
        pdf.image(file)
    pdf.output(pdf_name)
    if open == True:
        try:
            os.startfile(pdf_name) # if sys.platform == "win32":
        except:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, pdf_name])
    if remove == True:
        for element in files_list:
            os.remove(element)
    print(os.path.abspath(pdf_name))

# %% [markdown]
# ## Применение функций
# %% [markdown]
# ### Тестовое создание блока бейджей

# %%
badges_block(501)

# %% [markdown]
# ### Сохранение блоков бейджей в картинки

# %%
print(os.path.abspath(BADGES_FOLDER))
#print(os.path.join(os.getcwd(), BADGES_FOLDER))
print()

filenames_list = saver(blocks_list(7))
print(filenames_list)

# %% [markdown]
# ### Создание pdf-файла

# %%
create_pdf_binder(filenames_list, True, True)


# %%
end = time.time()
print('Время работы скрипта: ', round(end - start, 2), 'секунд')

# %% [markdown]
# Sources
# 
# 1. https://egorovegor.ru/python-image-to-pdf-convert/
# 2. https://stackoverflow.com/questions/65676937/function-to-make-grid-of-images/65695715
# 3. https://stackoverflow.com/questions/37921295/python-pil-image-make-3x3-grid-from-sequence-images
# 4. https://python-scripts.com/create-pdf-pyfpdf

