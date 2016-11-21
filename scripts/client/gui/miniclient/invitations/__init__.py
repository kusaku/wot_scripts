# Embedded file name: scripts/client/gui/miniclient/invitations/__init__.py
import pointcuts as _pointcuts

def configure_pointcuts():
    _pointcuts.PrbDisableAcceptButton()
    _pointcuts.PrbInvitationText()
    _pointcuts.ClubDisableAcceptButton()
    _pointcuts.ClubInvitationText()
    _pointcuts.ClubInvitationComment()