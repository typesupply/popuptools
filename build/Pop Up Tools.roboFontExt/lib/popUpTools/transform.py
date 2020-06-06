from fontTools.misc.arrayTools import unionRect, rectCenter
from fontTools.pens.cocoaPen import CocoaPen
import vanilla
from fontParts.base import BaseBPoint, BaseContour, BaseComponent
from .base import BaseActionWindowController, getImage
from mojo import events
from mojo import drawingTools as bot
from mojo.UI import UpdateCurrentGlyphView, getDefault
from fontParts.world import CurrentGlyph


class TransformationController(BaseActionWindowController):

    def buildInterface(self, w):
        self.glyph = CurrentGlyph()
        self.selection = getSelection(self.glyph)
        self.currentTransformation = None
        self.previewObjects = []
        events.addObserver(self, "drawActionPreview", "drawBackground")

        w.originButton = OriginButton(
            value=None,
            callback=self.updatePreview
        )

        value = False
        if self.selection["contours"] or self.selection["bPoints"]:
            value = True
        w.contoursCheckBox = vanilla.CheckBox(
            "auto",
            "Contours",
            value=value,
            sizeStyle="small"
        )
        w.componentsCheckBox = vanilla.CheckBox(
            "auto",
            "Components",
            value=bool(self.selection["components"]),
            sizeStyle="small"
        )
        w.anchorsCheckBox = vanilla.CheckBox(
            "auto",
            "Anchors",
            value=bool(self.selection["anchors"]),
            sizeStyle="small"
        )
        w.guidesCheckBox = vanilla.CheckBox(
            "auto",
            "Guides",
            value=bool(self.selection["guidelines"]),
            sizeStyle="small"
        )
        w.metricsCheckBox = vanilla.CheckBox(
            "auto",
            "Metrics",
            value=self.selection["metrics"],
            sizeStyle="small"
        )

        w.sectionLine = vanilla.HorizontalLine("auto")

        w.moveGroup = TransformationGroup(
            "Move",
            entry1PreText="x:",
            entry1Value="0",
            entry2PreText="y:",
            entry2Value="0",
            callback=self.moveCallback,
            valueChangedCallback=self.updatePreview
        )
        w.transformLine1 = vanilla.HorizontalLine("auto")
        w.scaleGroup = ScaleGroup(
            callback=self.scaleCallback,
            valueChangedCallback=self.updatePreview
        )
        w.transformLine2 = vanilla.HorizontalLine("auto")
        bounds = self.getSelectionBounds()
        if bounds is None:
            x = 0
            y = 0
        else:
            xMin, yMin, xMax, yMax = bounds
            x = xMax - xMin
            y = yMax - yMin
        w.fitGroup = FitGroup(
            x=x,
            y=y,
            callback=self.fitCallback,
            valueChangedCallback=self.updatePreview
        )
        w.transformLine3 = vanilla.HorizontalLine("auto")
        w.rotateGroup = TransformationGroup(
            "Rotate",
            entry1Value="0",
            entry1PostText="°",
            showEntry2=False,
            callback=self.rotateCallback,
            valueChangedCallback=self.updatePreview
        )
        w.transformLine4 = vanilla.HorizontalLine("auto")
        w.skewGroup = TransformationGroup(
            "Skew",
            entry1PreText="x:",
            entry1Value="0",
            entry1PostText="°",
            entry2PreText="y:",
            entry2Value="0",
            entry2PostText="°",
            callback=self.skewCallback,
            valueChangedCallback=self.updatePreview
        )

        m = w.skewGroup.metrics
        self.metrics["optionsIndent"] = self.metrics["margin"] + m["buttonWidth"] + m["padding"] + m["textWidth"]
        self.metrics["originButtonWidth"] = 52
        self.metrics["originButtonHeight"] = self.metrics["originButtonWidth"]
        rules = [
            "H:|-margin-[originButton(==originButtonWidth)]",

            "H:|-optionsIndent-[contoursCheckBox]-margin-|",
            "H:|-optionsIndent-[componentsCheckBox]-margin-|",
            "H:|-optionsIndent-[anchorsCheckBox]-margin-|",
            "H:|-optionsIndent-[guidesCheckBox]-margin-|",
            "H:|-optionsIndent-[metricsCheckBox]-margin-|",

            "H:|-margin-[sectionLine(==272)]-margin-|",

            "H:|-margin-[moveGroup(==sectionLine)]-margin-|",
            "H:|-margin-[transformLine1]-margin-|",
            "H:|-margin-[scaleGroup(==moveGroup)]-margin-|",
            "H:|-margin-[transformLine2]-margin-|",
            "H:|-margin-[fitGroup(==moveGroup)]-margin-|",
            "H:|-margin-[transformLine3]-margin-|",
            "H:|-margin-[rotateGroup(==moveGroup)]-margin-|",
            "H:|-margin-[transformLine4]-margin-|",
            "H:|-margin-[skewGroup(==moveGroup)]-margin-|",

            "V:|-margin-"
                "[moveGroup(==22)]"
                    "-groupPadding-"
                "[transformLine1]"
                    "-groupPadding-"
                "[scaleGroup(==moveGroup)]"
                    "-groupPadding-"
                "[transformLine2]"
                    "-groupPadding-"
                "[fitGroup(==moveGroup)]"
                    "-groupPadding-"
                "[transformLine3]"
                    "-groupPadding-"
                "[rotateGroup(==moveGroup)]"
                    "-groupPadding-"
                "[transformLine4]"
                    "-groupPadding-"
                "[skewGroup(==moveGroup)]"
                    "-groupPadding-"
                "[sectionLine]",

            "V:"
                "[sectionLine]"
                    "-groupPadding-"
                "[contoursCheckBox]"
                "[componentsCheckBox]"
                "[anchorsCheckBox]"
                "[guidesCheckBox]"
                "[metricsCheckBox]"
                    "-margin-"
                "|",

            "V:"
                "[sectionLine]"
                    "-groupPadding-"
                "[originButton(==originButtonHeight)]",

        ]
        return rules

    def windowCloseCallback(self, sender):
        super(TransformationController, self).windowCloseCallback(sender)
        events.removeObserver(self, "drawBackground")

    def responderWillBecomeFirstCallback(self, responder):
        if self.w.moveGroup.containsResponder(responder):
            self.currentTransformation = "move"
        elif self.w.scaleGroup.containsResponder(responder):
            self.currentTransformation = "scale"
        elif self.w.fitGroup.containsResponder(responder):
            self.currentTransformation = "fit"
        elif self.w.rotateGroup.containsResponder(responder):
            self.currentTransformation = "rotate"
        elif self.w.skewGroup.containsResponder(responder):
            self.currentTransformation = "skew"
        self.updatePreview()

    # ----------------
    # Action Callbacks
    # ----------------

    def _action(self, actionName, methodName, previewOnly, **kwargs):
        glyph = self.glyph
        selection = self.selection
        if not previewOnly:
            glyph.prepareUndo(actionName)
        objects = []
        if self.w.contoursCheckBox.get():
            objects += selection["contours"]
            objects += selection["bPoints"]
        if self.w.componentsCheckBox.get():
            objects += selection["components"]
        if self.w.anchorsCheckBox.get():
            objects += selection["anchors"]
        if self.w.guidesCheckBox.get():
            objects += selection["guidelines"]
        if previewOnly:
            objects = [o.copy() for o in objects]
        for obj in objects:
            m = getattr(obj, methodName)
            m(**kwargs)
        if not previewOnly:
            if self.w.metricsCheckBox.get():
                if selection["metrics"]:
                    value = kwargs["value"]
                    if methodName == "moveBy":
                        glyph.width += value[0]
                    elif methodName == "scaleBy":
                        v = glyph.width * value[0]
                        glyph.width = int(round(v))
        if not previewOnly:
            glyph.round() # XXX get the snap value from the prefs?
            glyph.performUndo()
            glyph.changed()
        else:
            self.previewObjects = objects
        UpdateCurrentGlyphView()
        if not previewOnly:
            self.w.close()

    def getSelectionBounds(self):
        selection = self.selection
        bounds = []
        if self.w.contoursCheckBox.get():
            for contour in selection["contours"]:
                b = contour.bounds
                if b is not None:
                    bounds.append(b)
            for bPoint in selection["bPoints"]:
                x = bPoint.anchor.x
                y = bPoint.anchor.y
                bounds.append((x, y, x, y))
        if self.w.componentsCheckBox.get():
            for component in selection["component"]:
                b = component.bounds
                if b is not None:
                    bounds.append(b)
        if self.w.anchorsCheckBox.get():
            for anchor in selection["anchors"]:
                x = anchor.x
                y = anchor.y
                bounds.append((x, y, x, y))
        if not bounds:
            return None
        total = bounds[0]
        for b in bounds[1:]:
            total = unionRect(total, b)
        return total

    def getOrigin(self):
        name = self.w.originButton.get()
        if name is None:
            return None
        xName, yName = name
        bounds = self.getSelectionBounds()
        if bounds is None:
            return None
        xMin, yMin, xMax, yMax = bounds
        xValues = dict(
            left=xMin,
            center=xMin + ((xMax - xMin) / 2),
            right=xMin + xMax
        )
        yValues = dict(
            bottom=yMin,
            center=yMin + ((yMax - yMin) / 2),
            top=yMin + yMax
        )
        x = xValues[xName]
        y = yValues[yName]
        return (x, y)

    def moveCallback(self, sender, previewOnly=False):
        try:
            x, y = sender.get()
            x = int(round(x))
            y = int(round(y))
        except (ValueError, TypeError):
            return
        self._action("Move", "moveBy", previewOnly, value=(x, y))
        if not previewOnly:
            self.updatePreview()

    def scaleCallback(self, sender, previewOnly=False):
        try:
            x, y = sender.get()
            x *= 0.01
            y *= 0.01
            value = (x, y)
        except (ValueError, TypeError):
            return
        origin = self.getOrigin()
        self._action("Scale", "scaleBy", previewOnly, value=value, origin=origin)
        if not previewOnly:
            self.updatePreview()

    def fitCallback(self, sender, previewOnly=False):
        try:
            bounds = self.getSelectionBounds()
            if bounds is None:
                return
            xMin, yMin, xMax, yMax = bounds
            w = abs(xMax - xMin)
            h = abs(yMax - yMin)
            x, y = sender.get()
            x = int(round(x))
            y = int(round(y))
            x /= w
            y /= h
            value = (x, y)
        except (ValueError, TypeError):
            return
        self._action("Fit", "scaleBy", previewOnly, value=(x, y))
        if not previewOnly:
            self.updatePreview()

    def rotateCallback(self, sender, previewOnly=False):
        try:
            value = sender.get()[0]
        except (ValueError, TypeError):
            return
        origin = self.getOrigin()
        self._action("Rotate", "rotateBy", previewOnly, value=value, origin=origin)
        if not previewOnly:
            self.updatePreview()

    def skewCallback(self, sender, previewOnly=False):
        try:
            value = sender.get()
        except (ValueError, TypeError):
            return
        origin = self.getOrigin()
        self._action("Skew", "skewBy", previewOnly, value=value, origin=origin)
        if not previewOnly:
            self.updatePreview()

    # -------
    # Preview
    # -------

    def updatePreview(self, sender=None):
        if self.currentTransformation == "move":
            self.moveCallback(self.w.moveGroup, previewOnly=True)
        elif self.currentTransformation == "scale":
            self.scaleCallback(self.w.scaleGroup, previewOnly=True)
        elif self.currentTransformation == "fit":
            self.fitCallback(self.w.fitGroup, previewOnly=True)
        elif self.currentTransformation == "rotate":
            self.rotateCallback(self.w.rotateGroup, previewOnly=True)
        elif self.currentTransformation == "skew":
            self.skewCallback(self.w.skewGroup, previewOnly=True)

    def drawActionPreview(self, data):
        if not self.previewObjects:
            return
        pen = CocoaPen(glyphSet=self.glyph.layer)
        for obj in self.previewObjects:
            if isinstance(obj, BaseBPoint):
                pass
            elif isinstance(obj, BaseContour):
                obj.draw(pen)
            elif isinstance(obj, BaseComponent):
                obj.draw(pen)
        pixel = 1.0 / data["scale"]
        r, g, b, a = getDefault("glyphViewEchoStrokeColor")
        with bot.savedState():
            bot.fill(None)
            bot.stroke(r, g, b, a)
            bot.strokeWidth(pixel)
            bot.drawPath(pen.path)


def getSelection(glyph):
    contours = []
    bPoints = []
    components = []
    anchors = []
    guidelines = []
    metrics = False
    haveSelection = False
    for contour in glyph.contours:
        if len(contour) == len(contour.selectedSegments):
            contours.append(contour)
            haveSelection = True
        else:
            for bPoint in contour.selectedBPoints:
                bPoints.append(bPoint)
                haveSelection = True
    for component in glyph.selectedComponents:
        components.append(component)
        haveSelection = True
    for anchor in glyph.selectedAnchors:
        anchors.append(anchor)
        haveSelection = True
    if not haveSelection:
        contours = glyph.contours
        components = glyph.components
        anchors = glyph.anchors
        guidelines = glyph.guidelines
        metrics = True
    selection = dict(
        contours=contours,
        bPoints=bPoints,
        components=components,
        anchors=anchors,
        guidelines=guidelines,
        metrics=metrics
    )
    return selection


# ---------------------
# Action Control Groups
# ---------------------

class TransformationGroup(vanilla.Group):

    def __init__(self,
            title,
            entry1PreText="",
            entry1PostText="",
            entry1Value=None,
            showEntry2=True,
            entry2PreText="",
            entry2PostText="",
            entry2Value=None,
            showLinkButton=False,
            linked=False,
            callback=None,
            valueChangedCallback=None
        ):
        super(TransformationGroup, self).__init__("auto")
        self.callback = callback
        self.valueChangedCallback = valueChangedCallback
        self.button = vanilla.Button(
            "auto",
            title,
            callback=self.buttonCallback
        )

        self.entry1PreText = vanilla.TextBox(
            "auto",
            entry1PreText,
            alignment="right"
        )
        self.entry1 = vanilla.EditText(
            "auto",
            entry1Value,
            callback=self.entry1Callback
        )
        self.entry1PostText = vanilla.TextBox(
            "auto",
            entry1PostText,
            alignment="left"
        )

        self.entry2PreText = vanilla.TextBox(
            "auto",
            entry2PreText,
            alignment="right"
        )
        self.entry2 = vanilla.EditText(
            "auto",
            entry2Value,
            callback=self.entry2Callback
        )
        self.entry2PostText = vanilla.TextBox(
            "auto",
            entry2PostText,
            alignment="left"
        )
        if not showEntry2:
            self.entry2PreText.show(False)
            self.entry2.show(False)
            self.entry2PostText.show(False)

        self.linked = linked
        self.linkedImage = getImage("icon-transform-linked")
        self.unlinkedImage = getImage("icon-transform-unlinked")
        if linked:
            image = self.linkedImage
        else:
            image = self.unlinkedImage
        if entry1Value != entry2Value:
            image = self.unlinkedImage
        self.linkedButton = vanilla.ImageButton(
            "auto",
            callback=self.linkedButtonCallback,
            imageObject=self.linkedImage,
            bordered=False
        )
        self.linkedButton.show(showLinkButton)
        self.linked = not self.linked
        self.linkedButtonCallback(self.linkedButton)

        field1 = self.entry1.getNSTextField()
        field2 = self.entry2.getNSTextField()
        field1.setNextKeyView_(field2)
        field2.setNextKeyView_(field1)

        self.metrics = dict(
            padding=3,
            buttonWidth=80,
            entryWidth=42,
            textWidth=15,
            linkedButtonWidth=30,
            linePadding=10
        )
        rules = [
            "H:|"
                "[button(==buttonWidth)]"
                "-padding-"
                "[entry1PreText(==textWidth)]"
                "-padding-"
                "[entry1(==entryWidth)]"
                "-padding-"
                "[entry1PostText(==textWidth)]"
                "-padding-"
                "[entry2PreText(==textWidth)]"
                "-padding-"
                "[entry2(==entryWidth)]"
                "-padding-"
                "[entry2PostText(==textWidth)]"
                "-padding-"
                "[linkedButton(==linkedButtonWidth)]",

            "V:|[button]",
            "V:|[entry1PreText]",
            "V:|[entry1]",
            "V:|[entry1PostText]",
            "V:|[entry2PreText]",
            "V:|[entry2]",
            "V:|[entry2PostText]",
            "V:|[linkedButton]",
        ]
        self.addAutoPosSizeRules(rules, self.metrics)

    def valueChanged(self):
        if self.valueChangedCallback is not None:
            self.valueChangedCallback(self)

    def containsResponder(self, responder):
        if self.entry1.getNSTextField() == responder:
            return True
        if self.entry2.getNSTextField() == responder:
            return True

    def entry1Callback(self, sender):
        self.valueChanged()

    def entry2Callback(self, sender):
        self.valueChanged()

    def linkedButtonCallback(self, sender):
        self.linked = not self.linked
        if self.linked:
            image = self.linkedImage
        else:
            image = self.unlinkedImage
        sender.setImage(imageObject=image)

    def buttonCallback(self, sender):
        if self.callback is not None:
            self.callback(self)

    def get(self):
        value1 = float(self.entry1.get())
        if self.linked:
            value2 = value1
        else:
            value2 = self.entry2.get()
            if value2 is not None:
                value2 = float(value2)
        return value1, value2


class ScaleGroup(TransformationGroup):

    def __init__(self, callback=None, valueChangedCallback=None):
        super(ScaleGroup, self).__init__(
            "Scale",
            entry1PreText="x:",
            entry1Value="100",
            entry1PostText="%",
            entry2PreText="y:",
            entry2Value="100",
            entry2PostText="%",
            showLinkButton=True,
            linked=True,
            callback=callback,
            valueChangedCallback=valueChangedCallback
        )

    def linkedButtonCallback(self, sender):
        super(ScaleGroup, self).linkedButtonCallback(sender)
        self.entry2.enable(not self.linked)
        self.valueChanged()


class FitGroup(TransformationGroup):

    def __init__(self, x, y, callback=None, valueChangedCallback=None):
        self._x = x
        self._y = y
        super(FitGroup, self).__init__(
            "Fit",
            entry1PreText="w:",
            entry1Value=str(x),
            entry2PreText="h:",
            entry2Value=str(y),
            showLinkButton=True,
            linked=True,
            callback=callback,
            valueChangedCallback=valueChangedCallback
        )

    def linkedButtonCallback(self, sender):
        super(FitGroup, self).linkedButtonCallback(sender)
        if self.linked:
            self.entry1Callback(self.entry1)
        self.valueChanged()

    def entry1Callback(self, sender):
        if not self.linked:
            return
        size = sender.get()
        try:
            size = float(size)
        except (ValueError, TypeError):
            return
        scale = size / self._x
        y = int(round(self._y * scale))
        self.entry2.set(str(y))
        self.valueChanged()

    def entry2Callback(self, sender):
        if not self.linked:
            return
        size = sender.get()
        try:
            size = float(size)
        except (ValueError, TypeError):
            return
        scale = size / self._y
        x = int(round(self._x * scale))
        self.entry1.set(str(x))
        self.valueChanged()

    def get(self):
        value1 = float(self.entry1.get())
        value2 = float(self.entry2.get())
        return value1, value2

# --------------
# Origin Control
# --------------

class OriginButton(vanilla.Group):

    def __init__(self, value, callback):
        self.callback = callback
        super(OriginButton, self).__init__("auto")

        self.value = value

        self.image = vanilla.ImageView(
            "auto",
            scale="none"
        )
        self.topLeft = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.topCenter = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.topRight = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.centerLeft = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.centerCenter = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.centerRight = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.bottomLeft = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.bottomCenter = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.bottomRight = vanilla.ImageButton(
            "auto",
            bordered=False,
            callback=self.buttonCallback
        )
        self.updateIcon()

        metrics = {}
        rules = [
            "H:|[topLeft][topCenter(==topLeft)][topRight(==topLeft)]|",
            "H:|[centerLeft(==topLeft)][centerCenter(==topLeft)][centerRight(==topLeft)]|",
            "H:|[bottomLeft(==topLeft)][bottomCenter(==topLeft)][bottomRight(==topLeft)]|",

            "V:|"
                "[topLeft]"
                "[centerLeft(==topLeft)]"
                "[bottomLeft(==topLeft)]"
                "|",
            "V:|"
                "[topCenter(==topLeft)]"
                "[centerCenter(==topLeft)]"
                "[bottomCenter(==topLeft)]"
                "|",
            "V:|"
                "[topRight(==topLeft)]"
                "[centerRight(==topLeft)]"
                "[bottomRight(==topLeft)]"
                "|",
        ]
        self.addAutoPosSizeRules(rules, metrics)

    def updateIcon(self):
        images = {
            None : getImage("icon-transform-origin-none"),
            "topLeft" : getImage("icon-transform-origin-top-left"),
            "topCenter" : getImage("icon-transform-origin-top-center"),
            "topRight" : getImage("icon-transform-origin-top-right"),
            "centerLeft" : getImage("icon-transform-origin-center-left"),
            "centerCenter" : getImage("icon-transform-origin-center-center"),
            "centerRight" : getImage("icon-transform-origin-center-right"),
            "bottomLeft" : getImage("icon-transform-origin-bottom-left"),
            "bottomCenter" : getImage("icon-transform-origin-bottom-center"),
            "bottomRight" : getImage("icon-transform-origin-bottom-right")
        }
        self.image.setImage(imageObject=images[self.value])

    def buttonCallback(self, sender):
        values = {
            self.topLeft : "topLeft",
            self.topCenter : "topCenter",
            self.topRight : "topRight",
            self.centerLeft : "centerLeft",
            self.centerCenter : "centerCenter",
            self.centerRight : "centerRight",
            self.bottomLeft : "bottomLeft",
            self.bottomCenter : "bottomCenter",
            self.bottomRight : "bottomRight",
        }
        value = values[sender]
        if value == self.value:
            value = None
        self.value = value
        self.updateIcon()
        if self.callback is not None:
            self.callback(self)

    def get(self):
        values = {
            None : None,
            "topLeft" : ("left", "top"),
            "topCenter" : ("center", "top"),
            "topRight" : ("right", "top"),
            "centerLeft" : ("left", "center"),
            "centerCenter" : ("center", "center"),
            "centerRight" : ("right", "center"),
            "bottomLeft" : ("left", "bottom"),
            "bottomCenter" : ("center", "bottom"),
            "bottomRight" : ("right", "bottom")
        }
        return values[self.value]
