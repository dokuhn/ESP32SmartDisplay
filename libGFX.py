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


    
    def drawChar(self, char, color):

        for i in range(5):
            line = font_cfg.font[ ord(char) ][i]

            for j in range(8):
                if(line & 1):
                    self.drawPixel(i, j, color)
                line = line >> 1

        self.np.write()         
        
