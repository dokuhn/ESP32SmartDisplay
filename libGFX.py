import time

import font_cfg


class gfx:

    ROWS    = 10  
    COLS    = 10 

    def __init__(self, NeoPixelInst, rows, cols):
        self.np    = NeoPixelInst
        self.ROWS  = rows
        self.COLS  = cols


    def drawPixel(self, x, y, color):
        self.np[ x + (y* self.COLS) ] = color


    def clearScreen(self):
        for i in range( self.ROWS * self.COLS):
            self.np[i] = (0,0,0)
        
        self.np.write()
        time.sleep_ms(10)    


    def drawLine(self, x0, y0, x1, y1, color):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if(steep):
            # swap points
            t = x0
            x0 = y0
            y0 = t

            t = x1
            x1 = y1
            y1 = t
        if(x0> x1):
            # swap points
            t = x0
            x0= x1
            x1 = t

            t = y0
            y0 = y1
            y1 = t


        dx = x1 - x0
        dy = abs(y1 - y0)
        
        err = dx / 2

        if(y0 < y1):
            ystep = 1
        else:
            ystep = -1

        yi = y0
        for xi in range(x0, x1 + 1):
            if(steep):
                self.drawPixel(yi, xi, color)
            else:
                self.drawPixel(xi, yi, color)
            err -= dy

            if(err < 0):
                yi += ystep
                err += dx


        self.np.write() 


    def drawRect(self, x, y, w, h, color):

        self.drawLine( x, y, x + w, y, color)
        self.drawLine( x + w, y, x + w, y + h, color)
        self.drawLine( x + w, y + h, x, y + h, color)
        self.drawLine( x, y + h, x, y, color)
       

    def drawCircle(self, x0, y0, r, color):

        f = 1 - r
        ddF_x = 1
        ddf_y = -2 * r

        x = 0
        y = r

        self.drawPixel(x0, y0 + r, color)
        self.drawPixel(x0, y0 - r, color)
        self.drawPixel(x0 + r, y0, color)
        self.drawPixel(x0 - r, y0, color)

        while(x < y):

            if(f >= 0):
                y -= 1
                ddf_y += 2
                f += ddf_y

            x += 1
            ddF_x += 2
            f += ddF_x

            self.drawPixel(x0 + x, y0 + y, color)
            self.drawPixel(x0 - x, y0 + y, color)
            self.drawPixel(x0 + x, y0 - y, color)
            self.drawPixel(x0 - x, y0 - y, color)
            self.drawPixel(x0 + y, y0 + x, color)
            self.drawPixel(x0 - y, y0 + x, color)
            self.drawPixel(x0 + y, y0 - x, color)
            self.drawPixel(x0 - y, y0 - x, color)

        self.np.write() 


    def drawChar(self, char, color):

        for i in range(5):
            line = font_cfg.font[ ord(char) ][i]

            for j in range(8):
                if(line & 1):
                    self.drawPixel(i, j, color)
                line = line >> 1

        self.np.write()         
        
