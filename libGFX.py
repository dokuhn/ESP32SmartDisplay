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


    def drawLine(self, point0, point1, color):
        steep = abs(point1['y'] - point0['y']) > abs(point1['x'] - point0['x'])
        if(steep):
            # swap points
            t = point0['x']
            point0['x'] = point0['y']
            point0['y'] = t

            t = point1['x']
            point1['x'] = point1['y']
            point1['y'] = t
        if(point0['x'] > point1['x']):
            # swap points
            t = point0['x']
            point0['x'] = point1['x']
            point1['x'] = t

            t = point0['y']
            point0['y'] = point1['y']
            point1['y'] = t


        dx = point1['x'] - point0['x']
        dy = abs(point1['y'] - point0['y'])
        
        err = dx / 2

        if(point0['y'] < point1['y']):
            ystep = 1
        else:
            ystep = -1

        yi = point0['y']
        for xi in range(point0['x'], point1['x'] + 1):
            if(steep):
                self.drawPixel(yi, xi, color)
            else:
                self.drawPixel(xi, yi, color)
            err -= dy

            if(err < 0):
                yi += ystep
                err += dx


        self.np.write() 


    def drawRect(self, point0, point1, color):

        self.drawLine({'x':point0['x'], 'y':point0['y']}, {'x':point1['x'], 'y':point0['y']}, color)
        self.drawLine({'x':point1['x'], 'y':point0['y']}, {'x':point1['x'], 'y':point1['y']}, color)
        self.drawLine({'x':point1['x'], 'y':point1['y']}, {'x':point0['x'], 'y':point1['y']}, color)
        self.drawLine({'x':point0['x'], 'y':point1['y']}, {'x':point0['x'], 'y':point0['y']}, color)



    
    def drawChar(self, char, color):

        for i in range(5):
            line = font_cfg.font[ ord(char) ][i]

            for j in range(8):
                if(line & 1):
                    self.drawPixel(i, j, color)
                line = line >> 1

        self.np.write()         
        
