from Fractal import Fractal
import math
import gtk

class Mandelbrot (Fractal):
    
    z0 = (0.0, 0.0)
    width = 600
    height = 600
    cPlaneArea = (-1.5, -1.5, 1.5, 1.5)
    cPlaneAreaHistory = []
    
    def __init__(self):
        Fractal.__init__(self)
        self.gladefile = "fractals/MandelbrotFractal.glade"
        self.wTree = gtk.glade.XML(self.gladefile)
        return
    
    def getControlPanel(self):
        return self.wTree.get_widget('controlPanel')
    
    def cPlus(self, c1, c2):
        c = ((c1[0] + c2[0]), (c1[1] + c2[1]))
        return c
    
    def cMinus(self, c1, c2):
        c = ((c1[0] - c2[0]), (c1[1] - c2[1]))
        return c
    
    def cMulti(self, c1, c2):
        re = c1[0]*c2[0] - c1[1]*c2[1]
        im = c1[1]*c2[0] + c1[0]*c2[1]
        return (re, im)
    
    def drawing(self):
        self.cleanAll()
        self.stopFlag = False
        for i in range(-self.width/2, self.width/2):
            for j in range(-self.height/2, self.height/2):
                # left-shift the image for 150 pixels
                c = (1.5 * (i+150)/(self.width/2), 1.5*j/(self.height/2))
                #print z
                k = 0
                z = self.z0
                for k in range(0, 128):
                    # check stop flag at beginning of each loop
                    if self.stopFlag == True:
                        self.stopFlag = False
                        return
                    z = self.cMinus(self.cMulti(z, z), c)
                    if (z[0]*z[0] + z[1]*z[1]) > 64.0:
                        break
                if True:
                    color = gtk.gdk.Color(red=1.0-1.0*(k/16), green=1.0-1.0*((k%16)/4), blue=1.0-1.0*(k%4))
                    #color = gtk.gdk.Color(red=1.0*k/128, green=(1.0-1.0*k/128), blue=(1.0 - 1.0*k/128))
                    self.drawPointColor(i, j, color)
        return
    
    def getName(self):
        return "Mandelbrot"
    
    def zoomIn(self, x0, y0, x1, y1):
        Fractal.zoomIn(self, x0, y0, x1, y1)
        # save current c area
        self.cPlaneAreaHistory.append(self.cPlaneArea)
        # calculate new c area (a0, b0, a1, b1)
        a0 = (self.cPlaneArea[2] - self.cPlaneArea[0]) / 600 * (x0 - (-300)) + self.cPlaneArea[0]
        b0 = (self.cPlaneArea[3] - self.cPlaneArea[1]) / 600 * (y0 - (-300)) + self.cPlaneArea[1]
        a1 = (self.cPlaneArea[2] - self.cPlaneArea[0]) / 600 * (x1 - (-300)) + self.cPlaneArea[0]
        b1 = (self.cPlaneArea[3] - self.cPlaneArea[1]) / 600 * (y1 - (-300)) + self.cPlaneArea[1]
        self.cPlaneArea = (a0, b0, a1, b1)
        print self.cPlaneArea
        return True
    
    def zoomOut(self):
        if len(self.cPlaneAreaHistory) == 0:
            return False
        Fractal.zoomOut(self)
        self.cPlaneArea = self.cPlaneAreaHistory.pop()
        return True