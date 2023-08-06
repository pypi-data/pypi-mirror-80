from appdirs import user_cache_dir
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
import sys
import string
import argparse
import ast

import importlib.resources as pkg_resources
from . import fonts

CACHE_PATH = user_cache_dir('aa-gen', 'kobayashi1757')
if not os.path.exists(CACHE_PATH) :
    os.makedirs(CACHE_PATH)

ASCII_TABLE_PATH = os.path.join(CACHE_PATH, 'ascii.txt')
CACHE_TABLE_PATH = os.path.join(CACHE_PATH, 'cache.txt')
with pkg_resources.path(fonts, 'Poppins-Regular.ttf') as p :
    FONT_PATH = str(p)

def make_ascii_table():
    def sampling(np_array):
        for i in range(0, 120, 24) :
            for j in range(0, 72, 24) :
                avg = np.average(np_array[i:i+24,j:j+24])
                yield 0 if avg > 220 else 1

    font = ImageFont.truetype(FONT_PATH, 120)

    im = Image.new(mode='L', size=(72, 120), color=255)
    im_draw = ImageDraw.Draw(im)
    with open(ASCII_TABLE_PATH, 'wt') as f :
        for char in (string.digits + string.punctuation + string.ascii_letters) :
            if char == ':' :
                continue
            im_draw.rectangle(xy=[(0, 0), (72, 120)], fill=255)
            im_draw.text(xy=(0, 0), text=char, fill=0, font=font)
            array = np.asarray(im)
            f.write(f'{char}:{tuple(sampling(array))}\n')
        f.write(f' :{tuple((0 for _ in range(15)))}\n')

def array_to_ascii(name, np_array):
    def load_table(path):
        table = {}
        with open(path) as f :
            for line in f :
                c, t = line.rstrip().split(':')
                table[ast.literal_eval(t)] = c
        return table

    ascii_table = load_table(ASCII_TABLE_PATH)
    cache_table = load_table(CACHE_TABLE_PATH)

    def sampling(np_array) :
        for i in range(0, 10, 2) :
            for j in range(0, 6, 2) :
                avg = np.average(np_array[i:i+2,j:j+2])
                yield 0 if avg > 220 else 1

    def best(sample):
        best_c, best_score = ' ', 15
        for t, c in ascii_table.items() :
            score = sum((abs(i-j) for i, j in zip(t, sample)))
            if score < best_score :
                best_c, best_score = c, score
        return best_c

    with open(CACHE_TABLE_PATH, 'at') as cache_file :
        height, width = np_array.shape
        for i in range(0, height, 10) :
            for j in range(0, width, 6) :
                sample = tuple(sampling(np_array[i:i+10,j:j+6]))
                if sample in ascii_table :
                    sys.stdout.write(ascii_table[sample])
                elif sample in cache_table :
                    sys.stdout.write(cache_table[sample])
                else :
                    best_c = best(sample)
                    cache_table[sample] = best_c
                    cache_file.write(f'{best_c}:{sample}\n')
                    sys.stdout.write(best_c)
            sys.stdout.write('\n')

def text_to_ascii(text: str, fontsize: int) :
    font = ImageFont.truetype(FONT_PATH, fontsize)
    text_width, text_height = font.getsize(text)
    if text_width % 6 != 0 :
        text_width += (6 - text_width % 6)
    if text_height % 10 != 0 :
        text_height += (10 - text_height % 10)

    with Image.new(mode='L', size=(text_width, text_height), color=255) as im :
        im_draw = ImageDraw.Draw(im)
        im_draw.text(xy=(0, 0), text=text, fill=0, font=font)
        array = np.asarray(im)
        array_to_ascii(text, array)

def main():
    parser = argparse.ArgumentParser(prog='Ascii Art Generator', description='Create ascii art based on input text.')
    parser.add_argument('-r', '--remake', action='store_true', default=False, help='Remake the bitmap_to_ascii_table')
    parser.add_argument('-c', '--clear', action='store_true', default=False, help='Clear the cache file')
    parser.add_argument('-t', '--text', help='Input text', dest='text')
    parser.add_argument('-s', '--size', type=int, nargs='?', default=110, help='fontsize (default 110)', dest='fontsize')

    args = parser.parse_args()

    if args.remake or not os.path.exists(ASCII_TABLE_PATH) :
        make_ascii_table()
    if args.clear :
        open(CACHE_TABLE_PATH, 'w').close()
    if args.text != None :
        text_to_ascii(args.text, args.fontsize)
