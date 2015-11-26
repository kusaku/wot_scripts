# Embedded file name: scripts/client/gui/Scaleform/daapi/view/lobby/customization_2_0/purchase_window.py
from Event import Event
from debug_utils import LOG_ERROR
from gui.Scaleform.daapi.view.meta.CustomizationBuyWindowMeta import CustomizationBuyWindowMeta
from gui.Scaleform.framework.entities.DAAPIDataProvider import SortableDAAPIDataProvider
from gui.Scaleform.locale.CUSTOMIZATION import CUSTOMIZATION
from gui.Scaleform.locale.RES_ICONS import RES_ICONS
from gui.Scaleform.locale.TOOLTIPS import TOOLTIPS
from gui.shared.ItemsCache import g_itemsCache
from gui.shared.formatters import text_styles, icons
from gui.shared.utils.functions import makeTooltip
from helpers.i18n import makeString as _ms
from gui.customization_2_0 import g_customizationController, shared
from gui.customization_2_0.shared import formatPriceCredits, formatPriceGold, isSale, getSalePriceString

class PurchaseWindow(CustomizationBuyWindowMeta):

    def __init__(self, ctx = None):
        super(PurchaseWindow, self).__init__()

    def selectItem(self, idx):
        self.__searchDP.setSelectFlag(idx, True)

    def deselectItem(self, idx):
        self.__searchDP.setSelectFlag(idx, False)

    def onWindowClose(self):
        self.destroy()

    def buy(self):
        excludedItems = []
        for item in self.__searchDP.collection:
            if not item['selected']:
                excludedItems.append((item['id'], item['cType']))

        g_customizationController.carousel.slots.cart.buyItems(excludedItems)

    def _dispose(self):
        self.__searchDP.selectionChanged -= self.__setTotalData
        self.__searchDP.fini()
        g_customizationController.carousel.slots.cart.purchaseProcessed -= self.destroy
        super(PurchaseWindow, self)._dispose()

    def _populate(self):
        super(PurchaseWindow, self)._populate()
        g_customizationController.carousel.slots.cart.purchaseProcessed += self.destroy
        self.__totalPrice = {'gold': g_customizationController.carousel.slots.cart.totalPriceGold,
         'credits': g_customizationController.carousel.slots.cart.totalPriceCredits}
        self.__searchDP = PurchaseDataProvider(g_customizationController.carousel.slots.cart.items, self.__totalPrice)
        self.__searchDP.setFlashObject(self.as_getPurchaseDPS())
        self.__searchDP.selectionChanged += self.__setTotalData
        self.as_setInitDataS({'windowTitle': CUSTOMIZATION.WINDOW_PURCHASE_HEADER,
         'imgGold': RES_ICONS.MAPS_ICONS_LIBRARY_GOLDICON_1,
         'imgCredits': RES_ICONS.MAPS_ICONS_LIBRARY_CREDITSICON_1,
         'btnBuyLabel': CUSTOMIZATION.WINDOW_PURCHASE_BTNBUY,
         'btnCancelLabel': CUSTOMIZATION.WINDOW_PURCHASE_BTNCANCEL,
         'buyDisabledTooltip': TOOLTIPS.CUSTOMIZATION_BUYDISABLED_BODY,
         'defaultSortIndex': 0,
         'tableHeader': [self.__packHeaderColumnData('itemName', text_styles.main(CUSTOMIZATION.WINDOW_PURCHASE_TABLEHEADER_ITEMS), 250), self.__packHeaderColumnData('lblBonus', text_styles.main(CUSTOMIZATION.WINDOW_PURCHASE_TABLEHEADER_BONUS), 110), self.__packHeaderColumnData('lblPrice', text_styles.main(CUSTOMIZATION.WINDOW_PURCHASE_TABLEHEADER_COST), 150)]})
        self.__setTotalData()

    def __setTotalData(self):
        notEnoughGoldTooltip = notEnoughCreditsTooltip = ''
        enoughGold = g_itemsCache.items.stats.gold >= self.__totalPrice['gold']
        enoughCredits = g_itemsCache.items.stats.credits >= self.__totalPrice['credits']
        buyEnabled = bool(self.__totalPrice['credits'] + self.__totalPrice['gold']) and enoughGold and enoughCredits
        if not enoughGold:
            diff = text_styles.gold(self.__totalPrice['gold'] - g_itemsCache.items.stats.gold)
            notEnoughGoldTooltip = makeTooltip(_ms(TOOLTIPS.CUSTOMIZATION_NOTENOUGHRESOURCES_HEADER), _ms(TOOLTIPS.CUSTOMIZATION_NOTENOUGHRESOURCES_BODY, count='{0}{1}'.format(diff, icons.gold())))
        if not enoughCredits:
            diff = text_styles.credits(self.__totalPrice['credits'] - g_itemsCache.items.stats.credits)
            notEnoughCreditsTooltip = makeTooltip(_ms(TOOLTIPS.CUSTOMIZATION_NOTENOUGHRESOURCES_HEADER), _ms(TOOLTIPS.CUSTOMIZATION_NOTENOUGHRESOURCES_BODY, count='{0}{1}'.format(diff, icons.credits())))
        self.as_setTotalDataS({'credits': formatPriceCredits(self.__totalPrice['credits']),
         'gold': formatPriceGold(self.__totalPrice['gold']),
         'totalLabel': text_styles.highTitle(_ms(CUSTOMIZATION.WINDOW_PURCHASE_TOTALCOST, selected=self.__searchDP.getSelectedNum(), total=len(self.__searchDP.collection))),
         'buyEnabled': buyEnabled,
         'enoughGold': enoughGold,
         'enoughCredits': enoughCredits,
         'notEnoughGoldTooltip': notEnoughGoldTooltip,
         'notEnoughCreditsTooltip': notEnoughCreditsTooltip})

    @staticmethod
    def __packHeaderColumnData(idx, label, buttonWidth, tooltip = '', icon = '', sortOrder = -1, showSeparator = True):
        return {'id': idx,
         'label': _ms(label),
         'iconSource': icon,
         'buttonWidth': buttonWidth,
         'toolTip': tooltip,
         'sortOrder': sortOrder,
         'defaultSortDirection': 'ascending',
         'buttonHeight': 50,
         'showSeparator': showSeparator}


class PurchaseDataProvider(SortableDAAPIDataProvider):

    def __init__(self, cartItems, totalPrice):
        super(PurchaseDataProvider, self).__init__()
        self._listMapping = {}
        self._list = []
        self.__mapping = {}
        self.__selectedID = None
        self.__totalPrice = totalPrice
        self.__setList(cartItems)
        self.selectionChanged = Event()
        return

    @property
    def collection(self):
        return self._list

    def buildList(self, cartItems):
        self.clear()
        self.__setList(cartItems)

    def emptyItem(self):
        return None

    def getSelectedNum(self):
        result = 0
        for item in self._list:
            if item['selected']:
                result += 1

        return result

    def clear(self):
        self._list = None
        self._listMapping.clear()
        self.__mapping.clear()
        self.__selectedID = None
        return

    def fini(self):
        self.clear()
        self._dispose()

    def getSelectedIdx(self):
        if self.__selectedID in self.__mapping:
            return self.__mapping[self.__selectedID]
        return -1

    def setSelectedID(self, idx):
        self.__selectedID = idx

    def getVO(self, index):
        vo = None
        if index > -1:
            try:
                vo = self.sortedCollection[index]
            except IndexError:
                LOG_ERROR('Item not found', index)

        return vo

    def setSelectFlag(self, idx, flag):
        for item in self._list:
            if item['id'] == idx:
                item['selected'] = flag
                if item['imgCurrency'] == RES_ICONS.MAPS_ICONS_LIBRARY_CREDITSICON_2:
                    if flag:
                        self.__totalPrice['credits'] += item['price']
                    else:
                        self.__totalPrice['credits'] -= item['price']
                elif flag:
                    self.__totalPrice['gold'] += item['price']
                else:
                    self.__totalPrice['gold'] -= item['price']
                self.selectionChanged()
                return None

        return None

    def pyGetSelectedIdx(self):
        return self.getSelectedIdx()

    def pySortOn(self, fields, order):
        super(PurchaseDataProvider, self).pySortOn(fields, order)

    def __setList(self, cartItems):
        self._list = []
        for item in cartItems:
            if item['currencyIcon'] == RES_ICONS.MAPS_ICONS_LIBRARY_CREDITSICON_2:
                priceFormatter = text_styles.credits
            else:
                priceFormatter = text_styles.gold
            dpItem = {'id': item['itemID'],
             'slotIdx': item['idx'],
             'selected': True,
             'cType': item['type'],
             'itemName': item['name'],
             'imgBonus': item['bonusIcon'],
             'imgCurrency': item['currencyIcon'],
             'lblPrice': priceFormatter(item['price']),
             'price': item['price'],
             'lblBonus': text_styles.stats('+{0}%{1}'.format(item['bonusValue'], item['isConditional']))}
            if isSale(item['type'], item['duration']):
                isGold = item['currencyIcon'] != RES_ICONS.MAPS_ICONS_LIBRARY_CREDITSICON_2
                dpItem['salePrice'] = getSalePriceString(isGold, item['price'])
            self._list.append(dpItem)