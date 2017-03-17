# Embedded file name: scripts/client/PostProcessing/__init__.py
"""The PostProcessing Module.  This imports all of the c++ _PostProcessing module
into the PostProcessing namespace.  It allows code to be written in script to
directly override c++ behaviour."""
from _PostProcessing import *
from _PostProcessing import debug as _debug
from _PostProcessing import chain as _chain
from _PostProcessing import save as _save
from _PostProcessing import load as _load
from bwdebug import ERROR_MSG
from bwdebug import INFO_MSG
import RenderTargets
import Phases
import BigWorld
import ChainView
import ResMgr
import exceptions
from Phases import getPhaseNames
import Listener
DEFAULT_HIGH = 0
DEFAULT_MEDIUM = 1
DEFAULT_LOW = 2
DEFAULT_DISABLED = 3
FXAA_ON = 0
FXAA_OFF = 1
_graphicsSetting = None
_fxaaSetting = None
preChainListeners = []
chainListeners = []
_graphicsSettingListeners = Listener.FunctionListeners()

def _dataSectionFromFilename(filename, createIfMissing = False):
    """
    This method returns a data section, given a data section
    or a filename
    """
    ds = None
    if isinstance(filename, ResMgr.DataSection):
        ds = filename
    else:
        ds = ResMgr.openSection(filename, createIfMissing)
        if ds == None:
            basePath = 'system/post_processing/chains/'
            ds = ResMgr.openSection(basePath + filename, createIfMissing)
    return ds


def _materialPrerequisites(materialSect):
    ret = []
    ret.append(materialSect.readString('fx'))
    for name, sect in materialSect.items():
        if name == 'property' and sect.has_key('Texture'):
            ret.append(sect.readString('Texture'))

    return ret


def prerequisites(filename):
    """
    This method returns a list of resources required for background loading.
    It assumes the data section has been preloaded, since this function needs
    to parse the xml file and must return synchronously.
    
    There are not many resources held by PP effects, mainly their materials.
    The only exceptions are VisualTransferMeshes.
    """
    ds = _dataSectionFromFilename(filename)
    ret = []
    if ds:
        for name, effectSect in ds.items():
            for name, phaseSect in effectSect.items():
                if phaseSect.has_key('material'):
                    ret += _materialPrerequisites(phaseSect['material'])
                if phaseSect.has_key('filterQuad'):
                    if phaseSect['filterQuad'].has_key('PyVisualTransferMesh'):
                        ret.append(phaseSect['filterQuad']['PyVisualTransferMesh'].readString('resourceID'))

    return ret


def chain(*kargs):
    """
    This method overloads the chain method in C++, and extends it
    to provide listener support
    """
    global chainListeners
    global preChainListeners
    if len(kargs) == 0:
        return _chain()
    for preListener in preChainListeners:
        if not preListener(*kargs):
            return

    _chain(*kargs)
    for listener in chainListeners:
        listener()


def save(dataSection):
    """
    This method overloads the underlying C++ function, and allows us to
    check if the dataSection is actually a filename instead.  Also added
    is the default folder name from WorldEditor
    """
    dataSection = _dataSectionFromFilename(dataSection, True)
    return _save(dataSection)


def load(dataSection):
    """
    This method overloads the underlying C++ function, and allows us to
    check if the dataSection is actually a filename instead.  Also added
    is the default folder name from WorldEditor
    """
    dataSection = _dataSectionFromFilename(dataSection)
    return _load(dataSection)


def merge(dataSection, addEffectIfMissing = False):
    """
    This method loads a chain from XML and merges it with the
    existing chain.  Effects with the same name as any of those
    loaded via XML will be replaced.
    """
    dataSection = _dataSectionFromFilename(dataSection)
    from Effects import Properties
    ds = ResMgr.openSection(dataSection)
    oldEffects = chain()
    newEffects = load(ds)
    ch = []
    for old in oldEffects:
        found = False
        for nw in newEffects:
            if old.name == nw.name:
                ch.append(nw)
                found = True
                break

        if not found:
            ch.append(old)

    if addEffectIfMissing == True:
        for nw in newEffects:
            found = False
            for old in ch:
                if old.name == nw.name:
                    found = True
                    break

            if not found:
                pass

    chain(*ch)


def isSupported(dataSection):
    """
    This method checks an dataSection to see if all the Effects contained
    therein are supported by the current graphics setting.
    
    Currently the only issue is that cases are depth-based effects are not
    available if the MRTDepth setting is not turned on.
    
    Raises an AttributeError if it can't open the given dataSection.
    Raises a ValueError if it can't get the "MRT_DEPTH" graphics setting.
    """
    if dataSection is None:
        return True
    else:
        optionIdx = getGraphicsSetting('MRT_DEPTH')
        if optionIdx == 0:
            return True
        ds = ResMgr.openSection(dataSection)
        if ds is None:
            raise exceptions.AttributeError('Could not load data section %s' % (dataSection,))
        effects = ds.readStrings('Effect')
        for name in effects:
            if name in ('Depth of Field (variable filter)', 'Depth of Field (bokeh control)', 'Depth of Field (multi-blur)', 'Rainbow', 'God Rays', 'Volume Light'):
                return False

        return True


def appendChain(effect):
    """
    This method appends an effect to the end of the post-processing chain
    """
    c = list(chain())
    c.append(effect)
    chain(*c)


def insertEffectAfter(previous, effect):
    """
    This method inserts an effect into the post-processing chain,
    after the effect specified by name.
    """
    c = list(chain())
    for i in xrange(0, len(c)):
        if c[i].name == previous:
            c.insert(i, effect)
            chain(*c)
            return True

    return False


def getEffect(name):
    """
    This function finds the appropriate effect in the post-processing chain
    """
    ch = chain()
    for e in ch:
        if e.name == name:
            return e

    raise exceptions.NameError(name)
    return None


def debug():
    """
    This method hides the debug method in C++, and extends it
    by automatically creating a render target for the debug object
    , and showing a GUI     component representing this texture
    """
    import GUI
    s = GUI.Simple('')
    GUI.addRoot(s)
    db = Debug()
    db.renderTarget = BigWorld.RenderTarget('debug post-processing', 1024, 1024)
    _debug(db)
    s.texture = db.renderTarget.texture
    s.materialFX = 'SOLID'
    return s


def debugGui():
    if _debug() == None:
        db = Debug()
        db.renderTarget = BigWorld.RenderTarget('debug post-processing', 1024, 1024)
        _debug(db)
        print 'created debug rT'
    import GUI
    debugWindow = GUI.Window('')
    GUI.addRoot(debugWindow)
    debugWindow.script = ChainView.ChainView(debugWindow)
    debugWindow.script.createChildren()
    debugWindow.size = (0.75, 3.0)
    return debugWindow


def getGraphicsSetting(name):
    """
    Try and get the selected option for the graphics setting called "name".
    Catches exceptions and returns -1 if it wasn't available.
    Eg.
    optionIdx = getGraphicsSetting( "POST_PROCESSING" )
    """
    optionIdx = -1
    try:
        optionIdx = BigWorld.getGraphicsSetting(name)
        INFO_MSG('Found %s option %s' % (name, optionIdx))
    except ValueError as e:
        ERROR_MSG('Unable to get %s graphics setting: %s' % (name, e))

    return optionIdx


def getDefaultChainFile(optionIdx = -1):
    """
    Get the name of the default post processing chain to use.
    Return the file name or None.
    """
    global DEFAULT_MEDIUM
    global DEFAULT_HIGH
    global DEFAULT_LOW
    file = None
    if optionIdx < 0:
        optionIdx = getGraphicsSetting('POST_PROCESSING')
    if optionIdx == DEFAULT_HIGH:
        file = 'system/post_processing/chains/High Graphics Setting.ppchain'
    elif optionIdx == DEFAULT_MEDIUM:
        file = 'system/post_processing/chains/Medium Graphics Setting.ppchain'
    elif optionIdx == DEFAULT_LOW:
        file = 'system/post_processing/chains/Low Graphics Setting.ppchain'
    return file


def defaultChain(optionIdx = -1):
    """
    Create the default BigWorld PostProcessing chain, for the given
    graphics setting level.  If no graphics setting level is passed in,
    the current Post Processing graphics setting is read from the
    graphics setting registry and used.
    """
    file = getDefaultChainFile(optionIdx=-1)
    RenderTargets.clearRenderTargets()
    if file is not None:
        chain(load(file))
    else:
        chain(None)
    return


def isFxaaOn():
    global FXAA_ON
    fxaaIdx = getGraphicsSetting('FXAA_PROCESSING')
    if fxaaIdx == FXAA_ON:
        return True
    return False


def isFxaaSupported():
    """Check if the default graphics pipeline + FXAA is supported."""
    result = False
    file = ''
    file = getFxaaChainFile()
    try:
        result = isSupported(file)
    except AttributeError as e:
        ERROR_MSG('Unable to check if FXAA is supported: %s' % (e,))
        ERROR_MSG('Could not open data section in: ' + file)
    except ValueError as e:
        ERROR_MSG('Unable to check if FXAA is supported: %s' % (e,))

    return result


def getFxaaChainFile(optionIdx = -1):
    """
    Get the name of the post processing chain to use for FXAA.
    optionIdx specifies if the default chain is on high, medium, low, disabled.
    If optionIdx isn't given, then look it up from the current graphics setting.
    Return the file name or None.
    """
    file = None
    if optionIdx < 0:
        optionIdx = getGraphicsSetting('POST_PROCESSING')
    if optionIdx == DEFAULT_HIGH:
        file = 'system/post_processing/chains/High Graphics Setting FXAA.ppchain'
    elif optionIdx == DEFAULT_MEDIUM:
        file = 'system/post_processing/chains/Medium Graphics Setting FXAA.ppchain'
    elif optionIdx == DEFAULT_LOW:
        file = 'system/post_processing/chains/Low Graphics Setting FXAA.ppchain'
    return file


def fxaaChain(optionIdx = -1):
    """
    Load the FXAA chain given by optionIdx.
    optionIdx specifies if the default chain is on high, medium, low, disabled.
    If optionIdx isn't given, then look it up from the current graphics setting.
    """
    file = getFxaaChainFile(optionIdx)
    RenderTargets.clearRenderTargets()
    if file is not None:
        chain(load(file))
    else:
        chain(None)
    return


def registerGraphicsSettingListener(listener):
    global _graphicsSettingListeners
    _graphicsSettingListeners.append(listener)


def _onSelectQualityOption(optionIdx):
    """
    Callback from the graphics settings system when the user changes the desired
    post-processing quality.
    """
    if isFxaaOn():
        fxaaChain(optionIdx)
    else:
        defaultChain(optionIdx)
    from Effects import Properties
    _graphicsSettingListeners(optionIdx)
    BigWorld.callback(0.1, RenderTargets.reportMemoryUsage)


def _onSelectFXAAOption(optionIdx):
    """
    Callback from the graphics settings system when the user changes the desired
    post-processing quality.
    """
    if optionIdx == FXAA_ON:
        fxaaChain()
    else:
        defaultChain()
    defaultIdx = getGraphicsSetting('POST_PROCESSING')
    from Effects import Properties
    _graphicsSettingListeners(defaultIdx)
    BigWorld.callback(0.1, RenderTargets.reportMemoryUsage)


def _registerGraphicsSettings():
    """
    Create and register graphics settings for Post Processing
    """
    global _graphicsSetting
    global _fxaaSetting
    gs = BigWorld.GraphicsSetting('POST_PROCESSING', 'Post Processing', -1, False, False, _onSelectQualityOption)
    gs.addOption('High', 'High', isSupported(getDefaultChainFile(0)))
    gs.addOption('Medium', 'Medium', isSupported(getDefaultChainFile(1)))
    gs.addOption('Low', 'Low', isSupported(getDefaultChainFile(2)))
    gs.addOption('Disabled', 'Disabled', True)
    gs.registerSetting()
    _graphicsSetting = gs
    INFO_MSG('Registered POST_PROCESSING graphics settings')
    gs = BigWorld.GraphicsSetting('FXAA_PROCESSING', 'Fast Approx. AA', -1, False, False, _onSelectFXAAOption)
    gs.addOption('On', 'On', isFxaaSupported())
    gs.addOption('Off', 'Off', True)
    gs.registerSetting()
    _fxaaSetting = gs
    INFO_MSG('Registered FXAA_PROCESSING graphics settings')
    if isFxaaOn():
        fxaaChain()
    else:
        defaultChain()


def _deregisterGraphicsSettings():
    """
    Create and register graphics settings for Post Processing
    """
    global _graphicsSetting
    global _fxaaSetting
    if _graphicsSetting is not None:
        _graphicsSetting.callback = None
        _graphicsSetting = None
    if _fxaaSetting is not None:
        _fxaaSetting.callback = None
        _fxaaSetting = None
    return


def init():
    INFO_MSG('PostProcessing.init()')
    RenderTargets.createStubs()
    _registerGraphicsSettings()


def fini():
    INFO_MSG('PostProcessing.fini()')
    chain(None)
    _deregisterGraphicsSettings()
    RenderTargets.fini()
    Phases.finiPhases()
    _graphicsSettingListeners.reset()
    return


def gatherPhases(effect, name):
    """This function returns a list of phases
    matching the search string.  Wildcard *
    can be used"""
    if name == '*':
        return effect.phases
    else:
        phases = []
        for phase in effect.phases:
            if name == phase.name:
                phases.append(phase)

        return phases


def gatherEffects(chain, name):
    """This function returns a list of effects
    matching the search string.  Wildcard *
    can be used"""
    if name == '*':
        return chain
    else:
        effects = []
        for effect in chain:
            if name == effect.name:
                effects.append(effect)

        return effects


def setMaterialProperty(chain, name, value):
    """
    This function sets a material property on a chain.
    
    The name of the variable can be specified in 1 up to
    3 parts, separated with a forward slash :
    
    material variable name
    phase name/material variable name
    effect name/phase name/material variable name
    
    Additionally, you can use a wild card on the effect or
    phase name :
    
    effect name/*/variable name
    
    If there is more than one phase that has the name that
    matches, the property will be set on multiple materials.
    """
    if chain == None:
        return
    elif len(chain) == 0:
        return
    else:
        searchFields = name.split('/')
        if len(searchFields) == 3:
            effects = gatherEffects(chain, searchFields[0])
            searchFields = searchFields[1:]
        else:
            effects = gatherEffects(chain, '*')
        phases = []
        if len(searchFields) == 2:
            for effect in effects:
                phases += gatherPhases(effect, searchFields[0])

            searchFields = searchFields[1:]
        else:
            for effect in effects:
                phases += gatherPhases(effect, '*')

        if len(searchFields) == 1:
            for phase in phases:
                try:
                    setattr(phase.material, searchFields[0], value)
                except AttributeError:
                    pass

        return


from FilterKernels import *
from Effects import *
global FXAA_OFF ## Warning: Unused global