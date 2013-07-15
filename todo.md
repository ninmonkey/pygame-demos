todo / roadmap
============

@property:
    font (name)
    	first abs name; then abs(match_font()) ; then None;
        font.match_font('bitstreamverasans') => Vera.ttf

@font_size.setter
	exception written bad?

TextWall._calc_offset
	self.rect not set properly after calc. some how rect is continuing
change font

TextWall._render() 
	only call _calc_offset if needed

move loaded fonts to module level

TextLineFPS
text-list
text-wall (auto-wraps container)
	arg bounding Rect() , None=Screen.rect
		optional scroll offset

global font data (duplicate data in each line atm)

text-wall demo follow mouse, to display auto-wrap

parse_text() allow iteratable vs "\n"
split into two demos?

move logs to 'logging'
