# -*- coding: utf-8 -*-

from os.path import splitext, split, join
import Image


def add_file_termination(filename, termination):
    '''
    Adiciona um sufixo ao nome de um arquivo

    Exemplo de uso:
     - ``filename``: /home/soda/imagem.jpg
     - ``termination``: _min
     -> vai ficar: /home/soda/imagem_min.jpg

    '''
    path, file_name = split(filename)
    file_name, pic_ext = splitext(file_name)
    return join(path, file_name + termination + pic_ext)

def crop_center(img, size):
    '''
    Corta a imagem passada no centro, com as dimensões passadas
    '''
    width, height = size
    if img.size[0] <= width or img.size[1] <= height:
        img.thumbnail( (width, height), Image.ANTIALIAS )
        return img
    top_left     = (img.size[0] - width) / 2
    top_right    = (img.size[1] - height) / 2
    bottom_left  = top_left + width
    bottom_right = top_right + height
    new_img = img.crop( (top_left, top_right, bottom_left, bottom_right) )
    return new_img

