import os
from AppKit import NSApp, NSImage
import vanilla
from mojo.UI import CurrentGlyphWindow, UpdateCurrentGlyphView,\
    StatusInteractivePopUpWindow
from fontParts.world import CurrentGlyph

resourcesDirectory = os.path.dirname(__file__)
resourcesDirectory = os.path.dirname(resourcesDirectory)
resourcesDirectory = os.path.dirname(resourcesDirectory)
resourcesDirectory = os.path.join(resourcesDirectory, "resources")

imageCache = {}

def getImage(name):
    if name not in imageCache:
        imagePath = os.path.join(resourcesDirectory, name + ".pdf")
        image = NSImage.alloc().initWithContentsOfFile_(imagePath)
        image.setTemplate_(True)
        imageCache[name] = image
    return imageCache[name]

def getActiveGlyphWindow():
    window = CurrentGlyphWindow()
    # there is no glyph window
    if window is None:
        return None
    # the editor is not the first responder
    if not window.getGlyphView().isFirstResponder():
        return None
    return window


# ---------------
# Base Controller
# ---------------

class BaseActionWindowController(object):

    def __init__(self):
        glyphWindow = getActiveGlyphWindow()
        if glyphWindow is None:
            return
        self.w = ActionWindow(
            (1, 1),
            centerInView=CurrentGlyphWindow().getGlyphView()
        )
        self.w.responderWillBecomeFirstCallback = self.responderWillBecomeFirstCallback
        # There is probably a better way to set
        # the escape key to close the window but
        # I am lazy so I'm using a hidden button.
        self.w._closeButton = vanilla.ImageButton(
            (0, 0, 0, 0),
            bordered=False,
            callback=self._closeButtonCallback
        )
        self.w._closeButton.bind("\u001B", [])
        # Build the interface
        self.metrics = dict(
            margin=15,
            iconPadding=5,
            iconButtonWidth=30,
            iconButtonHeight=30,
            groupPadding=15,
        )
        rules = self.buildInterface(self.w)
        if rules is not None:
            self.w.addAutoPosSizeRules(rules, self.metrics)
        # Bind close.
        self.w.bind("close", self.windowCloseCallback)
        # Go
        self.w.open()

    def _closeButtonCallback(self, sender):
        self.w.responderWillBecomeFirstCallback = None
        self.w.close()

    def buildInterface(self):
        pass

    def windowCloseCallback(self, sender):
        pass

    def responderWillBecomeFirstCallback(self, responder):
        pass

# ------
# Window
# ------


class TSActionNSWindow(StatusInteractivePopUpWindow.nsWindowClass):

    def makeFirstResponder_(self, responder):
        value = super(TSActionNSWindow, self).makeFirstResponder_(responder)
        if value:
            delegate = self.delegate()
            if delegate is not None and delegate.responderWillBecomeFirstCallback is not None:
                delegate.responderWillBecomeFirstCallback(responder)
        return responder


class ActionWindow(StatusInteractivePopUpWindow):

    nsWindowClass = TSActionNSWindow



# -------------
# Action Button
# -------------

class IconButton(vanilla.ImageButton):

    def __init__(self, imageName, actionName="Quick Action", actionCallback=None, closesWindow=True):
        super(IconButton, self).__init__(
            "auto",
            callback=self.performAction,
            imageObject=getImage(imageName),
            bordered=False
        )
        self.actionName = actionName
        self.actionCallback = actionCallback
        self.closesWindow = closesWindow
        button = self.getNSButton()
        button.setToolTip_(actionName)

    def performAction(self, sender):
        if self.actionCallback is not None:
            glyph = CurrentGlyph()
            glyph.prepareUndo(self.actionName)
            self.actionCallback(glyph)
            glyph.performUndo()
            glyph.changed()
            UpdateCurrentGlyphView()
        if self.closesWindow:
            window = self.getNSButton().window().delegate()
            window.close()
