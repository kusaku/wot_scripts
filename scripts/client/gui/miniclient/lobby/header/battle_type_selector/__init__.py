# Embedded file name: scripts/client/gui/miniclient/lobby/header/battle_type_selector/__init__.py
import pointcuts as _pointcuts

def configure_pointcuts():
    _pointcuts.RankedBattle()
    _pointcuts.CommandBattle()
    _pointcuts.TrainingBattle()
    _pointcuts.SpecialBattle()
    _pointcuts.FalloutBattle()
    _pointcuts.OnBattleTypeSelectorPopulate()
    _pointcuts.StrongholdBattle()