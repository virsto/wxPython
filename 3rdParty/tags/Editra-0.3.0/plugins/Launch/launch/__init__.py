# -*- coding: utf-8 -*-
###############################################################################
# Name: __init__.py                                                           #
# Purpose: Launch Plugin                                                      #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################
# Plugin Metadata
"""Run the script in the current buffer"""
__version__ = "0.2"

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#
# Imports
import wx

# Local modules
import launch

# Editra imports
import iface
import plugin
import syntax.synglob as synglob

#-----------------------------------------------------------------------------#
# Globals
_ = wx.GetTranslation

#-----------------------------------------------------------------------------#
# Interface Implementation
class Launch(plugin.Plugin):
    """Script Launcher and output viewer"""
    plugin.Implements(iface.ShelfI)
    ID_LAUNCH = wx.NewId()

    @property
    def __name__(self):
        return u'Launch'

    def AllowMultiple(self):
        """Launch allows multiple instances"""
        return True

    def CreateItem(self, parent):
        """Create a Launch panel"""
        self._log = wx.GetApp().GetLog()
        self._log("[Launch][info] Creating Launch instance for Shelf")

        output = launch.LaunchWindow(parent)
        return output

    def GetId(self):
        """The unique identifier of this plugin"""
        return self.ID_LAUNCH

    def GetMenuEntry(self, menu):
        """This plugins menu entry"""
        return wx.MenuItem(menu, self.ID_LAUNCH, self.__name__, 
                           _("Run script from current buffer"))

    def GetName(self):
        """The name of this plugin"""
        return self.__name__

    def IsStockable(self):
        return True

#-----------------------------------------------------------------------------#
