import os
from AppKit import NSImage
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

# ---------------
# Base Controller
# ---------------

class BaseActionWindowController(object):

    def __init__(self):
        glyphWindow = CurrentGlyphWindow()
        if glyphWindow is None:
            return
        self.w = StatusInteractivePopUpWindow(
            (1, 1),
            centerInView=CurrentGlyphWindow().getGlyphView()
        )
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
        # Go
        self.w.open()

    def _closeButtonCallback(self, sender):
        self.w.close()

    def buildInterface(self):
        pass


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
            pass