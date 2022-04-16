from os import walk
import pygame

def import_folder(path):

    surfaces =[]

    for _,__,img_file in walk(path):
        for image in img_file:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surfaces.append(image_surf)

    return surfaces


