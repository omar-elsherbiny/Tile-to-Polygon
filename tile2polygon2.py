#Imports
import pygame as pyg
from random import randint
from classes import *

pyg.init()

#Globals
TILE_WIDTH=40
SCREEN_HEIGHT = bas_rnd(520,TILE_WIDTH)
SCREEN_WIDTH = bas_rnd(640,TILE_WIDTH)
SCREEN = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pyg.font.Font("freesansbold.ttf", 20)

#Main
def main():
    clock = pyg.time.Clock()
    pols=[Polygon(80,80,TILE_WIDTH)]
    pyg.display.set_caption('Tile-map to polygons demo      ||Omar el sherbiny||')
    print(f'\n{TILE_WIDTH=}, ({SCREEN_HEIGHT=}, {SCREEN_WIDTH=})')
    #MAIN LOOP
    run = True
    while run:
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                pyg.quit()
                exit()
            if event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = pyg.mouse.get_pos()
                    mx, my=bas_rnd(mx,TILE_WIDTH),bas_rnd(my,TILE_WIDTH)
                    nearest_pol=get_nearest_pol(pols,(mx,my),TILE_WIDTH)
                    if nearest_pol[1]>TILE_WIDTH:
                        pols.append(Polygon(mx,my,TILE_WIDTH,(randint(0,255),randint(0,255),randint(0,255))))
                    elif nearest_pol[1]>0:
                        if len(nearest_pol[0])>1:
                            diff=0
                            for pol_ind in nearest_pol[0][1:]:
                                for tile in pols[pol_ind-diff].tiles:
                                    pols[nearest_pol[0][0]].add(tile.xy[0],tile.xy[1])
                                pols.pop(pol_ind-diff)
                                diff+=1
                        pols[nearest_pol[0][0]].add(mx,my)
                if event.button == 3:
                    mx, my = pyg.mouse.get_pos()
                    mx, my=bas_rnd(mx,TILE_WIDTH),bas_rnd(my,TILE_WIDTH)
                    nearest_pol=get_nearest_pol(pols,(mx,my),TILE_WIDTH)
                    if nearest_pol[1]<=TILE_WIDTH:
                        pols[nearest_pol[0][0]].delete(mx,my)
                        if len(pols[nearest_pol[0][0]].tiles)==0:
                            pols.pop(nearest_pol[0][0])
        SCREEN.fill((25, 25, 25))
        for pol in pols:
            pol.update()
            pol.draw(SCREEN)
            pol.draw_faces(SCREEN)
            pol.draw_vertices(SCREEN,True)

        clock.tick(30)
        pyg.display.update()

main()