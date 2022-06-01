from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
import os
from pathlib import Path
from itertools import cycle, chain
import time

def get_pictures(base_dir: str):
    image_paths = []
    dirs = os.listdir(base_dir)
    dirs.sort()
    for d in dirs:
        directory = os.path.join(base_dir, d)
        files = os.listdir(directory)
        files.sort()
        for f in files:
            filename = os.path.join(directory, f)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.sld')):
                image_paths.append(filename)

    texts = sum(name.lower().endswith('.sld') for name in image_paths)
    print(f'{len(image_paths) - texts} images found')
    print(f'{texts} only-text slides found')
    time.sleep(1)
    return iter(image_paths)

class App(tk.Tk):
    def __init__(self, base_dir: str, delay_photo: int, delay_text: int):
        tk.Tk.__init__(self)
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.overrideredirect(1)
        self.geometry("%dx%d" % (self.w, self.h))
        self.delay_photo = delay_photo
        self.delay_text = delay_text
        self.pictures = get_pictures(base_dir)
        self.configure(background='grey13')

        self.picture_display = tk.Label(self, bg='black')
        self.text = tk.Label(self, font=("Ericsson Hilda", 20), bg='grey13', fg='white')

        self.picture_display.pack()
        self.text.pack(expand=True, fill=tk.BOTH)


    def show_slides(self):
        x = next(self.pictures)
        self.show_image(x)


    def show_image(self, x):
        text = self.get_text(x)
        self.picture_display.destroy()
        self.text.destroy()

        if not x.endswith('.sld'):
            original_image = Image.open(x)

            h = self.h if text is None else self.h - 100

            ratio = min(self.w/original_image.width, h/original_image.height)
            size = int(original_image.width * ratio + 0.5), int(original_image.height * ratio + 0.5)
            fg= original_image.resize(size, Image.ANTIALIAS)
            bg = original_image.resize((self.w, h), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(10))
            bg.paste(fg, (int((self.w - size[0]) / 2 - 0.5),int((h - size[1]) / 2 - 0.5)))
            new_img = ImageTk.PhotoImage(bg)
            self.picture_display = tk.Label(self, bg='grey13', image=new_img)
            self.picture_display.image = new_img
            self.text = tk.Label(self, font=("Ericsson Hilda", 40), bg='grey13', fg='mint cream', text=text)
            self.picture_display.pack()
            self.text.pack(expand=True, fill=tk.BOTH)
            self.after(self.delay_photo, self.show_slides)

        else:
            self.text = tk.Label(self, font=("Ericsson Hilda", 100), bg='grey13', fg='goldenrod3', text=text,
                                 wraplength=self.w, justify='left')
            self.text.pack(expand=True, fill=tk.BOTH)
            self.after(self.delay_text, self.show_slides)

        self.text.config(text=text)


    def get_text(self, x):
        text_file = x + '.txt' if not x.endswith('.sld') else x
        if os.path.exists(text_file):
            with open(text_file, encoding='utf-8') as f:
                return f.read()


delay_photo = 1500
delay_text = 2000
base_dir = '/route/to/pictures'
app = App(base_dir, delay_photo, delay_text)
app.show_slides()
app.mainloop()
