import time

import font_cfg


class gfx:

    ROWS    = 10  
    COLS    = 10 

    def __init__(self, NeoPixelInst, rows, cols):
        self.np    = NeoPixelInst
        self.ROWS  = rows
        self.COLS  = cols


    def writePixel(self, x, y, color):
        self.drawPixel(x, y, color)
        selp.np.write()


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

    def drawFastVLine(self, x, y, h, color):
        self.drawLine(x, y, x, y + h - 1, color)

    def drawFastHLine(self, x, y, w, color):
        self.drawLine(x, y, x + w - 1, y, color)


    def writeFastVLine(self, x, y, h, color):
        self.drawLine(x, y, x, y + h - 1, color)
        self.np.write()
        

    def writeFastHLine(self, x, y, w, color):
        self.drawLine(x, y, x + w - 1, y, color)
        self.np.write()
        

    def writeLine(self, x0, y0, x1, y1, color):

        if (x0 == x1):
            if (y0 > y1):
                # swap points
                t = y0
                y0 = y1
                y1 = t
            self.writeFastVLine(x0, y0, y1 - y0 + 1, color);
        elif (y0 == y1):
            if (x0 > x1):
                # swap points
                t = x0
                x0 = x1
                x1 = t                
            self.writeFastHLine(x0, y0, x1 - x0 + 1, color);
        else:
            self.drawLine(x0, y0, x1, y1, color);
            self.np.write()

        


    def drawRect(self, x, y, w, h, color):

        self.writeFastHLine(x, y, w, color)
        self.writeFastHLine(x, y + h - 1, w, color)
        self.writeFastVLine(x, y, h, color)
        self.writeFastVLine(x + w - 1, y, h, color)
       
    def writeRect(self, x, y, w, h, color):
        self.drawRect(x, y, w, h, color)
        self.np.write()

    def writeFillRect(self, x, y, w, h, color):
        for xi in range(x, x + w):
            self.writeFastVLine(xi, y, h, color)


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

 
    def writeCircle(self, x0, y0, r, color):
        self.drawCircle(x0, y0, r, color)
        self.np.write()

    def drawCircleHelper(self, x0, y0, r, cornername, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r

        while(x < y):
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y
            
            x += 1
            ddF_x += 2
            f += ddF_x
            if (cornername & 0x4):
                self.drawPixel(x0 + x, y0 + y, color)
                self.drawPixel(x0 + y, y0 + x, color)
            if (cornername & 0x2):
                self.drawPixel(x0 + x, y0 - y, color)
                self.drawPixel(x0 + y, y0 - x, color)
            if (cornername & 0x8):
                self.drawPixel(x0 - y, y0 + x, color)
                self.drawPixel(x0 - x, y0 + y, color)
            if (cornername & 0x1):
                self.drawPixel(x0 - y, y0 - x, color)
                self.drawPixel(x0 - x, y0 - y, color)
            

    def writeCircleHelper(self, x0, y0, r, cornername, color):
        self.drawCircleHelper(x0, y0, r, cornername, color)
        self.np.write()

    def drawChar(self, char, color):

        for i in range(5):
            line = font_cfg.font[ ord(char) ][i]

            for j in range(8):
                if(line & 1):
                    self.drawPixel(i, j, color)
                line = line >> 1

        self.np.write()         
        
