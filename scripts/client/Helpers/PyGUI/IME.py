# Embedded file name: scripts/client/Helpers/PyGUI/IME.py
import BigWorld
import GUI
import Math
import weakref
import Utils
from Utils import BlinkingCursor
from Utils import blinkingColourProvider
from Utils import getHPixelScalar, getVPixelScalar
from bwdebug import *
from debug_utils import LOG_DEBUG
ALWAYS_ON_TOP_Z = 0.01
BACKGROUND_COLOUR = (32, 32, 32, 255)
DEFAULT_FONT_NAME = 'default_small.font'
CANDIDATE_READING_FONT_NAME = 'ime_candidates.font'
SELECTED_CANDIDATE_BGCOLOUR = (220, 220, 220, 255)
SELECTED_CANDIDATE_FGCOLOUR = (16, 16, 16, 255)
IDEOGRAPHIC_SPACE = u'\u3000'
ATTR_INPUT = 0
ATTR_TARGET_CONVERTED = 1
ATTR_CONVERTED = 2
ATTR_TARGET_NOTCONVERTED = 3
ATTR_INPUT_ERROR = 4
ATTR_FIXEDCONVERTED = 5

def _attrToColours(attr):
    bgColour = None
    fgColour = None
    if attr in [ATTR_INPUT, ATTR_CONVERTED]:
        bgColour = (32, 32, 32, 255)
        fgColour = (255, 255, 255, 255)
    else:
        bgColour = (220, 220, 220, 255)
        fgColour = (16, 16, 16, 255)
    return (bgColour, fgColour)


def _compositionStringBlocks():
    """
            Returns the current composition string as a list of blocks of
            consecutive characters which share the same composition attributes.
    
            The return is a list of 2-tuples in the format (attr, unistring)
    """
    comp = BigWorld.ime.composition
    attr = BigWorld.ime.compositionAttr
    if len(comp) == 0:
        return []
    ret = []
    currentAttr = attr[0]
    currentBlock = u''
    for idx in range(len(comp)):
        if attr[idx] != currentAttr:
            ret.append((currentAttr, currentBlock))
            currentAttr = attr[idx]
            currentBlock = u''
        currentBlock += comp[idx]

    if len(currentBlock) > 0:
        ret.append((currentAttr, currentBlock))
    return ret


def _bgText(text, font, bgcolour, fgcolour):
    w = Utils.createTextWithBackground(text, font, bgcolour, fgcolour)
    w.colouriser = GUI.ColourShader()
    w.colouriser.colourProvider = bgcolour
    w.text.colouriser = GUI.ColourShader()
    w.text.colouriser.colourProvider = fgcolour
    return w


def logIMEEvent(event):
    LOG_DEBUG(str(event) + ':')
    LOG_DEBUG('   stateChanged=' + str(event.stateChanged) + " (value='" + str(BigWorld.ime.state) + "')")
    LOG_DEBUG('   candidatesVisibilityChanged=' + str(event.candidatesVisibilityChanged) + ' (value=' + str(BigWorld.ime.candidatesVisible) + ')')
    LOG_DEBUG('   candidatesChanged=' + str(event.candidatesChanged) + " (value='" + str(BigWorld.ime.candidates) + "', attrs=" + str(BigWorld.ime.compositionAttr) + ')')
    LOG_DEBUG('   selectedCandidateChanged=' + str(event.selectedCandidateChanged) + ' (value=' + str(BigWorld.ime.selectedCandidate) + ')')
    LOG_DEBUG('   compositionChanged=' + str(event.compositionChanged) + " (value='" + str(BigWorld.ime.composition) + "')")
    LOG_DEBUG('   compositionCursorPositionChanged=' + str(event.compositionCursorPositionChanged) + ' (value=' + str(BigWorld.ime.compositionCursorPosition) + ')')
    LOG_DEBUG('   readingVisibilityChanged=' + str(event.readingVisibilityChanged) + ' (value=' + str(BigWorld.ime.readingVisible) + ')')
    LOG_DEBUG('   readingChanged=' + str(event.readingChanged) + " (value='" + str(BigWorld.ime.reading) + "')")


class CompositionWindow(object):

    @staticmethod
    def create():
        component = GUI.Window(db.DBLogic.g_instance.getGUITexture('TX_MAP_MASK'))
        component.materialFX = 'BLEND'
        component.horizontalPositionMode = 'CLIP'
        component.horizontalAnchor = 'LEFT'
        component.verticalPositionMode = 'CLIP'
        component.verticalAnchor = 'CENTER'
        component.widthMode = 'PIXEL'
        component.heightMode = 'PIXEL'
        component.position.z = ALWAYS_ON_TOP_Z
        component.script = CompositionWindow(component)
        return component

    def __init__(self, component):
        component.visible = False
        component.script = self
        component.addChild(GUI.Text(), 'text')
        component.text.font = DEFAULT_FONT_NAME
        component.text.horizontalAnchor = 'LEFT'
        component.text.horizontalPositionMode = 'PIXEL'
        component.text.colouriser = GUI.ColourShader()
        component.text.colouriser.colourProvider = component.text.colour
        self.cursor = BlinkingCursor.create()
        component.addChild(self.cursor, 'cursor')
        self.cursor.script.enable(True)
        component.backgroundColouriser = GUI.ColourShader()
        component.backgroundColouriser.colourProvider = BACKGROUND_COLOUR
        self._firstTargetConvertedBlock = -1
        self.comp = weakref.proxy(component)

    def populate(self, fontName):
        if len(BigWorld.ime.composition) == 0:
            self.comp.visible = False
            return False
        if not len(BigWorld.ime.compositionAttr) == len(BigWorld.ime.composition):
            raise AssertionError
            for name, comp in self.comp.children:
                if name not in ('cursor', 'text'):
                    self.comp.delChild(comp)

            BigWorld.ime.language == 'KOREAN' and self._populateKorean(fontName)
        else:
            self._populateChineseJapanese(fontName)
        self.comp.visible = True
        return True

    def _populateChineseJapanese(self, fontName):
        compString = BigWorld.ime.composition
        self.comp.text.font = fontName
        self.comp.text.text = ''
        compBlocks = _compositionStringBlocks()
        raise len(compBlocks) > 0 or AssertionError
        self._firstTargetConvertedBlock = -1
        fullWidth = 0
        idx = 0
        for attr, str in compBlocks:
            bgColour, fgColour = _attrToColours(attr)
            if self._firstTargetConvertedBlock < 0 and attr not in [ATTR_INPUT, ATTR_CONVERTED]:
                self._firstTargetConvertedBlock = idx
            if str == IDEOGRAPHIC_SPACE and len(compBlocks) == 1:
                str = ' '
            w = _bgText(str, fontName, bgColour, fgColour)
            w.horizontalAnchor = 'LEFT'
            w.horizontalPositionMode = 'PIXEL'
            w.position.x = fullWidth
            self.comp.addChild(w, 'compBlock%d' % idx)
            idx += 1
            fullWidth += w.width

        self.comp.widthMode = 'PIXEL'
        self.comp.width = fullWidth
        _, self.comp.height = self.comp.compBlock0.text.stringDimensions(compString)
        self.comp.height = self.comp.height * getVPixelScalar()
        cursorIndex = BigWorld.ime.compositionCursorPosition
        cursorOffset = self.comp.compBlock0.text.stringWidth(compString[:cursorIndex])
        self.cursor.position.x = cursorOffset * getHPixelScalar()
        self.comp.backgroundColouriser.colourProvider = BACKGROUND_COLOUR
        self.cursor.script.enable(True)
        self.cursor.script.touch()

    def _populateKorean(self, fontName):
        compString = BigWorld.ime.composition
        self.comp.text.font = fontName
        self.comp.text.text = compString
        sw, sh = self.comp.text.stringDimensions(compString)
        hratio = getHPixelScalar()
        vratio = getVPixelScalar()
        self.comp.width = sw * hratio
        self.comp.height = sh * vratio
        self.comp.text.position.x = 0
        self.comp.backgroundColouriser.colourProvider = blinkingColourProvider(BACKGROUND_COLOUR, Utils.CURSOR_BLINK_PERIOD)
        self.cursor.script.enable(False)

    def reposition(self, positionClip, minClip, maxClip):
        widthInClip, heightInClip = Utils.clipSize(self.comp)
        if positionClip[0] + widthInClip > maxClip[0]:
            positionClip = minClip
        self.comp.position.x = positionClip.x
        self.comp.position.y = positionClip.y

    def clipBounds(self):
        return Utils.clipRegion(self.comp)

    def candidateClipBounds(self):
        clipMins, clipMaxs = self.cursor.script.clipBounds()
        if BigWorld.ime.language == 'JAPANESE':
            ftcb = self._firstTargetConvertedBlock
            block = getattr(self.comp, 'compBlock%d' % ftcb, None)
            if block is not None:
                widthMode = block.widthMode
                block.widthMode = 'CLIP'
                blockMins = block.localToScreen((-1, -1))
                block.widthMode = widthMode
                clipMins[0] = blockMins[0]
                clipMaxs[0] = blockMins[0]
        return (clipMins, clipMaxs)

    def hide(self):
        self.comp.visible = False


class ReadingWindow(object):
    MARGIN_SIZE = 2

    @staticmethod
    def create():
        component = GUI.Window(db.DBLogic.g_instance.getGUITexture('TX_MAP_MASK'))
        component.materialFX = 'BLEND'
        component.colour = BACKGROUND_COLOUR
        component.visible = False
        component.horizontalPositionMode = 'CLIP'
        component.horizontalAnchor = 'LEFT'
        component.verticalPositionMode = 'CLIP'
        component.verticalAnchor = 'TOP'
        component.widthMode = 'PIXEL'
        component.heightMode = 'PIXEL'
        component.position.z = ALWAYS_ON_TOP_Z
        component.script = ReadingWindow(component)
        return component

    def __init__(self, component):
        component.addChild(GUI.Text(''), 'text')
        component.text.multiline = True
        component.text.font = DEFAULT_FONT_NAME
        component.text.horizontalAnchor = 'LEFT'
        component.text.horizontalPositionMode = 'PIXEL'
        component.text.verticalAnchor = 'TOP'
        component.text.verticalPositionMode = 'PIXEL'
        self.comp = weakref.proxy(component)

    def populate(self, fontName):
        readingString = BigWorld.ime.reading
        if not BigWorld.ime.readingVisible or len(readingString) == 0:
            self.comp.visible = False
            return False
        self.comp.text.font = fontName
        if BigWorld.ime.readingVertical:
            readingString = '\n'.join([ c for c in readingString ])
        horzMargin = self.MARGIN_SIZE * getHPixelScalar()
        vertMargin = self.MARGIN_SIZE * getVPixelScalar()
        self.comp.text.text = readingString
        self.comp.text.position.x = horzMargin
        self.comp.text.position.y = vertMargin
        self.comp.widthMode = 'PIXEL'
        textWidth, textHeight = self.comp.text.stringDimensions(readingString)
        self.comp.width = horzMargin * 2 + textWidth * getHPixelScalar()
        self.comp.height = vertMargin * 2 + textHeight * getVPixelScalar()
        self.comp.visible = True
        return True

    def reposition(self, screenClipMins, screenClipMaxs):
        clipWidth, clipHeight = Utils.clipSize(self.comp)
        cx, cy = screenClipMaxs.x, screenClipMins.y
        if cy - clipHeight < -1.0:
            cy = screenClipMaxs.y + clipHeight
        self.comp.position[0] = cx
        self.comp.position[1] = cy
        self.comp.visible = True

    def clipBounds(self):
        return Utils.clipRegion(self.comp)

    def hide(self):
        self.comp.visible = False


class CandidateWindow(object):

    @staticmethod
    def create():
        component = GUI.Window(db.DBLogic.g_instance.getGUITexture('TX_MAP_MASK'))
        component.colour = (32, 32, 32, 255)
        component.materialFX = 'BLEND'
        component.visible = False
        component.horizontalPositionMode = 'CLIP'
        component.horizontalAnchor = 'LEFT'
        component.position.x = 0
        component.verticalPositionMode = 'CLIP'
        component.verticalAnchor = 'TOP'
        component.position.y = 0
        component.position.z = ALWAYS_ON_TOP_Z
        component.widthMode = 'PIXEL'
        component.heightMode = 'PIXEL'
        component.script = CandidateWindow(component)
        return component

    def __init__(self, component):
        component.addChild(GUI.Text(''), 'candidateText')
        component.candidateText.font = DEFAULT_FONT_NAME
        component.candidateText.multiline = True
        component.candidateText.horizontalPositionMode = 'PIXEL'
        component.candidateText.verticalPositionMode = 'PIXEL'
        component.candidateText.horizontalAnchor = 'LEFT'
        component.candidateText.verticalAnchor = 'TOP'
        component.candidateText.position = (0, 0, 0.5)
        self.comp = weakref.proxy(component)

    def populate(self, fontName):
        if not BigWorld.ime.candidatesVisible:
            self.comp.visible = False
            return False
        candidates = BigWorld.ime.candidates
        selectedIdx = BigWorld.ime.selectedCandidate
        fullText = u''
        preSelectWidth = 0
        for i in range(len(candidates)):
            fullText += str((i + 1) % 10) + candidates[i]
            if i < len(candidates) - 1:
                fullText += u'\n' if BigWorld.ime.candidatesVertical else u' '
            if i == selectedIdx - 1:
                preSelectWidth, _ = self.comp.candidateText.stringDimensions(fullText)

        self.comp.candidateText.font = fontName
        self.comp.candidateText.text = fullText
        sw, sh = self.comp.candidateText.stringDimensions(fullText)
        self._resize(sw, sh)
        if hasattr(self.comp, 'selectedCandidate'):
            self.comp.delChild(self.comp.selectedCandidate)
        if selectedIdx >= 0 and len(candidates) > 0:
            selStr = str((selectedIdx + 1) % 10) + candidates[selectedIdx]
            selectedComp = _bgText(selStr, fontName, SELECTED_CANDIDATE_BGCOLOUR, SELECTED_CANDIDATE_FGCOLOUR)
            selectedComp.horizontalAnchor = 'LEFT'
            selectedComp.horizontalPositionMode = 'PIXEL'
            selectedComp.verticalAnchor = 'TOP'
            selectedComp.verticalPositionMode = 'PIXEL'
            selectedComp.position.z = 0.01
            selectedComp.text.horizontalPositionMode = 'PIXEL'
            selectedComp.text.horizontalAnchor = 'LEFT'
            selectedComp.text.position.x = 0
            fontWidth, fontHeight = self.comp.candidateText.stringDimensions(selStr)
            if BigWorld.ime.candidatesVertical:
                selectedComp.position.x = 0
                selectedComp.position.y = fontHeight * selectedIdx * getVPixelScalar()
                selectedComp.widthMode = self.comp.widthMode
                selectedComp.width = self.comp.width
            else:
                selectedComp.position.x = preSelectWidth * getHPixelScalar()
                selectedComp.position.y = 0
                selectedComp.widthMode = 'PIXEL'
                selectedComp.width = (fontWidth + 1) * getHPixelScalar()
                selectedComp.heightMode = self.comp.heightMode
                selectedComp.height = self.comp.height
            self.comp.addChild(selectedComp, 'selectedCandidate')
        self.comp.visible = True
        return True

    def reposition(self, screenClipMins, screenClipMaxs):
        clipWidth, clipHeight = Utils.clipSize(self.comp)
        cx, cy = screenClipMaxs.x, screenClipMins.y
        if cy - clipHeight < -1.0:
            cy = screenClipMaxs.y + clipHeight
        if cx + clipWidth > 1.0:
            cx = max(-1.0, 1.0 - clipWidth)
        self.comp.position[0] = cx
        self.comp.position[1] = cy

    def _resize(self, pixelW, pixelH):
        self.comp.width = pixelW * getHPixelScalar()
        self.comp.height = pixelH * getVPixelScalar()

    def hide(self):
        self.comp.visible = False


_composition = None
_reading = None
_candidates = None

def init():
    """
            Initialises the singleton IME GUI components (i.e. composition
            and candidate windows). These components are displayed on top of
            all other GUI components and are positioned in screen clip space.
    """
    global _composition
    global _reading
    global _candidates
    TRACE_MSG('Initialising IME components')
    if _composition is None:
        _composition = CompositionWindow.create()
        GUI.addRoot(_composition)
    if _reading is None:
        _reading = ReadingWindow.create()
        GUI.addRoot(_reading)
    if _candidates is None:
        _candidates = CandidateWindow.create()
        GUI.addRoot(_candidates)
    return


def fini():
    """
            Cleans up the singleton IME GUI components. This should
            be called on application shutdown.
    """
    global _reading
    global _candidates
    global _composition
    if _composition is not None:
        GUI.delRoot(_composition)
        _composition = None
    if _reading is not None:
        GUI.delRoot(_reading)
        _reading = None
    if _candidates is not None:
        GUI.delRoot(_candidates)
        _candidates = None
    return


def refresh(positionClip, minClip, maxClip, fontName):
    """
            Refreshes the IME sub-components based on the current
            underlying IME state. This should be called on IME events
            coming from the engine (i.e. handleIMEEvent).
    
            Parameters:
    
            positionClip            -       The clip space position where the composition
                                                            string will be placed (ideally).
    
            minClip, maxClip        -       The clip space bounding box of the parent edit box.
                                                            This is used to keep the IME components viewable in
                                                            this area of the screen. This is calculated based on
                                                            the screenClip parameter and the final width of the
                                                            composition window.
            fontName                        -       The name of the font resource to use to display text.
                                                            This is usually set to the same font as the edit control
                                                            that invoked the IME.
    """
    if _composition is None or _candidates is None or _reading is None:
        ERROR_MSG('IME components have not been initialised.')
        return
    else:
        gotComposition = _composition.script.populate(fontName)
        gotReading = _reading.script.populate(CANDIDATE_READING_FONT_NAME)
        gotCandidates = _candidates.script.populate(CANDIDATE_READING_FONT_NAME)
        if gotComposition:
            _composition.script.reposition(positionClip, minClip, maxClip)
        else:
            return
        compPosMins, compPosMaxs = _composition.script.clipBounds()
        candPosMins, candPosMaxs = _composition.script.candidateClipBounds()
        if gotReading:
            _reading.script.reposition(compPosMins, compPosMaxs)
            readingMins, readingMaxs = _reading.script.clipBounds()
            candPosMins[1] = readingMins[1]
            candPosMaxs[1] = compPosMaxs[1]
        else:
            candPosMins[1] = compPosMins[1]
            candPosMaxs[1] = compPosMaxs[1]
        if gotCandidates:
            _candidates.script.reposition(candPosMins, candPosMaxs)
        return


def handleIMEEvent(event, positionClip, minClip, maxClip, fontName):
    """
            Takes a PyIMEEvent object and calls refresh if neccessary.
            See refresh for detailed information on the other parameters.
    """
    if event.compositionChanged or event.compositionCursorPositionChanged or event.candidatesVisibilityChanged or event.candidatesChanged or event.selectedCandidateChanged or event.readingChanged:
        refresh(positionClip, minClip, maxClip, fontName)


def hideAll():
    """
            Hides any visible IME interfaces.
    """
    _composition.script.hide()
    _candidates.script.hide()
    _reading.script.hide()