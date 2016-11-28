# Embedded file name: scripts/common/arena_bonus_type_caps.py
from constants import ARENA_BONUS_TYPE

class ARENA_BONUS_TYPE_CAPS():
    RESULTS = 'RESULTS'
    DAMAGE_VEHICLE = 'DAMAGE_VEHICLE'
    CREDITS = 'CREDITS'
    XP = 'XP'
    RANSOM_IN = 'RANSOM_IN'
    REWARD_FOR_ACHIEVEMENT = 'REWARD_FOR_ACHIEVEMENT'
    QUESTS = 'QUESTS'
    DOSSIER_TOTAL = 'DOSSIER_TOTAL'
    DOSSIER_KILL_LIST = 'DOSSIER_KILL_LIST'
    DOSSIER_15X15 = 'DOSSIER_15X15'
    DOSSIER_7X7 = 'DOSSIER_7X7'
    DOSSIER_COMPANY = 'DOSSIER_COMPANY'
    DOSSIER_CLAN = 'DOSSIER_CLAN'
    DOSSIER_ACHIEVEMENTS_15X15 = 'DOSSIER_ACHIEVEMENTS_15X15'
    DOSSIER_ACHIEVEMENTS_7X7 = 'DOSSIER_ACHIEVEMENTS_7X7'
    DOSSIER_MAX15X15 = 'DOSSIER_MAX15X15'
    DOSSIER_MAX7X7 = 'DOSSIER_MAX7X7'
    CYBERSPORT_RATING = 'CYBERSPORT_RATING'
    XP_FACTOR_15X15 = 'XP_FACTOR_15X15'
    XP_FACTOR_7X7 = 'XP_FACTOR_7X7'
    CREDITS_FACTOR_15X15 = 'CREDITS_FACTOR_15X15'
    CREDITS_FACTOR_7X7 = 'CREDITS_FACTOR_7X7'
    TKILL_RATING = 'TKILL_RATING'
    DOSSIER_SORTIE = 'DOSSIER_SORTIE'
    DOSSIER_MAXSORTIE = 'DOSSIER_MAXSORTIE'
    DOSSIER_ACHIEVEMENTS_SORTIE = 'DOSSIER_ACHIEVEMENTS_SORTIE'
    FORT_RESOURCE = 'FORT_RESOURCE'
    FORT_QUESTS = 'FORT_QUESTS'
    FORT_BATTLE_RESULTS = 'FORT_BATTLE_RESULTS'
    DOSSIER_FORT_BATTLE = 'DOSSIER_FORT_BATTLE'
    DOSSIER_MAXFORTBATTLE = 'DOSSIER_MAXFORTBATTLE'
    REF_SYSTEM_BONUS = 'REF_SYSTEM_BONUS'
    DOSSIER_RATED7X7 = 'DOSSIER_RATED7X7'
    DOSSIER_MAXRATED7X7 = 'DOSSIER_MAXRATED7X7'
    DOSSIER_CLUB = 'DOSSIER_CLUB'
    DOSSIER_ACHIEVEMENTS_RATED7X7 = 'DOSSIER_ACHIEVEMENTS_RATED7X7'
    INFLUENCE_POINTS = 'INFLUENCE_POINTS'
    RESPAWN = 'RESPAWN'
    INTERACTIVE_STATS = 'INTERACTIVE_STATS'
    FLAG_MECHANICS = 'FLAG_MECHANICS'
    WIN_POINTS_MECHANICS = 'WIN_POINTS_MECHANICS'
    REPAIR_MECHANICS = 'REPAIR_MECHANICS'
    NO_ALLY_DAMAGE = 'NO_ALLY_DAMAGE'
    DAILY_MULTIPLIED_XP = 'DAILY_MULTIPLIED_XP'
    MULTITEAMS = 'MULTITEAMS'
    DOSSIER_GLOBAL_MAP = 'DOSSIER_GLOBAL_MAP'
    RAGE_MECHANICS = 'RAGE_MECHANICS'
    RESOURCE_POINTS = 'RESOURCE_POINTS'
    RANSOM_OUT = 'RANSOM_OUT'
    RENT_BATTLES_COUNTED = 'RENT_BATTLES_COUNTED'
    DOSSIER_FALLOUT = 'DOSSIER_FALLOUT'
    DOSSIER_MAXFALLOUT = 'DOSSIER_MAXFALLOUT'
    CREW_IMMUNE_TO_DAMAGE = 'CREW_IMMUNE_TO_DAMAGE'
    BOOSTERS = 'BOOSTERS'
    GAS_ATTACK_MECHANICS = 'GAS_ATTACK_MECHANICS'
    DOSSIER_ACHIEVEMENTS_FALLOUT = 'DOSSIER_ACHIEVEMENTS_FALLOUT'
    SQUADS = 'SQUADS'
    SQUAD_XP = 'SQUAD_XP'
    COMMON_CHAT = 'COMMON_CHAT'
    REGULAR = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     CREDITS_FACTOR_15X15,
     XP,
     XP_FACTOR_15X15,
     REWARD_FOR_ACHIEVEMENT,
     QUESTS,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     DOSSIER_15X15,
     DOSSIER_ACHIEVEMENTS_15X15,
     DOSSIER_MAX15X15,
     TKILL_RATING,
     REF_SYSTEM_BONUS,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED,
     REPAIR_MECHANICS,
     BOOSTERS,
     SQUADS,
     SQUAD_XP))
    TRAINING = frozenset((RESULTS, REPAIR_MECHANICS, COMMON_CHAT))
    COMPANY = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     CREDITS_FACTOR_15X15,
     XP,
     XP_FACTOR_15X15,
     RANSOM_IN,
     RANSOM_OUT,
     QUESTS,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     DOSSIER_15X15,
     DOSSIER_COMPANY,
     DOSSIER_MAX15X15,
     TKILL_RATING,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED,
     REPAIR_MECHANICS))
    TOURNAMENT = frozenset((RESULTS,
     TKILL_RATING,
     REPAIR_MECHANICS,
     QUESTS))
    TOURNAMENT_REGULAR = frozenset((RESULTS,
     TKILL_RATING,
     REPAIR_MECHANICS,
     CREDITS,
     CREDITS_FACTOR_7X7,
     XP,
     XP_FACTOR_7X7,
     QUESTS,
     BOOSTERS,
     DAMAGE_VEHICLE))
    TOURNAMENT_CLAN = frozenset((RESULTS,
     TKILL_RATING,
     REPAIR_MECHANICS,
     CREDITS,
     CREDITS_FACTOR_7X7,
     XP,
     XP_FACTOR_7X7,
     QUESTS,
     BOOSTERS))
    CLAN = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     CREDITS_FACTOR_15X15,
     XP,
     XP_FACTOR_15X15,
     RANSOM_IN,
     RANSOM_OUT,
     QUESTS,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     DOSSIER_15X15,
     DOSSIER_CLAN,
     TKILL_RATING,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED,
     REPAIR_MECHANICS))
    GLOBAL_MAP = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     CREDITS_FACTOR_15X15,
     XP,
     XP_FACTOR_15X15,
     RANSOM_IN,
     RANSOM_OUT,
     QUESTS,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     DOSSIER_GLOBAL_MAP,
     TKILL_RATING,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED))
    TUTORIAL = frozenset()
    CYBERSPORT = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     CREDITS_FACTOR_7X7,
     XP,
     XP_FACTOR_7X7,
     RANSOM_IN,
     QUESTS,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     DOSSIER_7X7,
     DOSSIER_MAX7X7,
     CYBERSPORT_RATING,
     DOSSIER_ACHIEVEMENTS_7X7,
     TKILL_RATING,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED,
     REPAIR_MECHANICS,
     BOOSTERS))
    EVENT_BATTLES = frozenset((RESULTS, QUESTS, SQUADS))
    FALLOUT_CLASSIC = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     XP,
     QUESTS,
     RESPAWN,
     INTERACTIVE_STATS,
     FLAG_MECHANICS,
     WIN_POINTS_MECHANICS,
     REPAIR_MECHANICS,
     TKILL_RATING,
     RAGE_MECHANICS,
     RESOURCE_POINTS,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED,
     BOOSTERS,
     DOSSIER_FALLOUT,
     DOSSIER_MAXFALLOUT,
     DOSSIER_TOTAL,
     DOSSIER_ACHIEVEMENTS_FALLOUT,
     SQUADS,
     REWARD_FOR_ACHIEVEMENT))
    FALLOUT_MULTITEAM = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     XP,
     QUESTS,
     RESPAWN,
     INTERACTIVE_STATS,
     FLAG_MECHANICS,
     WIN_POINTS_MECHANICS,
     REPAIR_MECHANICS,
     TKILL_RATING,
     MULTITEAMS,
     RAGE_MECHANICS,
     RESOURCE_POINTS,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED,
     BOOSTERS,
     DOSSIER_FALLOUT,
     DOSSIER_MAXFALLOUT,
     DOSSIER_TOTAL,
     GAS_ATTACK_MECHANICS,
     DOSSIER_ACHIEVEMENTS_FALLOUT,
     SQUADS,
     REWARD_FOR_ACHIEVEMENT))
    SORTIE = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     XP,
     RANSOM_IN,
     RANSOM_OUT,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     DOSSIER_SORTIE,
     DOSSIER_MAXSORTIE,
     DOSSIER_ACHIEVEMENTS_SORTIE,
     FORT_RESOURCE,
     INFLUENCE_POINTS,
     QUESTS,
     TKILL_RATING,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED,
     REPAIR_MECHANICS))
    FORT_BATTLE = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     XP,
     RANSOM_IN,
     RANSOM_OUT,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     FORT_BATTLE_RESULTS,
     DOSSIER_FORT_BATTLE,
     DOSSIER_MAXFORTBATTLE,
     QUESTS,
     TKILL_RATING,
     DAILY_MULTIPLIED_XP,
     RENT_BATTLES_COUNTED,
     REPAIR_MECHANICS))
    RATED_CYBERSPORT = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     CREDITS_FACTOR_7X7,
     XP,
     XP_FACTOR_7X7,
     RANSOM_IN,
     QUESTS,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     TKILL_RATING,
     DOSSIER_RATED7X7,
     DOSSIER_MAXRATED7X7,
     CYBERSPORT_RATING,
     DOSSIER_CLUB,
     DOSSIER_ACHIEVEMENTS_RATED7X7,
     RENT_BATTLES_COUNTED,
     REPAIR_MECHANICS,
     BOOSTERS))
    RATED_SANDBOX = frozenset((RESULTS,
     DAMAGE_VEHICLE,
     CREDITS,
     CREDITS_FACTOR_15X15,
     XP,
     XP_FACTOR_15X15,
     QUESTS,
     DOSSIER_TOTAL,
     DOSSIER_KILL_LIST,
     DOSSIER_15X15,
     DOSSIER_MAX15X15,
     TKILL_RATING,
     DAILY_MULTIPLIED_XP,
     CREW_IMMUNE_TO_DAMAGE,
     RENT_BATTLES_COUNTED,
     BOOSTERS))
    SANDBOX = frozenset((RESULTS, TKILL_RATING, CREW_IMMUNE_TO_DAMAGE))
    DOSSIER_ACHIEVEMENTS = frozenset((DOSSIER_ACHIEVEMENTS_7X7,
     DOSSIER_ACHIEVEMENTS_15X15,
     DOSSIER_ACHIEVEMENTS_SORTIE,
     DOSSIER_ACHIEVEMENTS_RATED7X7))
    __RULES = (lambda caps: ARENA_BONUS_TYPE_CAPS.DOSSIER_ACHIEVEMENTS not in caps or ARENA_BONUS_TYPE_CAPS.MULTITEAMS not in caps,
     lambda caps: ARENA_BONUS_TYPE_CAPS.DOSSIER_ACHIEVEMENTS not in caps or ARENA_BONUS_TYPE_CAPS.RESPAWN not in caps,
     lambda caps: ARENA_BONUS_TYPE_CAPS.DOSSIER_CLUB not in caps or ARENA_BONUS_TYPE_CAPS.RESPAWN not in caps,
     lambda caps: ARENA_BONUS_TYPE_CAPS.DOSSIER_CLUB not in caps or ARENA_BONUS_TYPE_CAPS.MULTITEAMS not in caps,
     lambda caps: ARENA_BONUS_TYPE_CAPS.INFLUENCE_POINTS not in caps or ARENA_BONUS_TYPE_CAPS.MULTITEAMS not in caps,
     lambda caps: ARENA_BONUS_TYPE_CAPS.FORT_BATTLE_RESULTS not in caps or ARENA_BONUS_TYPE_CAPS.MULTITEAMS not in caps,
     lambda caps: ARENA_BONUS_TYPE_CAPS.CYBERSPORT_RATING not in caps or ARENA_BONUS_TYPE_CAPS.MULTITEAMS not in caps,
     lambda caps: ARENA_BONUS_TYPE_CAPS.WIN_POINTS_MECHANICS not in caps or ARENA_BONUS_TYPE_CAPS.INTERACTIVE_STATS in caps)
    _typeToCaps = {ARENA_BONUS_TYPE.REGULAR: REGULAR,
     ARENA_BONUS_TYPE.TRAINING: TRAINING,
     ARENA_BONUS_TYPE.COMPANY: COMPANY,
     ARENA_BONUS_TYPE.TOURNAMENT: TOURNAMENT,
     ARENA_BONUS_TYPE.TOURNAMENT_REGULAR: TOURNAMENT_REGULAR,
     ARENA_BONUS_TYPE.TOURNAMENT_CLAN: TOURNAMENT_CLAN,
     ARENA_BONUS_TYPE.CLAN: CLAN,
     ARENA_BONUS_TYPE.GLOBAL_MAP: GLOBAL_MAP,
     ARENA_BONUS_TYPE.TUTORIAL: TUTORIAL,
     ARENA_BONUS_TYPE.CYBERSPORT: CYBERSPORT,
     ARENA_BONUS_TYPE.FALLOUT_CLASSIC: FALLOUT_CLASSIC,
     ARENA_BONUS_TYPE.FALLOUT_MULTITEAM: FALLOUT_MULTITEAM,
     ARENA_BONUS_TYPE.EVENT_BATTLES: EVENT_BATTLES,
     ARENA_BONUS_TYPE.SORTIE: SORTIE,
     ARENA_BONUS_TYPE.FORT_BATTLE: FORT_BATTLE,
     ARENA_BONUS_TYPE.RATED_CYBERSPORT: RATED_CYBERSPORT,
     ARENA_BONUS_TYPE.RATED_SANDBOX: RATED_SANDBOX,
     ARENA_BONUS_TYPE.SANDBOX: SANDBOX}

    @staticmethod
    def init():
        for caps in ARENA_BONUS_TYPE_CAPS._typeToCaps.itervalues():
            for rule in ARENA_BONUS_TYPE_CAPS.__RULES:
                raise rule(caps) or AssertionError

    @staticmethod
    def get(arenaBonusType):
        return ARENA_BONUS_TYPE_CAPS._typeToCaps.get(arenaBonusType, frozenset())

    @staticmethod
    def checkAny(arenaBonusType, *args):
        caps = ARENA_BONUS_TYPE_CAPS.get(arenaBonusType)
        for cap in args:
            if isinstance(cap, str):
                if cap in caps:
                    return True
            elif isinstance(cap, (set, frozenset)):
                if len(cap & caps) > 0:
                    return True

        return False

    @staticmethod
    def checkAll(arenaBonusType, *args):
        caps = ARENA_BONUS_TYPE_CAPS.get(arenaBonusType)
        for cap in args:
            if isinstance(cap, str):
                if cap not in caps:
                    return False
            elif isinstance(cap, (set, frozenset)):
                if len(cap & caps) != len(cap):
                    return False
            else:
                return False

        return True


ARENA_BONUS_TYPE_CAPS.init()