# Embedded file name: scripts/common/account_shared.py
import collections
import re
from items import vehicles, ITEM_TYPES
from constants import FAIRPLAY_VIOLATIONS_NAMES, FAIRPLAY_VIOLATIONS_MASKS
from items.components.c11n_constants import CustomizationType
from debug_utils import *
if IS_CELLAPP or IS_BASEAPP:
    from typing import Union, Tuple

class AmmoIterator(object):

    def __init__(self, ammo):
        self.__ammo = ammo
        self.__idx = 0

    def __iter__(self):
        return self

    def next(self):
        if self.__idx >= len(self.__ammo):
            raise StopIteration
        idx = self.__idx
        self.__idx += 2
        return (abs(self.__ammo[idx]), self.__ammo[idx + 1])


class LayoutIterator(object):

    def __init__(self, layout):
        self.__layout = layout
        self.__idx = 0

    def __iter__(self):
        return self

    def next(self):
        if self.__idx >= len(self.__layout):
            raise StopIteration
        idx = self.__idx
        self.__idx += 2
        compDescr = self.__layout[idx]
        return (abs(compDescr), self.__layout[idx + 1], compDescr < 0)


def getAmmoDiff(ammo1, ammo2):
    diff = collections.defaultdict(int)
    for compDescr, count in AmmoIterator(ammo1):
        diff[abs(compDescr)] += count

    for compDescr, count in AmmoIterator(ammo2):
        diff[abs(compDescr)] -= count

    return diff


def getEquipmentsDiff(eqs1, eqs2):
    diff = collections.defaultdict(int)
    for eqCompDescr in eqs1:
        if eqCompDescr != 0:
            diff[abs(eqCompDescr)] += 1

    for eqCompDescr in eqs2:
        if eqCompDescr != 0:
            diff[abs(eqCompDescr)] -= 1

    return diff


def currentWeekPlayDaysCount(curTime, newDayStart, newWeekStart):
    curTime += newDayStart
    wday = time.gmtime(curTime).tm_wday + 1
    curWeekPlayDaysCnt = wday - newWeekStart
    if newWeekStart >= 0:
        if curWeekPlayDaysCnt == 0:
            curWeekPlayDaysCnt = 7
        elif curWeekPlayDaysCnt < 0:
            curWeekPlayDaysCnt += 7
    elif curWeekPlayDaysCnt == 8:
        curWeekPlayDaysCnt = 1
    elif curWeekPlayDaysCnt > 8:
        curWeekPlayDaysCnt -= 7
    return curWeekPlayDaysCnt


def getFairPlayViolationName(violationsMask):
    if violationsMask == 0:
        return None
    else:
        for name in FAIRPLAY_VIOLATIONS_NAMES:
            if violationsMask & FAIRPLAY_VIOLATIONS_MASKS[name] != 0:
                return name

        return None


def validateCustomizationItem(custData):
    """Check customization data
    
    :returns: (False, reason) if validation failed or (True, customizationItem) if success
    """
    custID = custData.get('id', None)
    custType = custData.get('custType', None)
    value = custData.get('value', None)
    vehTypeCompDescr = custData.get('vehTypeCompDescr', None)
    if custID is None:
        return (False, 'Cust id is not specified')
    elif not custType:
        return (False, 'Cust type is not specified')
    else:
        custTypeId = getattr(CustomizationType, str(custType).upper(), None)
        if not custTypeId:
            return (False, 'Invalid customization type')
        elif value == 0 or not isinstance(value, int):
            return (False, 'Invalid value')
        c20cache = vehicles.g_cache.customization20()
        c11nItems = c20cache.itemTypes[custTypeId]
        c11nItem = c11nItems.get(custID)
        if not c11nItem:
            return (False, 'Invalid customization item id')
        if vehTypeCompDescr is not None:
            itemTypeID, vehNationID, vehInnationID = vehicles.parseIntCompactDescr(vehTypeCompDescr)
            if itemTypeID != ITEM_TYPES.vehicle:
                return (False, 'Invalid type compact descriptor')
            try:
                vehTypeDescr = vehicles.g_cache.vehicle(vehNationID, vehInnationID)
            except:
                LOG_CURRENT_EXCEPTION()
                return (False, 'Invalid type compact descriptor')

            if not c11nItem.matchVehicleType(vehTypeDescr):
                return (False, 'Customization item {} and vehTypeCompDescr {} mismatch'.format(c11nItem.id, vehTypeCompDescr))
        return (True, c11nItem)


class NotificationItem(object):

    def __init__(self, item):
        self.item = item
        cont = []
        cont.append(item['type'])
        text = item['text']
        for k in sorted(text.keys()):
            cont.append(k)
            cont.append(text[k])

        cont.append(item['data'])
        for s in sorted(item['requiredTokens']):
            cont.append(s)

        self.asString = ''.join(cont)

    def __cmp__(self, other):
        if other is None:
            return 1
        left = self.asString
        right = other.asString
        if left == right:
            return 0
        elif left < right:
            return -1
        else:
            return 1

    def __hash__(self):
        return hash(self.asString)


_VERSION_REGEXP = re.compile('^([a-z]{2,4}_)?(([0-9]+\\.){2,4}[0-9]+)(_[0-9]+)?$')

def parseVersion(version):
    """ Parses given version with formatter reg and returns realm code,
    main and patch version
    
    :param version: Account.def/Properties/requiredVersion
    :return: (realm_code, main_version, patch_version) or None
    """
    result = _VERSION_REGEXP.search(version)
    if result is None:
        return
    else:
        realmCode, mainVersion, _, patchVersion = result.groups()
        if mainVersion:
            realmCode = realmCode.replace('_', '') if realmCode else ''
            patchVersion = int(patchVersion.replace('_', '')) if patchVersion else 0
            return (realmCode, mainVersion, patchVersion)
        return


def isValidClientVersion(clientVersion, serverVersion):
    if clientVersion != serverVersion:
        if clientVersion is None or serverVersion is None:
            return False
        clientParsedVersion = parseVersion(clientVersion)
        serverParsedVersion = parseVersion(serverVersion)
        if clientParsedVersion is None or serverParsedVersion is None:
            return False
        clientRealmCode, clientMainVersion, clientPatchVersion = clientParsedVersion
        serverRealmCode, serverMainVersion, serverPatchVersion = serverParsedVersion
        if clientRealmCode != serverRealmCode:
            return False
        if clientMainVersion != serverMainVersion:
            return False
        if clientPatchVersion < serverPatchVersion:
            return False
    return True


def getClientMainVersion():
    mainVersion = None
    try:
        _, clentVersion = readClientServerVersion()
        parsedVersion = parseVersion(clentVersion)
        _, mainVersion, _ = parsedVersion
    except:
        LOG_ERROR('Can not read or parse client-server version')

    return mainVersion


def readClientServerVersion():
    import ResMgr
    fileName = 'scripts/entity_defs/Account.def'
    section = ResMgr.openSection(fileName)
    if section is None:
        raise Exception('Cannot open ' + fileName)
    for attrName, section in section['Properties'].items():
        if not attrName.startswith('requiredVersion_'):
            continue
        version = section.readString('Default')
        if not version:
            raise Exception('Subsection Account.def/Properties/%s/Default is missing or empty' % attrName)
        section = None
        ResMgr.purge(fileName)
        return (attrName, version)

    raise Exception('Field Account.def/Properties/requiredVersion_* is not found')
    return