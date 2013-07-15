from __future__ import print_function, division
import pygame
from pygame.color import THECOLORS
# I don't know the convinent way to import key constants
from pygame.locals import *
"""
@author: Jacob bolton (2013/07/06)
@copyright: boilerplate. Use the code for anything.
@version: 1.0

"""

debug = True

class TextLine(object):
    # Manages drawing and caching of a single line of text
    # properties will auto-toggle dirty bool as needed
    """
    properties:
        font, font_size:    change loaded font
        aa: toggle antialiasing
        rect:   render Rect()
        color_fg:   color of text
        color_bg:   None or Color()

        If background is going to be solid color, you can render faster by
        setting a color_bg to blend AA to.
    """

    def __init__(self, font=None, size=16, text="Hi world", color_fg=None):
        self.font_name = font
        self.font_size = size
        self.color_bg = None
        if color_fg is None:
            self.color_fg = Color("white")
        else:
            self.color_fg = color_fg

        self._aa = True
        self._text = text
        self._load_font()
        self.screen = pygame.display.get_surface()

        self.dirty = True
        self.image = None
        self.rect = Rect(0,0,0,0)
        self._render()

    def _load_font(self):
        # (re)loads font, fallsback to None.
        try:
            self.font = pygame.font.Font(self.font_name, self.font_size)
        except IOError:
            self.font_name = None
            self.font = pygame.font.Font(self.font_name, self.font_size)

    def _render(self):
        # create cache'd surface        
        if debug: print('_render()')

        self.dirty = False
        if not self.color_bg:
            self.image = self.font.render(self._text, self.aa, self.color_fg)
        else:
            self.image = self.font.render(self._text, self.aa, self.color_fg, self.color_bg)
        self.rect.size = self.image.get_rect().size

    def draw(self, dest=None):
        # blit using cache'd surface
        if dest is None: dest = self.screen

        if self.dirty or self.image is None: self._render()
        dest.blit(self.image, self.rect)

    #def size(self):
        # Rect() containing required render space
        #return self.font.size(self.text)

    @property
    def font_size(self):
        # Modify font size
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self.dirty = True
        self._font_size = size
        self._load_font()

    @property
    def text(self):
        # Modify text
        return self._text

    @text.setter
    def text(self, text):
        self.dirty = True
        self._text = text

    @property
    def aa(self):
        # Modify antialiasing
        return self._aa

    @aa.setter
    def aa(self, aa):
        self.dirty = True
        self._aa = aa


class TextWall(object):
    # manage multiple TextLine()'s of text / paragraphs.
    """
    properties:
        font, font_size:    change loaded font
        rect: offset and size as Rect()
        aa: toggle antialiasing
        rect:   render Rect()
        color_fg:   color of text
        color_bg:   None or Color()

        If background is going to be solid color, you can render faster by
        setting a color_bg to blend AA to.
    """

    def __init__(self, font=None, size=16):        
        self.font = font
        self.font_size = size
        self.text_lines = []
        self.aa = True
        self.rect = Rect(0,0,1,1)

        self.screen = pygame.display.get_surface()
        self.dirty = True
        self.text = "Hello\nWorld!"        
        
        self._render()

    def _render(self):
        # create cache'd surface
        self.dirty = False
        self.text_lines = [ TextLine(self.font, self.font_size, line) for line in self._text_parsed ]
        for t in self.text_lines:
            t.aa = self.aa
            t.font_size = self.font_size
        self._calc_offset()

    def _calc_offset(self):
        # offsets for each line        
        #full = Rect(self.rect)
        full = self.rect.copy()
        
        prev = Rect(self.rect)
        for t in self.text_lines:            
            print("  line = ",full)
            t.rect.topleft = prev.bottomleft
            prev = t.rect.copy()
            full = full.union(t.rect)

        # verify containment        
        print("full.size=", full.size)
        #print("self.size=", self.rect.size)
        
        #bug: this line causes full to increase height every loop
        #self.rect = full.copy()

        if debug: pygame.draw.rect(self.screen, Color("pink"), full, 1)
        if debug: pygame.draw.rect(self.screen, Color("green"), self.rect, 1)


    def parse_text(self, text):
        # convert string with "\n" to drawn text        
        self.dirty = True        
        self._text_raw = text
        self._text_parsed = self._text_raw.split("\n")
        self._render()

    def draw(self, dest=None):
        # draw to surface     
        self._calc_offset()   
        if dest is None: dest = self.screen
        if self.dirty or not self.text_lines: self._render()
        for text in self.text_lines: text.draw(dest)

    @property
    def font_size(self):
        # modify font size
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        try:
            if self._font_size == size: return
        except AttributeError:
            self._font_size = size

        self.dirty = True
        self._font_size = size

    @property
    def text(self):
        # Modify and parse new text
        return self._text

    @text.setter
    def text(self, text):
        try:
            if self._text_raw == text: return
        except AttributeError:
            self._text_raw = text

        self.dirty = True
        self._text_raw = text
        self.parse_text(self._text_raw)

    @property
    def aa(self):
        # Modify antialiasing
        return self._aa

    @aa.setter
    def aa(self, aa):
        try:
            if self._aa == aa: return
        except AttributeError:
            self._aa = aa

        self.dirty = True
        self._aa = aa    

class TextWrap(object):
    # probably will replace TextWall completely.
    def __init__(self, font=None, size=16, rect_wrap=None, text="", color_fg=None):
        self.screen = pygame.display.get_surface()
        if rect_wrap is None:
            self.rect_wrap = self.screen.get_rect()
        else:
            self.rect_wrap = rect_wrap

        if color_fg is None:
            self.color_fg = Color("white")
        else:
            self.color_fg = color_fg

    def parse_text(self, text):
        pass

    def draw(self):
        return
        if debug: pygame.draw.rect(self.screen, Color("darkred"), self.rect_wrap, 1)