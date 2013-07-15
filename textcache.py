from __future__ import print_function, division
import pygame
from pygame.color import THECOLORS
# I don't know the convinent way to import key constants
from pygame.locals import *
"""
@author: Jacob bolton (2013/07/06)
@copyright: boilerplate. Use the code for anything.
@about: started as cleaned up demo for http://www.reddit.com/r/pygame/
@version: 1.0

== @todo ==


question:
    how to comment properties

@property:
    font (name)
        font.match_font('bitstreamverasans') => Vera.ttf

change font

text-list
text-wall (auto-wraps container)
global font data (duplicate data in each line atm)

text-wall demo follow mouse, to display auto-wrap

"""

debug = False


class TextLine(object):
    # Manage drawing and caching of a single line of text
    # properties auto-toggle dirty bool as needed
    """properties:
    font, font_size:    change loaded font
    aa: toggle antialiasing
    rect:   render Rect()
    color_fg:   color of text
    color_bg:   None or Color()
        If background will be a solid color, you can render faster by setting color_bg

    """

    def __init__(self, font=None, size=16, text="Hi world"):
        self.font_name = font
        self.font_size = size
        self.color_fg = Color("white")
        self.color_bg = None

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
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        self.dirty = True
        self._font_size = size
        self._load_font()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self.dirty = True
        self._text = text

    @property
    def aa(self):
        return self._aa

    @aa.setter
    def aa(self, aa):
        self.dirty = True
        self._aa = aa


class TextWall(object):
    # manage multiple TextLine()'s of text / paragraphs.
    def __init__(self, font=None, size=16):
        self.font = font
        self.font_size = size
        self.text_lines = []
        self.aa = True
        self.offset = Rect(20,20,1,1)

        self.screen = pygame.display.get_surface()
        self.dirty = True
        
        #self._text_raw = "Hello\nWorld!"        
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
        prev = self.offset
        for t in self.text_lines:            
            t.rect.topleft = prev.left, prev.bottom
            prev = t.rect

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
        return self._font_size

    @font_size.setter
    def font_size(self, size):
        #todo: I feel the except/else isn't written well?    
        try:
            if self._font_size == size: return
        except AttributeError:
            self._font_size = size

        self.dirty = True
        self._font_size = size

    @property
    def text(self):
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
    def __init__(self):
        pass