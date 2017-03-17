# Embedded file name: scripts/common/Lib/curses/textpad.py
"""Simple textbox editing widget with Emacs-like keybindings."""
import curses
import curses.ascii

def rectangle(win, uly, ulx, lry, lrx):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    win.vline(uly + 1, ulx, curses.ACS_VLINE, lry - uly - 1)
    win.hline(uly, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
    win.hline(lry, ulx + 1, curses.ACS_HLINE, lrx - ulx - 1)
    win.vline(uly + 1, lrx, curses.ACS_VLINE, lry - uly - 1)
    win.addch(uly, ulx, curses.ACS_ULCORNER)
    win.addch(uly, lrx, curses.ACS_URCORNER)
    win.addch(lry, lrx, curses.ACS_LRCORNER)
    win.addch(lry, ulx, curses.ACS_LLCORNER)


class Textbox:
    """Editing widget using the interior of a window object.
     Supports the following Emacs-like key bindings:
    
    Ctrl-A      Go to left edge of window.
    Ctrl-B      Cursor left, wrapping to previous line if appropriate.
    Ctrl-D      Delete character under cursor.
    Ctrl-E      Go to right edge (stripspaces off) or end of line (stripspaces on).
    Ctrl-F      Cursor right, wrapping to next line when appropriate.
    Ctrl-G      Terminate, returning the window contents.
    Ctrl-H      Delete character backward.
    Ctrl-J      Terminate if the window is 1 line, otherwise insert newline.
    Ctrl-K      If line is blank, delete it, otherwise clear to end of line.
    Ctrl-L      Refresh screen.
    Ctrl-N      Cursor down; move down one line.
    Ctrl-O      Insert a blank line at cursor location.
    Ctrl-P      Cursor up; move up one line.
    
    Move operations do nothing if the cursor is at an edge where the movement
    is not possible.  The following synonyms are supported where possible:
    
    KEY_LEFT = Ctrl-B, KEY_RIGHT = Ctrl-F, KEY_UP = Ctrl-P, KEY_DOWN = Ctrl-N
    KEY_BACKSPACE = Ctrl-h
    """

    def __init__(self, win, insert_mode = False):
        self.win = win
        self.insert_mode = insert_mode
        self.maxy, self.maxx = win.getmaxyx()
        self.maxy = self.maxy - 1
        self.maxx = self.maxx - 1
        self.stripspaces = 1
        self.lastcmd = None
        win.keypad(1)
        return

    def _end_of_line(self, y):
        """Go to the location of the first blank on the given line,
        returning the index of the last non-blank character."""
        last = self.maxx
        while True:
            if curses.ascii.ascii(self.win.inch(y, last)) != curses.ascii.SP:
                last = min(self.maxx, last + 1)
                break
            elif last == 0:
                break
            last = last - 1

        return last

    def _insert_printable_char(self, ch):
        y, x = self.win.getyx()
        if y < self.maxy or x < self.maxx:
            if self.insert_mode:
                oldch = self.win.inch()
            try:
                self.win.addch(ch)
            except curses.error:
                pass

            if self.insert_mode:
                backy, backx = self.win.getyx()
                if curses.ascii.isprint(oldch):
                    self._insert_printable_char(oldch)
                    self.win.move(backy, backx)

    def do_command(self, ch):
        """Process a single editing command."""
        y, x = self.win.getyx()
        self.lastcmd = ch
        if curses.ascii.isprint(ch):
            if y < self.maxy or x < self.maxx:
                self._insert_printable_char(ch)
        elif ch == curses.ascii.SOH:
            self.win.move(y, 0)
        elif ch in (curses.ascii.STX,
         curses.KEY_LEFT,
         curses.ascii.BS,
         curses.KEY_BACKSPACE):
            if x > 0:
                self.win.move(y, x - 1)
            elif y == 0:
                pass
            elif self.stripspaces:
                self.win.move(y - 1, self._end_of_line(y - 1))
            else:
                self.win.move(y - 1, self.maxx)
            if ch in (curses.ascii.BS, curses.KEY_BACKSPACE):
                self.win.delch()
        elif ch == curses.ascii.EOT:
            self.win.delch()
        elif ch == curses.ascii.ENQ:
            if self.stripspaces:
                self.win.move(y, self._end_of_line(y))
            else:
                self.win.move(y, self.maxx)
        elif ch in (curses.ascii.ACK, curses.KEY_RIGHT):
            if x < self.maxx:
                self.win.move(y, x + 1)
            elif y == self.maxy:
                pass
            else:
                self.win.move(y + 1, 0)
        else:
            if ch == curses.ascii.BEL:
                return 0
            if ch == curses.ascii.NL:
                if self.maxy == 0:
                    return 0
                if y < self.maxy:
                    self.win.move(y + 1, 0)
            elif ch == curses.ascii.VT:
                if x == 0 and self._end_of_line(y) == 0:
                    self.win.deleteln()
                else:
                    self.win.move(y, x)
                    self.win.clrtoeol()
            elif ch == curses.ascii.FF:
                self.win.refresh()
            elif ch in (curses.ascii.SO, curses.KEY_DOWN):
                if y < self.maxy:
                    self.win.move(y + 1, x)
                    if x > self._end_of_line(y + 1):
                        self.win.move(y + 1, self._end_of_line(y + 1))
            elif ch == curses.ascii.SI:
                self.win.insertln()
            elif ch in (curses.ascii.DLE, curses.KEY_UP):
                if y > 0:
                    self.win.move(y - 1, x)
                    if x > self._end_of_line(y - 1):
                        self.win.move(y - 1, self._end_of_line(y - 1))
        return 1

    def gather(self):
        """Collect and return the contents of the window."""
        result = ''
        for y in range(self.maxy + 1):
            self.win.move(y, 0)
            stop = self._end_of_line(y)
            if stop == 0 and self.stripspaces:
                continue
            for x in range(self.maxx + 1):
                if self.stripspaces and x > stop:
                    break
                result = result + chr(curses.ascii.ascii(self.win.inch(y, x)))

            if self.maxy > 0:
                result = result + '\n'

        return result

    def edit--- This code section failed: ---

0	SETUP_LOOP        '87'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'win'
9	LOAD_ATTR         'getch'
12	CALL_FUNCTION_0   None
15	STORE_FAST        'ch'

18	LOAD_FAST         'validate'
21	POP_JUMP_IF_FALSE '39'

24	LOAD_FAST         'validate'
27	LOAD_FAST         'ch'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'ch'
36	JUMP_FORWARD      '39'
39_0	COME_FROM         '36'

39	LOAD_FAST         'ch'
42	POP_JUMP_IF_TRUE  '51'

45	CONTINUE          '3'
48	JUMP_FORWARD      '51'
51_0	COME_FROM         '48'

51	LOAD_FAST         'self'
54	LOAD_ATTR         'do_command'
57	LOAD_FAST         'ch'
60	CALL_FUNCTION_1   None
63	POP_JUMP_IF_TRUE  '70'

66	BREAK_LOOP        None
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	LOAD_FAST         'self'
73	LOAD_ATTR         'win'
76	LOAD_ATTR         'refresh'
79	CALL_FUNCTION_0   None
82	POP_TOP           None
83	JUMP_BACK         '3'
86	POP_BLOCK         None
87_0	COME_FROM         '0'

87	LOAD_FAST         'self'
90	LOAD_ATTR         'gather'
93	CALL_FUNCTION_0   None
96	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 86


if __name__ == '__main__':

    def test_editbox(stdscr):
        ncols, nlines = (9, 4)
        uly, ulx = (15, 20)
        stdscr.addstr(uly - 2, ulx, 'Use Ctrl-G to end editing.')
        win = curses.newwin(nlines, ncols, uly, ulx)
        rectangle(stdscr, uly - 1, ulx - 1, uly + nlines, ulx + ncols)
        stdscr.refresh()
        return Textbox(win).edit()


    str = curses.wrapper(test_editbox)
    print 'Contents of text box:', repr(str)