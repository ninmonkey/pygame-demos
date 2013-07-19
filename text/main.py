from __future__ import print_function, division
import pygame
from pygame import *
from textcache import TextLine, TextWall, TextWrap

lorem = """TextWrap() Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque bibendum nulla non diam elementum, id hendrerit eros ornare. Nulla ornare varius mi, sollicitudin ullamcorper magna placerat et. Pellentesque vehicula pharetra velit sed rhoncus. Donec dignissim porttitor neque. Praesent hendrerit malesuada libero sed condimentum. Aliquam ipsum metus, dictum non porta in, venenatis sed libero. Suspendisse faucibus fringilla magna, et vestibulum ligula aliquam nec. Sed nibh erat, facilisis nec velit eget, ultrices faucibus sapien. Suspendisse turpis erat, auctor commodo interdum vel, fringilla in dui. Aliquam nec porttitor leo. Vestibulum magna erat, pellentesque nec scelerisque a, fringilla sed lectus. Maecenas lobortis ipsum at lacinia rhoncus. Etiam id ante et elit auctor tincidunt. Quisque tincidunt molestie mi, nec pellentesque diam venenatis et. Curabitur at lorem ut lacus interdum pretium non non massa.
Morbi adipiscing consequat eleifend. Nam mollis arcu eget volutpat scelerisque. Suspendisse eu odio leo. Cras ut ipsum et quam pretium ultricies. Donec mattis lobortis odio at luctus. Aliquam ut velit ut quam egestas feugiat in vitae sapien. Maecenas vitae gravida arcu, quis imperdiet augue. Mauris dolor leo, fermentum ut eros nec, tempus hendrerit odio. Morbi in ornare lacus. Nam congue pretium felis. Sed fermentum nisl eu ligula rhoncus, ac porttitor eros hendrerit. Nullam eu felis enim. Etiam semper rutrum mauris in sodales. Maecenas risus eros, bibendum eu quam ut, semper commodo nisi. Mauris nec consequat turpis.

Aliquam nec turpis quis nibh vehicula varius ut non neque. Ut in urna urna. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Sed sed leo sed tortor dapibus adipiscing non ac diam. Sed semper sodales placerat. Curabitur nec tortor vestibulum, varius turpis vel, ultrices tellus. Phasellus tristique pulvinar lacus quis tempor. Cras lorem justo, vestibulum non tortor vel, varius vestibulum dui. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Vivamus at arcu nibh. Integer congue magna ut felis cursus vehicula. Phasellus congue gravida mi sit amet dignissim. Nunc sollicitudin est ultrices imperdiet hendrerit. Phasellus facilisis gravida iaculis.
"""

class Game():
    # main game logic
    done = False

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode ((640,480))
        self.toggle_bg = True

        self.lines = TextLine(None, 60, "TextLine() Hi world!")
        
        self.text_wall = TextWall(None, 24)
        self.text_wall.parse_text("TextWall() Hello world!\nfoo\nbar!")
        self.text_wall.offset.topleft = (40,50)
        
        self.text_wrap = TextWrap(None, 26, Rect(150,50,300,300), "Hi world")
        self.text_wrap.parse_text(lorem)

    def loop(self):
        while not self.done:
            self.handle_events()
            self.draw()

    def draw(self):
        # clear and draw
        bg = Color("gray60") if self.toggle_bg else Color("gray20")

        self.screen.fill(bg)                
        self.lines.draw()
        self.text_wall.draw()
        self.text_wrap.draw()
        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            
            elif event.type == MOUSEMOTION:
                # resize TextWrap() boundry
                buttons = pygame.mouse.get_pressed()
                if buttons[0]:
                    self.text_wrap.rect_wrap.left += event.rel[0]
                    self.text_wrap.rect_wrap.top += event.rel[1]
                elif buttons[2]:
                    self.text_wrap.rect_wrap.width += event.rel[0]
                    self.text_wrap.rect_wrap.height += event.rel[1]

                #print(self.text_wrap.rect_wrap)
                #print(event.pos)

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: self.done = True
                if event.key == K_f:
                    self.text_wall.font = "arial.ttf"
                elif event.key == K_SPACE:
                    self.toggle_bg = not self.toggle_bg
                elif event.key == K_a:
                    self.lines.aa = not self.lines.aa
                    self.text_wall.aa = not self.text_wall.aa
                elif event.key == K_1: self.text_wrap.font_size -= 4
                elif event.key == K_2: self.text_wrap.font_size += 4
                elif event.key == K_3: self.text_wall.font_size -= 4
                elif event.key == K_4: self.text_wall.font_size += 4

if __name__ == "__main__":    
    print("""hotkeys:
    Space:  toggle BG color
    A:  toggle Anti-Alias
    1, 2:   increase/decrease font size
    3, 4:   increase/decrease text wall size
    """)

    g = Game()
    g.loop()