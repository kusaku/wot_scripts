# Embedded file name: scripts/client/clientConsts.py
from consts import WORLD_SCALING, ARENA_TYPE, UPGRADE_TYPE, UPDATABLE_TYPE, TYPE_TEAM_OBJECT, IS_EDITOR, INPUT_SYSTEM_STATE, PLANE_TYPE, PART_TYPES_TO_ID, PLANE_CLASS, AIRCRAFT_CHARACTERISTIC, CONSUMABLES_FOR_HAND_USE, GLOBAL_EFFECTS, BOT_DIFFICULTY, SERVER_TICK_LENGTH, CREW_BODY_TYPE
import math
import Math
import BigWorld
LAYER_0_IMPORTED = False
LAYER_1_IMPORTED = False
LAYER_2_IMPORTED = False
if IS_EDITOR:
    pass
else:
    from Helpers.i18n import localizeOptions, localizeLobby
FP_VISIBILITY_DISTANCE = {1: 1200,
 2: 1350,
 3: 1500,
 4: 1650,
 5: 1800,
 6: 1950,
 7: 2100,
 8: 2250,
 9: 2400,
 10: 2550}
FP_SMALL_CIRCLE_K = 0.9
FP_EFFECTIVE_FIRING_DISTANCE_K = 0.7
FP_EFFECTIVE_FIRING_DISTANCE_TO_AIM = 50.0
WAIT_TIME_FOR_SEND_CHAT_MSG = 0.5
ALTITUDE_DX = 1
WARNING_ALTITUDE_LEVEL = 50.0
MIN_TARGET_SIZE = 0.5
MESSAGE_TYPE_UI_COLOR_YELLOW = '1'
MESSAGE_TYPE_UI_COLOR_GREEN = '2'
MESSAGE_TYPE_UI_COLOR_RED = '3'
MESSAGE_TYPE_UI_COLOR_BLUE = '4'
LOC_HINT_PLANE_TASK = {PLANE_TYPE.FIGHTER: 'hint_fighter_1',
 PLANE_TYPE.HFIGHTER: 'hint_hfighter_1',
 PLANE_TYPE.ASSAULT: 'hint_assault_1',
 PLANE_TYPE.NAVY: 'hint_dfighter_1'}
CRASHED_BY_ELEVATED_OBJECT = 1.5 * WORLD_SCALING
EFFECT_COLLISION_RANGE = 15 * WORLD_SCALING

class BULLET_PARAM:
    OWN = 0
    FOREIGN = 1
    INVISIBLE = 2


DELAY_AUTOSWITCH_PLANE = 0.5
DELAY_AUTOSWITCH_GROUNDOBJECT = 2
DELAY_SHOW_DESTROYED_PLANE = 3
DELAY_SHOW_DESTROYED_GROUNDOBJECT = 3
TARGET_RENDER_DISTANCE = 2000 * WORLD_SCALING
ACTIONMATCHER_ANIMATION_DISTANCE = 300.0
TEAMOBJECT_SIMPLIFICATION_DISTANCE = 1500 * WORLD_SCALING
TEAMOBJECT_SIMPLIFICATION_FILTER = 80 * WORLD_SCALING
DECAL_NUM_MIN = 2
DECAL_ISNT_EXIST_VALUE = [-1,
 -1,
 -1,
 -1,
 -1,
 0,
 -1,
 -1]
DECAL_DEFAULT_VALUE = [1,
 1,
 1,
 -1,
 -1,
 -1,
 -1,
 -1]
PROPELLOR_TRANSITION_TIME = 2
BOMB_SIGN_DISABLED_MATERIAL = 'lambert1'
FORCE_AND_FLAPS_AXIS = 99
SLATS_AXIS = 98
TURRET_TRACKER_AXIS = 97
SCENARIO_TRACKER_AXIS = 96
FORCE_AXIS_FALL_VALUE = -1.05
FORCE_AXIS_STOPPED_VALUE = -1.1
FORCE_AXIS_DEATH_VALUE = -1.1
FLAPS_SWITCHING_BY_FORCE = False
LOCAL_PARTICLE_ADJUST = Math.Vector3(0.0, 0.0, 1.0)
COMPOUND_ALPHA_ANIM_SPEED = 10

class VOIP_ICON_TYPES:
    NONE = 0
    DISCONNECTED = 1
    LISTENING = 2
    ARENA_CHANNEL_TALKING = 3
    SQUAD_CHANNEL_TALKING = 4
    SQUAD_CHANNEL = 5
    ARENA_CHANNEL = 6
    MUTED = 7
    UNAVAILABLE = 8

    @staticmethod
    def getConstNameByValue(const):
        for k, v in VOIP_ICON_TYPES.__dict__.items():
            if v == const:
                return k


class VOIP_ICON_TYPES_ARENA:
    NONE = 0
    ARENA_CHANNEL = 1
    SQUAD_CHANNEL = 2
    MUTED = 3
    DISCONNECTED = 4
    UNAVAILABLE = 5


class WEAPON_TYPES:
    GUN = 0
    ROCKET = 1
    BOMB = 2
    CANNON = 3


NEUTRAL_OBJECTS_COMMAND_TEAM_INDEX = 2
COSUMABLES_FOR_HAND_USE_REPAIRING_MODULES = {CONSUMABLES_FOR_HAND_USE.REPAIRING_MODULES_ENGINE: PART_TYPES_TO_ID['Engine']}

class BATTLE_UI_TYPES:
    NORMAL = 0
    MINIMAL = 1


SI_TO_IMPERIAL_KMH = 1.61
SI_TO_IMPERIAL_METER = 0.3048
SI_TO_IMPERIAL_KGS = 0.45359237
SI_TO_SEA_KMH = 1.853
SI_TO_SEA_METER = 0.3048
SI_TO_SEA_KGS = 0.45359237
SI_TO_SI_KMH = 1
SI_TO_SI_METER = 1
SI_TO_SI_KGS = 1
CLIENT_INACTIVITY_TIMEOUT = 40
PREBATTLE_PLANE_TYPE_NAME = {PLANE_TYPE.FIGHTER: 'prebattle_plane_type_fighter',
 PLANE_TYPE.HFIGHTER: 'prebattle_plane_type_heavy_fighter',
 PLANE_TYPE.ASSAULT: 'prebattle_plane_type_assault',
 PLANE_TYPE.NAVY: 'prebattle_plane_type_navy'}

class PLANE_TYPE_ICO_PATH:
    PLANE_TYPE_DICT = {PLANE_TYPE.FIGHTER: 'Fighter',
     PLANE_TYPE.HFIGHTER: 'HeavyFighter',
     PLANE_TYPE.ASSAULT: 'Attack',
     PLANE_TYPE.NAVY: 'MFighter'}
    PLANE_CLASS_DICT = {PLANE_CLASS.REGULAR: 'Regular',
     PLANE_CLASS.ELITE: 'Elite',
     PLANE_CLASS.PREMIUM: 'Premium'}
    TEMPLATE = 'icons/planeTypes/iconCarousel%s%s.png'

    @staticmethod
    def icon(planeType, planeStatus):
        return PLANE_TYPE_ICO_PATH.TEMPLATE % (PLANE_TYPE_ICO_PATH.PLANE_TYPE_DICT[planeType], PLANE_TYPE_ICO_PATH.PLANE_CLASS_DICT[planeStatus])


BATTLE_RESULT_ICOS_PATH = 'icons/planeTypesHud/%s'

class PLANE_TYPE_BATTLE_RESULT_ICO_PATH:
    PLANE_TYPE_DICT = {PLANE_TYPE.FIGHTER: 'hudTypeFighter_Color.png',
     PLANE_TYPE.HFIGHTER: 'hudTypeHeavyFighter_Color.png',
     PLANE_TYPE.ASSAULT: 'hudTypeAttack_Color.png',
     PLANE_TYPE.NAVY: 'hudTypeMFighter_Color.png'}

    @staticmethod
    def icon(planeType):
        return BATTLE_RESULT_ICOS_PATH % PLANE_TYPE_BATTLE_RESULT_ICO_PATH.PLANE_TYPE_DICT[planeType]


PLANE_TYPES_ORDER = [PLANE_TYPE.FIGHTER,
 PLANE_TYPE.NAVY,
 PLANE_TYPE.HFIGHTER,
 PLANE_TYPE.ASSAULT]
HUD_PLANE_TYPES_LOC_ID = {PLANE_TYPE.FIGHTER: 'prebattle_plane_type_fighter',
 PLANE_TYPE.HFIGHTER: 'prebattle_plane_type_heavy_fighter',
 PLANE_TYPE.ASSAULT: 'prebattle_plane_type_assault',
 PLANE_TYPE.NAVY: 'prebattle_plane_type_navy'}

def getHudPlaneIcon(planeType):
    return 'icons/planeTypesHud/hudType%s_Color.png' % PLANE_TYPE_ICO_PATH.PLANE_TYPE_DICT.get(planeType, PLANE_TYPE.FIGHTER)


BATTLE_RESULT_TURRET_ICO_PATH = BATTLE_RESULT_ICOS_PATH % 'iconHudTypeTurret.png'
BATTLE_RESULT_GROUND_OBJECT_ICO_PATH = BATTLE_RESULT_ICOS_PATH % 'iconHudTypeGroundTarget.png'
BATTLE_RESULT_BASE_OBJECT_ICO_PATH = BATTLE_RESULT_ICOS_PATH % 'iconHudTypeGroundTarget.png'
BATTLE_NAME_BY_TYPE_HUD_LOC_ID = {ARENA_TYPE.NORMAL: 'battle_random',
 ARENA_TYPE.PVE: 'battle_pve',
 ARENA_TYPE.DEV: 'battle_dev',
 ARENA_TYPE.TRAINING: 'battle_training',
 ARENA_TYPE.TUTORIAL: 'battle_tutorial',
 ARENA_TYPE.PVP_WITH_BOTS: 'battle_random',
 ARENA_TYPE.JAPANESE_THREAT: 'lobby_ja_tr_header'}
BATTLE_DESC_BY_TYPE_HUD_LOC_ID = {ARENA_TYPE.NORMAL: 'pre_battle_description_random',
 ARENA_TYPE.PVE: 'pre_battle_description_pve',
 ARENA_TYPE.DEV: 'pre_battle_description_dev',
 ARENA_TYPE.TRAINING: 'pre_battle_description_training',
 ARENA_TYPE.TUTORIAL: 'pre_battle_description_tutorial',
 ARENA_TYPE.PVP_WITH_BOTS: 'pre_battle_description_random',
 ARENA_TYPE.JAPANESE_THREAT: 'battle_ja_tr'}
BATTLE_LOBBY_DESC_BY_TYPE_HUD_LOC_ID = {ARENA_TYPE.NORMAL: 'lobby_battle_description_random',
 ARENA_TYPE.PVE: 'lobby_battle_description_pve',
 ARENA_TYPE.TRAINING: 'lobby_battle_description_training',
 ARENA_TYPE.TUTORIAL: 'lobby_battle_description_tutorial',
 ARENA_TYPE.PVP_WITH_BOTS: 'lobby_battle_description_random'}
BATTLE_LOBBY_ICON_BY_TYPE_HUD_LOC_ID = {ARENA_TYPE.NORMAL: 'standard',
 ARENA_TYPE.PVE: 'pve',
 ARENA_TYPE.TRAINING: 'training',
 ARENA_TYPE.TUTORIAL: 'tutorial',
 ARENA_TYPE.PVP_WITH_BOTS: 'standard'}
LOBBY_MESSAGE_MAX_SIZE = 512
HANGAR_VEHICLE_SWITCHING_WAIT_FRAMES = 4
EMPTY_WEAPON_SLOT_ICON_PATH = 'icons/modules/modulesIconEmpty.png'
SNOW_BALLS_ICON_PATH = 'icons/weapons/iconWeapSnowball.tga'
SNOW_BALLS_ICON_EMPTY_PATH = SNOW_BALLS_ICON_PATH

class HANGAR_MODE:
    HOME = 0
    AMMUNITION = 1
    MODULES = 2
    RESEARCH = 3
    STORE = 4
    CUSTOMIZATION = 5
    ACHIEVEMENTS = 6
    CREW = 7
    REFRESH_MODEL_MODES = (HOME,
     AMMUNITION,
     MODULES,
     CUSTOMIZATION,
     CREW)


class HANGAR_BUTTONS:
    SELL_PLANES = 0
    BUY_PLANES = 1
    SINGLE_DOGFIGHT = 2


WEAPON_TYPE_TO_UPDATABLE_TYPE_MAP = {UPGRADE_TYPE.BOMB: UPDATABLE_TYPE.BOMB,
 UPGRADE_TYPE.ROCKET: UPDATABLE_TYPE.ROCKET}
DISABLE_TUTORIAL_PROMPT_WINDOW = False
DISABLE_HANGAR_TURRET_ANIMATION = True
AOGAS_NOTIFY_MSG_TITLE = 'NOTIFICATION/TITLE'
AOGAS_NOTIFY_MSG_OK_BTN = 'NOTIFICATION/CLOSE'

class AOGAS_NOTIFY_MSG(object):
    AOND_1 = 'AOND_1'
    AOND_2 = 'AOND_2'
    AOND_3 = 'AOND_3'
    AOND_MORE_3 = 'AOND_MORE_3'
    AOND_MORE_5 = 'AOND_MORE_5'
    RESET = 'RESET'


CAPTCHA_WAITING_SCREEN_MESSAGE = 'LOBBY_LOAD_HANGAR_SPACE_VEHICLE'
HANGAR_LOBBY_WAITING_SCREEN_MESSAGE = 'LOBBY_LOAD_HANGAR_SPACE'
TUTORIAL_DATA_WAITING_SCREEN_MESSAGE = 'LOBBY_LOAD_HANGAR_SPACE_VEHICLE'
PVE_DATA_WAITING_SCREEN_MESSAGE = 'LOBBY_LOAD_HANGAR_SPACE_VEHICLE'
MODULES_TREE_WAITING_SCREEN_MESSAGE = 'LOBBY_LOAD_HANGAR_SPACE_VEHICLE'

class GUI_TYPES:
    EMPTY = 0
    NORMAL = 1
    PREMIUM = 2


GUI_TYPES_DICT = {GUI_TYPES.EMPTY: '',
 GUI_TYPES.NORMAL: 'basic',
 GUI_TYPES.PREMIUM: 'premium'}
HANGAR_SOUND_CONFIG = {'00_01_hangar_base': 'hangarAmbient',
 '00_02_hangar_premium': 'premiumHangarAmbient',
 '00_01_hangar_base_ny': 'hangarAmbientNY',
 '00_02_hangar_premium_ny': 'hangarAmbientNY',
 '00_02_hangar_premium_china': 'hangarAmbient'}
NONBATTLE_MUSIC_THEME = 'main_theme'
BLAST_FORCE_DISTANCE_FACTOR = 0.03
BLAST_FORCE_MAX = 10.0
BULLET_HIT_INITIAL_FORCE = 0.03
BULLET_HIT_FORCE_FACTOR = 0.5
BULLET_HIT_LIMITED_EFFECT_REL_HP_LIMIT = 0.25
SPEED_IDLE_EFFECT_START = 0.3
SPEED_IDLE_EFFECT_END = 0.7
DIVE_WARNING_CFC = 0.7
DIVE_WARNING_MIN_SPEED = 500.0 / 3.6
DIVE_WARNING_ANGLE1 = math.radians(45)
DIVE_WARNING_ANGLE2 = math.radians(60)
CAMERA_MOVING_SPEED = 0.5
CAMERA_SCROLL_SCALE = 0.001
CAMERA_SCROLL_STEP = 0.1
CAMERA_DEFAULT_BOMBING_IDX = 0
CAMERA_ALT_MODE_SHIFT_VECTOR = Math.Vector3(0.0, 0.0, 12.0)
CAMERA_MAX_TARGET_SPEED = 100.0
CAMERA_START_ALIGN_TIME = 1.5
CAMERA_STOP_ALIGN_TIME = 0.5
CAMERA_ALIGN_FLEXIBILITY = 0.27

class CAMERA_ZOOM_PRESET:
    NORMAL_COMBAT = 'normalCombat'
    NORMAL_ASSAULT = 'normalAssault'
    DIRECT_COMBAT = 'directCombat'
    DIRECT_ASSAULT = 'directAssault'
    JOYSTICK_COMBAT = 'joystickCombat'
    JOYSTICK_ASSAULT = 'joystickAssault'
    DEFAULT = NORMAL_COMBAT


INPUT_SYSTEM_PROFILES = {INPUT_SYSTEM_STATE.JOYSTICK: 'profileJoystick',
 INPUT_SYSTEM_STATE.GAMEPAD_DIRECT_CONTROL: 'profileGamepadDirectControl',
 INPUT_SYSTEM_STATE.MOUSE: 'profileMouse051'}
INPUT_SYSTEM_PROFILES_REV = dict([ (value, key) for key, value in INPUT_SYSTEM_PROFILES.iteritems() ])
KEY_RESEARCH_TREE_NATION = 'nation'
KEY_RESEARCH_TREE_NATION_LIST = 'nationList'
KEY_RESEARCH_TREE_DEV_NATION_LIST = 'devnationList'
DEFAULT_RESEARCH_NATION = 2
DEFAULT_RESEARCH_NATION_LIST = '2,1,3,4'
DEFAULT_RESEARCH_DEV_NATION_LIST = '2,1,3,4,5,6,7'

class CLASTERS:
    RU = 'ru'
    EN = 'en'
    NA = 'na'
    CN = 'cn'
    KR = 'kr'


class CombatScreenNames:
    GENERAL = 'general'
    UI = 'interface'
    AIM = 'aim'
    ENEMY = 'enemy'
    TARGET = 'target'
    FRIENDLY = 'friendly'
    SQUADS = 'squads'
    DEAD = 'dead'


AIMS_SHAPE_CROSSHAIR_PREFIX = 'SETTINGS_DROPDOWN_MENU_VARIANT_CROSSHAIR'
AIMS_SHAPE_TARGET_PREFIX = 'SETTINGS_DROPDOWN_MENU_VARIANT_DISPERSION_AREA'
AIMS_SHAPE_EXTERNAL_PREFIX = 'SETTINGS_DROPDOWN_MENU_VARIANT_IRON_SIGHT'
AIMS_COLOR_PREFIX = 'SETTINGS_BATTLE_HUD_CROSSHAIR_COLOR_%s'
CROSSHAIR_SHAPES_COUNT = 13
TARGET_AREA_SHAPES_COUNT = 8
EXTERNAL_AIM_SHAPES_COUNT = 12
FP_COLORS = ['RED',
 'GREEN',
 'WHITE',
 'LILAC',
 'BLUE',
 'BLACK',
 'ORANGE']
if IS_EDITOR:
    FP_COLORS_LOC = []
    CROSSHAIR_SHAPES, CROSSHAIR_COLORS, TARGET_AREA_SHAPES, TARGET_AREA_COLORS, EXTERNAL_AIM_SHAPES = ([],
     [],
     [],
     [],
     [])
else:
    CROSSHAIR_SHAPES = [ ''.join([localizeOptions(AIMS_SHAPE_CROSSHAIR_PREFIX), ' ', str(i)]) for i in range(1, CROSSHAIR_SHAPES_COUNT) ]
    CROSSHAIR_COLORS = [localizeOptions(AIMS_COLOR_PREFIX % 'ORANGE'),
     localizeOptions(AIMS_COLOR_PREFIX % 'RED'),
     localizeOptions(AIMS_COLOR_PREFIX % 'GREEN'),
     localizeOptions(AIMS_COLOR_PREFIX % 'BLUE'),
     localizeOptions(AIMS_COLOR_PREFIX % 'COMBINED')]
    TARGET_AREA_SHAPES = [ ''.join([localizeOptions(AIMS_SHAPE_TARGET_PREFIX), ' ', str(i)]) for i in range(1, TARGET_AREA_SHAPES_COUNT) ]
    TARGET_AREA_COLORS = [localizeOptions(AIMS_COLOR_PREFIX % 'RED'), localizeOptions(AIMS_COLOR_PREFIX % 'BLACK')]
    EXTERNAL_AIM_SHAPES = [ ''.join([localizeOptions(AIMS_SHAPE_EXTERNAL_PREFIX), ' ', str(i)]) for i in range(1, EXTERNAL_AIM_SHAPES_COUNT) ]
    FP_COLORS_LOC = [ localizeOptions(AIMS_COLOR_PREFIX % color) for color in FP_COLORS ]
AIMS_LOC = {'crosshairShape': CROSSHAIR_SHAPES,
 'crosshairColor': CROSSHAIR_COLORS,
 'targetAreaShape': TARGET_AREA_SHAPES,
 'targetAreaColor': TARGET_AREA_COLORS,
 'externalAimShape': EXTERNAL_AIM_SHAPES}
SOUND_SETTINGS_DICT = dict(masterVolume='master', musicVolume='music', voiceVolume='voice', vehicleVolume='aircraft', effectsVolume='sfx', interfaceVolume='ui', ambientVolume='ambient', engineVolume='engine', gunsVolume='guns')
VOIP_SETTINGS_DICT = dict(voiceChatVoiceVolume='voiceVolume', voiceChatMicrophoneSensitivity='voiceActivationLevel', voiceChatAmbientVolume='muffledMasterVolume', voiceChatMicDevice='captureDevice')
GAME_UI_SETTINGS = dict(instruments='mainDevices', instrumentsLocation='mainDevicesLocationList', aviaHorizon='horizon', aviaHorizonType='horizonList', playerList='players', playerListType='curPlayerListState', additionalView='targetWindow', additionalViewType='targetWindowList', damage='damageSchema', damageType='damageSchemaLocationList', healthMetter='damageSchemaInputDamageList', heightMode='heightMode', combatScreenName='combatScreenName', navigationWindowRadar='navigationWindowRadar', navigationWindowMinimap='navigationWindowMinimap', speedometerAndVariometer='speedometerAndVariometer', collisionWarningSystem='collisionWarningSystem', alternativeColorMode='alternativeColorMode', combatInterfaceType='combatInterfaceType')
GAME_UI_SETTINGS_REVERTED = dict([ (value, key) for key, value in GAME_UI_SETTINGS.iteritems() ])
QUALITY_SOUND_LOC = ['SOUND_QUALITY_SETTINGS_TURN_OFF',
 'SOUND_QUALITY_SETTINGS_LOW',
 'SOUND_QUALITY_SETTINGS_MEDIUM',
 'SOUND_QUALITY_SETTINGS_HIGH']
SOUND_QUALITY_IDX_DICT = {3: 0,
 2: 0,
 1: 2,
 0: 1}
CONTROLS_GROUPS = ['SETTINGS_FIRE',
 'SETTINGS_FLIGHT',
 'SETTINGS_HUD',
 'SETTINGS_CAMERA',
 'SETTINGS_CHAPTER_NAVIGATION',
 'SETTINGS_CHAT']
OBJECTS_INFO = {TYPE_TEAM_OBJECT.TURRET: {'ICO_PATH': BATTLE_RESULT_TURRET_ICO_PATH,
                           'LOC_ID': 'TeamTurret_STR'},
 TYPE_TEAM_OBJECT.BIG: {'ICO_PATH': BATTLE_RESULT_BASE_OBJECT_ICO_PATH,
                        'LOC_ID': 'TeamObject_STR'},
 TYPE_TEAM_OBJECT.SMALL: {'ICO_PATH': BATTLE_RESULT_GROUND_OBJECT_ICO_PATH,
                          'LOC_ID': 'TeamObject_STR'},
 TYPE_TEAM_OBJECT.VEHICLE: {'ICO_PATH': BATTLE_RESULT_GROUND_OBJECT_ICO_PATH,
                            'LOC_ID': 'TeamObject_STR'}}
TEXT_MESSAGE_HISTORY_LEN = 5

class TEXT_MESSAGE_TYPES:
    TEXT_MESSAGE = 0
    MARKER_MESSAGE = 1


class SWITCH_STYLES_BUTTONS:
    DISABLED = -1
    HOLD = 1
    SWITCH = 0


FIREPOWER_K = 1.0
SPEED_K = 1.0
MANEUVERABILITY_K = 1.0
HEIGHT_K = 1.0
HP_K = 1.0
OPTIMAL_HEIGHT_FOR_HINTS = 2000

class COMPARING_VEHICLE_STATES:
    NORMAL = 0
    UP = 1
    DOWN = 2


PLANE_TYPE_NAME_HINTS = {PLANE_TYPE.ASSAULT: 'ASSAULT',
 PLANE_TYPE.FIGHTER: 'FIGHTER',
 PLANE_TYPE.NAVY: 'NAVY',
 PLANE_TYPE.HFIGHTER: 'HFIGHTER'}
PERFORMANCE_SPECS_PARAMETERS = [AIRCRAFT_CHARACTERISTIC.HEALTH,
 AIRCRAFT_CHARACTERISTIC.GUNS_FIRE_POWER,
 AIRCRAFT_CHARACTERISTIC.SPEED,
 AIRCRAFT_CHARACTERISTIC.MANEUVERABILITY,
 AIRCRAFT_CHARACTERISTIC.ALT_PERFORMANCE]
INTERFACE_QUERY_PERIOD = SERVER_TICK_LENGTH / 10
__MAX_VIRTUAL_MEMORY_FOR_X86 = 2

def isLowMemory():
    """
    returns true if client CPU is x86 false otherwise
    @return: bool
    """
    return BigWorld.totalVirtualMemory() / 1048576 <= __MAX_VIRTUAL_MEMORY_FOR_X86


EULA_FILE_PATH = 'localization/text/EULA.xml'
OBT_INTRO_FILE_PATH = 'localization/text/OBT.xml'
RELEASE_INTRO_FILE_PATH = 'localization/text/RELEASE.xml'
SINGLE_EXP_INTRO_FILE_PATH = 'localization/text/SINGLE_EXP.xml'
GENERAL_INTRO_FILE_PATH = 'localization/text/GENERAL_TEST.xml'
LEGAL_INFO_FILE_PATH = 'localization/text/Credits.xml'

class GUI_COMPONENTS_DEPH:
    FLASH = 0.5
    MINIMAP_IN_BATTLE_LOADING = 0.4
    MINIMAP_IN_HUD = 0.7


class NOT_CONTROLLED_MOD:
    CONTROLLED = 0
    AUTOPILOT = 1
    PLAYER_MENU = 2
    PLANE_ALIGN = 4
    WAIT_START = 8
    LOST_WINDOW_FOCUS = 16
    MOUSE_INPUT_BLOCKED = 32
    NCBU_STRATEGY_ACTIVATE = PLANE_ALIGN | PLAYER_MENU | LOST_WINDOW_FOCUS | MOUSE_INPUT_BLOCKED


class AXIS_MUTE_MOD:
    NO_MUTE = 0
    DEBUG_CAMERA = 1


def getClientLanguage():
    return str(localizeLobby('LOCALIZATION_LANGUAGE'))


class WINDOW_RENDER_MODE:
    WRM_FULLSCREEN = 0
    WRM_WINDOWED = 1
    WRM_BORDERLESS = 2


NEWS_TICKER_SPEED = 40

class PLAYER_DETH:
    FROM_BOMB = 0
    FROM_ROCKET = 1
    FROM_GUNNER = 2
    COMMON_REASON = 3
    PLAYER_BURNED_YOU = 4
    FROM_HIT = 5
    YOU_BURNED = 6


LOCALIZE_PLAYER_DETH_TABLE = {PLAYER_DETH.FROM_BOMB: ('HUD_PLAYER_DEAD_FROM_BOMB', 'HUD_PLAYER_DEAD_FROM_BOMB_BOT'),
 PLAYER_DETH.FROM_ROCKET: ('HUD_PLAYER_DEAD_FROM_ROCKET', 'HUD_PLAYER_DEAD_FROM_ROCKET_BOT'),
 PLAYER_DETH.FROM_GUNNER: ('HUD_PLAYER_DEAD_FROM_GUNNER', 'HUD_PLAYER_DEAD_FROM_GUNNER_BOT'),
 PLAYER_DETH.COMMON_REASON: ('HUD_PLAYER_DEAD_FROM_COMMON_REASON', 'HUD_PLAYER_DEAD_FROM_COMMON_REASON_BOT'),
 PLAYER_DETH.PLAYER_BURNED_YOU: ('UI_MESSAGE_PLAYER_BURNED_YOU', 'UI_MESSAGE_PLAYER_BURNED_YOU_BOT'),
 PLAYER_DETH.FROM_HIT: ('HUD_PLAYER_DEAD_FROM_HIT', 'UI_MESSAGE_PLAYER_KILLED_YOU_BY_RAM_BOT'),
 PLAYER_DETH.YOU_BURNED: ('UI_MESSAGE_YOU_BURNED', 'UI_MESSAGE_YOU_BURNED')}
SPECTATOR_MODE_SCENARIO = ['',
 'dyn_camera_spectator_1',
 'dyn_camera_spectator_2',
 'dyn_camera_spectator_3',
 'dyn_camera_spectator_4',
 'dyn_camera_spectator_5']
CINEMATIC_CAMERA_SCENARIO_ID = 'cinematic_camera'
INTRO_CAMERA_TIMELINE_POOL = ['dyn_camera_start_1',
 'dyn_camera_start_2',
 'dyn_camera_start_3',
 'dyn_camera_start_4',
 'dyn_camera_start_5',
 'dyn_camera_start_6',
 'dyn_camera_start_7',
 'dyn_camera_start_8',
 'dyn_camera_start_9',
 'dyn_camera_start_10']

class TEAM_OBJECTS_PARTS_TYPES:
    ERROR = -1
    SIMPLE = 1
    SIMPLE_ARMORED = 2
    SIMPLE_FIRING = 3
    SIMPLE_FIRING_ARMORED = 4
    ARMORED = 5
    FIRING_ARMORED = 6


class MARKERS_GROUP_ICON_TYPES:
    MOVING_TARGETS = 1
    ATTACKING_TARGETS = 2
    BASE_TARGETS = 3


MARKERS_GROUP_ICON_INDEXES = {MARKERS_GROUP_ICON_TYPES.MOVING_TARGETS: [1, 3],
 MARKERS_GROUP_ICON_TYPES.ATTACKING_TARGETS: [3, 3],
 MARKERS_GROUP_ICON_TYPES.BASE_TARGETS: [5, 4]}
COUNT_SKIP_INTRO_FOR_DISABLED = 10
TIME_FOR_HIDE_INTRO_HINT_BEFORE_START_BATTLE = 5
TIME_FOR_SHOW_INTRO_HINT = 10.0
MARKERS_GROUP_ICON_LOC_ID = {MARKERS_GROUP_ICON_TYPES.MOVING_TARGETS: ['HUD_DEFENCE', 'HUD_ATTACK'],
 MARKERS_GROUP_ICON_TYPES.ATTACKING_TARGETS: ['HUD_ATTACK', 'HUD_ATTACK'],
 MARKERS_GROUP_ICON_TYPES.BASE_TARGETS: ['HUD_HQ', 'HUD_HQ']}
DAMAGED_PARTS_TEAM_OBJECTS_CALLBACK_TIME = 2.0
DAMAGED_PARTS_NAMES = ['leftWing', 'rightWing', 'tail']
POS_OFFSET_Y = 10
OUTRO_FADEIN_DURATION = 1.0

class TARGET_PARTS_TYPES:
    ARMORED_STATIC = 1
    ARMORED_FIRING = 2
    NOT_ARMORED_STATIC = 3
    NOT_ARMORED_FIRING = 4


ENABLE_CLAN_EMBLEMS = True
ENABLE_PLANE_CLAN_EMBLEM = True

class NODE_TIMELINE_NODE_FLAGS:
    NONE = 0
    STATIC_NODE = 1
    NEAREST_STATIC = 2


NODE_TIMELINE_NEAREST_NODE = 'ground_camera'
EFFECTS_NAMES = {GLOBAL_EFFECTS.FIRE_WORK: 'NY_FIREWORK',
 GLOBAL_EFFECTS.EXPLOSIVE_CHARACTER: 'EFFECT_BOMB_EXPLOSION_MED_SML'}

class SNOWBALLS_MOD:
    ENABLED = True
    NAMESUFFIX = '_SNOWBALLS'
    TRIGGERS = {'LOFT': 11}
    BengalFirePart = 'plane'
    BengalFireNode = 'HP_kill'
    BengalFireEffect = 'FORSAGE_SNOWBALLS'
    BengalFireTrigger = 'FORSAGE_SNOWBALLS'
    BengalFireConsumableID = 10
    LoftTrigger = 'LOFT_SNOWBALLS'

    @staticmethod
    def modName(name):
        return name + SNOWBALLS_MOD.NAMESUFFIX

    @staticmethod
    def getName(consumables, name):
        effect = SNOWBALLS_MOD.TRIGGERS.get(name)
        if effect and effect in consumables:
            return name + SNOWBALLS_MOD.NAMESUFFIX
        return name

    @staticmethod
    def canPlayBengalFire(consumables):
        return SNOWBALLS_MOD.ENABLED and SNOWBALLS_MOD.BengalFireConsumableID in consumables


class FLASH_HUD_STATES:
    UNDEFINED = 0
    BATTLERESULTS = 1
    CHAT = 2
    FASTCOMMANDSMENU = 3
    HELP = 4
    HIDDEN = 5
    MENU = 6
    NORMAL = 7
    SETTINGS = 8
    SPECTATORCINEMA = 9
    SPECTATORDEFAULT = 10
    SPECTATORDINAMIC = 11
    SPECTATORFINAL = 12
    SPECTATORINIT = 13
    TAB = 14
    TUTORIAL = 15


LOCAL_HOLIDAYS_MATRIX = {'APRIL_1ST': {'HUD_WINNERS_STR': 'HUD_WINNERS_STR_APRIL',
               'HUD_LOOSERS_STR': 'HUD_LOOSERS_STR_APRIL',
               'HUD_DRAW_STR': 'HUD_DRAW_STR_APRIL',
               'HUD_MESSAGE_ALLMOST_WIN': 'HUD_MESSAGE_ALLMOST_WIN_APRIL',
               'HUD_MESSAGE_ALLMOST_LOSE': 'HUD_MESSAGE_ALLMOST_LOSE_APRIL',
               'HUD_MESSAGE_ALLIES_DEAD': 'HUD_MESSAGE_ALLIES_DEAD_APRIL',
               'HUD_MESSAGE_ENEMIES_DEAD': 'HUD_MESSAGE_ENEMIES_DEAD_APRIL',
               'HUD_TOO_LOW_ALTITUDE_STR': 'HUD_TOO_LOW_ALTITUDE_STR_APRIL',
               'HUD_STALL_STR': 'HUD_STALL_STR_APRIL',
               'HUD_MAP_BORDER_TOO_CLOSE': 'HUD_MAP_BORDER_TOO_CLOSE_APRIL',
               'HUD_MESSAGE_ENGINE_OVERHEAT': 'HUD_MESSAGE_ENGINE_OVERHEAT_APRIL',
               'HUD_START_FIRE': 'HUD_START_FIRE_APRIL',
               'WAIT_BATTLE_FINISH': 'WAIT_BATTLE_FINISH_APRIL'}}
COLLISION_WARNING_ANGLE = 25.0

class QUEST_CONDITION_ERROR:
    ALLOWED = 0
    WRONG_BATTLE_TYPE = 1
    WRONG_PLANE_LEVEL = 2
    JAPANESE = 3


COMPLEX_QUEST_MIN_PLANE_LEVEL = 4

class PREBATTLE_BOT_DIFFICULTY:
    ICON_PATH_MAP = {BOT_DIFFICULTY.LOW: 'icons/planeTypesHud/botLevel_2.png',
     BOT_DIFFICULTY.MEDIUM: 'icons/planeTypesHud/botLevel_1.png',
     BOT_DIFFICULTY.HIGH: 'icons/planeTypesHud/botLevel_3.png'}
    TITLE_MAP = {BOT_DIFFICULTY.LOW: 'TRAINING_ROOMS_BOT_EASY',
     BOT_DIFFICULTY.MEDIUM: 'TRAINING_ROOMS_BOT_MEDIUM',
     BOT_DIFFICULTY.HIGH: 'TRAINING_ROOMS_BOT_HARD'}


HUD_AMMO_BELTS_TYPE_ICO = {'fugasbelt': 'icons/modules/ammoGoldenAttack.png',
 'armourpiercingbelt2': 'icons/modules/ammoGoldenCrit.png',
 'ap_incinerating': 'icons/modules/ammoGoldenFire.png',
 'standartbelt': 'icons/modules/ammoRegular.png',
 'armourpiercingbelt': 'icons/modules/ammoSilver.png'}
CREW_BODY_TYPE_LOCALIZE_PO_INDEX = {CREW_BODY_TYPE.MALE: '',
 CREW_BODY_TYPE.FEMALE: 'F',
 CREW_BODY_TYPE.UNIQUE: 'U'}