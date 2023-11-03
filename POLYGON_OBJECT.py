import pygame as pyg
class Rect:
    def __init__(self,x,y,size):
        self.xy=(x,y)
        self.xsy=(x+size,y)
        self.xsys=(x+size,y+size)
        self.xys=(x,y+size)
        self.t,self.b,self.r,self.l=True,True,True,True
        self.tr,self.tl,self.br,self.bl=False,False,False,False
    def points(self):
        return self.xy,self.xsy,self.xsys,self.xys
    def faces(self):
        return self.t,self.b,self.r,self.l
    def corners(self):
        return self.tr,self.tl,self.br,self.bl
class Polygon:
    def __init__(self, x, y, size=40, color=(253,2,45)):
        self.tiles=[Rect(x,y,size)]
        self.vertices=self.tiles[0].points()
        self.average=(int((2*x+size)/2), int((2*y+size)/2))
        self.size=size
        self.col=color
    def _find_neighbours(self,cid):
        for tile in self.tiles:
            dx,dy=tile.xy[0]-cid[0],tile.xy[1]-cid[1]
            if dx>self.size or dx<-self.size or dy>self.size or dy<-self.size:
                continue
            elif dx!=0 and dy!=0:
                ind=self.tiles.index([x for x in self.tiles if x.xy == tile.xy][0])
                if dx<0 and dy<0:
                    self.tiles[ind].br=True
                    self.tiles[-1].tl=True
                elif dx>0 and dy>0:
                    self.tiles[ind].tl=True
                    self.tiles[-1].br=True
                elif dx<0 and dy>0:
                    self.tiles[ind].tr=True
                    self.tiles[-1].bl=True
                elif dx>0 and dy<0:
                    self.tiles[ind].bl=True
                    self.tiles[-1].tr=True
            elif dx==0 and dy==0:
                continue
            else:
                ind=self.tiles.index([x for x in self.tiles if x.xy == tile.xy][0])
                if dx<0:
                    self.tiles[ind].r=False
                    self.tiles[-1].l=False
                elif dx>0:
                    self.tiles[ind].l=False
                    self.tiles[-1].r=False
                elif dy<0:
                    self.tiles[ind].b=False
                    self.tiles[-1].t=False
                elif dy>0:
                    self.tiles[ind].t=False
                    self.tiles[-1].b=False
    def _delete_neighbours(self,cid):
        for tile in self.tiles:
            dx,dy=tile.xy[0]-cid[0],tile.xy[1]-cid[1]
            if dx>self.size or dx<-self.size or dy>self.size or dy<-self.size:
                continue
            elif dx!=0 and dy!=0:
                ind=self.tiles.index([x for x in self.tiles if x.xy == tile.xy][0])
                if dx<0 and dy<0:
                    self.tiles[ind].br=False
                elif dx>0 and dy>0:
                    self.tiles[ind].tl=False
                elif dx<0 and dy>0:
                    self.tiles[ind].tr=False
                elif dx>0 and dy<0:
                    self.tiles[ind].bl=False
            elif dx==0 and dy==0:
                continue
            else:
                ind=self.tiles.index([x for x in self.tiles if x.xy == tile.xy][0])
                if dx<0:
                    self.tiles[ind].r=True
                elif dx>0:
                    self.tiles[ind].l=True
                elif dy<0:
                    self.tiles[ind].b=True
                elif dy>0:
                    self.tiles[ind].t=True

    def update(self):
        #updating verticies according to faces
        nv=[]
        for tile in self.tiles:
            f=tile.faces()#      top bottom right left
            c=tile.corners()#      tr tl br bl
            if f[0] and not f[2] and not f[3]:
                if c[0]:
                    nv.append(tile.xsy)
                if c[1]:
                    nv.append(tile.xy)
            elif f[0] and not f[2]:
                if c[0]:
                    nv.append(tile.xsy)
                nv.append(tile.xy)
            elif f[0] and not f[3]:
                if c[1]:
                    nv.append(tile.xy)
                nv.append(tile.xsy)
            elif f[0]:
                nv.append(tile.xy)
                nv.append(tile.xsy)
            if f[1] and not f[2] and not f[3]:
                if c[2]:
                    nv.append(tile.xsys)
                if c[3]:
                    nv.append(tile.xys)
            elif f[1] and not f[2]:
                if c[2]:
                    nv.append(tile.xsys)
                nv.append(tile.xys)
            elif f[1] and not f[3]:
                if c[3]:
                    nv.append(tile.xys)
                nv.append(tile.xsys)
            elif f[1]:
                nv.append(tile.xys)
                nv.append(tile.xsys)
        self.vertices=nv
        #removing duplicates
        self.vertices=list(dict.fromkeys(self.vertices))
        #updating average
        x_avg,y_avg=0,0
        for vertix in self.vertices:
            x_avg+=vertix[0]
            y_avg+=vertix[1]
        x_avg/=len(self.vertices)
        y_avg/=len(self.vertices)
        self.average=(int(x_avg),int(y_avg))

    def add(self, x, y):
        self.tiles.append(Rect(x,y,self.size))
        self._find_neighbours((x,y))
    def delete(self, x, y):
        search=[z for z in self.tiles if z.xy == (x,y)]
        if len(search)!=0:
            self.tiles.pop(self.tiles.index(search[0]))
        self._delete_neighbours((x,y))
    def draw(self, screen):
        for tile in self.tiles:
            pyg.draw.polygon(screen,self.col,tile.points())
    def draw_vertices(self, screen,avg=False):
        for vertix in self.vertices:
            pyg.draw.circle(screen,(255,255,255),vertix,3)
        inverse=(255-self.col[0],255-self.col[1],255-self.col[2])
        if avg:
            pyg.draw.circle(screen,inverse,self.average,5)
    def draw_faces(self, screen):
        for tile in self.tiles:
            f=tile.faces()
            if f[0]:
                pyg.draw.line(screen,(255,170,0),tile.xy,tile.xsy,3)
            if f[1]:
                pyg.draw.line(screen,(255,170,0),tile.xys,tile.xsys,3)
            if f[2]:
                pyg.draw.line(screen,(255,170,0),tile.xsy,tile.xsys,3)
            if f[3]:
                pyg.draw.line(screen,(255,170,0),tile.xy,tile.xys,3)
