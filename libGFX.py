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
        self.np.write()


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
            self.writeFastVLine(x0, y0, y1 - y0 + 1, color)
        elif (y0 == y1):
            if (x0 > x1):
                # swap points
                t = x0
                x0 = x1
                x1 = t                
            self.writeFastHLine(x0, y0, x1 - x0 + 1, color)
        else:
            self.drawLine(x0, y0, x1, y1, color)
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

    def drawfillCircleHelper(self, x0, y0, r, corners, delta, color):
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        px = x
        py = y

        delta += 1     # Avoid some +1's in the loop

        while(x < y):
            if (f >= 0):
                y -= 1
                ddF_y += 2
                f += ddF_y
            
            x += 1
            ddF_x += 2
            f += ddF_x
            # These checks avoid double-drawing certain lines
            if (x < (y + 1)):
                if (corners & 1):
                    self.writeFastVLine(x0 + x, y0 - y, 2 * y + delta, color)
                if (corners & 2):
                    self.writeFastVLine(x0 - x, y0 - y, 2 * y + delta, color)
            if (y != py):
                if (corners & 1):
                    self.writeFastVLine(x0 + py, y0 - px, 2 * px + delta, color)
                if (corners & 2):
                    self.writeFastVLine(x0 - py, y0 - px, 2 * px + delta, color)
                py = y
            px = x


    def writefillCircleHelper(self, x0, y0, r, corners, delta, color):
        self.drawfillCircleHelper(self, x0, y0, r, corners, delta, color)
        self.np.write()


    def writefillRoundRect(self, x, y, w, h, r, color):
        max_radius = (w if (w < h) else h) / 2  # 1/2 minor axis

        if (r > max_radius):
            r = max_radius

        self.writeFillRect(x + r, y, w - 2 * r, h, color)

        self.drawfillCircleHelper(x + w - r - 1, y + r, r, 1, h - 2 * r - 1, color)
        self.drawfillCircleHelper(x + r, y + r, r, 2, h - 2 * r - 1, color)

        self.np.write()


    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color):

        self.drawLine(x0, y0, x1, y1, color)
        self.drawLine(x1, y1, x2, y2, color)
        self.drawLine(x2, y2, x0, y0, color)


    def writeTriangle(self, x0, y0, x1, y1, x2, y2, color):
        self.drawTriangle(x0, y0, x1, y1, x2, y2, color)
        self.np.write()


    def drawfillTriangle(self, x0, y0, x1, y1, x2, y2, color):

        # Sort coordinates by Y order (y2 >= y1 >= y0)
        if(y0 > y1):
            t = y0
            y0 = y1
            y1 = t
            t = x0
            x0 = x1
            x1 = t
        if(y1 > y2):
            t = y1
            y1 = y2
            y2 = t
            t = x1
            x1 = x2
            x2 = x1
        if(y0 > y1):
            t = y0
            y0 = y1
            y1 = t
            t = x0
            x0 = x1
            x1 = t
            
        
        if(y0 == y2): # Handle awkward all-on-same-line case as its own thing
            a = x0
            b = x0
            if (x1 < a):
                a = x1
            elif (x1 > b):
                b = x1
            if (x2 < a):
                a = x2
            elif(x2 > b):
                b = x2
            self.drawFastHLine(a, y0, b - a + 1, color)
        
            return

        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa = 0
        sb = 0


        # For upper part of triangle, find scanline crossings for segments
        # 0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1
        # is included here (and second loop will be skipped, avoiding a /0
        # error there), otherwise scanline y1 is skipped here and handled
        # in the second loop...which also avoids a /0 error here if y0=y1
        # (flat-topped triangle).
        if(y1 == y2):
            last = y1 # Include y1 scanline
        else:
            last = y1 - 1 # Skip it

        for y in range(y0, last):
            a = int(x0 + sa / dy01)
            b = int(x0 + sb / dy02)
            sa += dx01
            sb += dx02
            ## longhand:
            # a = x0 + (x1 - x0) * (y - y0) / (y1 - y0)
            # b = x0 + (x2 - x0) * (y - y0) / (y2 - y0)
            if(a > b):
                t = a
                a = b
                b = t
            self.drawFastHLine(a, y, b - a + 1, color)


        # For lower part of triangle, find scanline crossings for segments
        # 0-2 and 1-2.  This loop is skipped if y1=y2.
        sa = int(dx12 * (y - y1))
        sb = int(dx02 * (y - y0))
        for y in range(last, y2):
            a = x1 + sa / dy12
            b = x0 + sb / dy02
            sa += dx12
            sb += dx02
            ## longhand:
            # a = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
            # b = x0 + (x2 - x0) * (y - y0) / (y2 - y0)
            if(a > b):
                t = a
                a = b
                b = t
            self.drawFastHLine(a, y, b - a + 1, color)
        



    def drawChar(self, char, color):

        for i in range(5):
            line = font_cfg.font[ ord(char) ][i]

            for j in range(8):
                if(line & 1):
                    self.drawPixel(i, j, color)
                line = line >> 1

        self.np.write()        


        
