from fontTools.misc.arrayTools import unionRect, rectCenter
import vanilla
from .base import BaseActionWindowController, IconButton

class AlignDistributeController(BaseActionWindowController):

    def buildInterface(self, w):

        # Align Horizontal

        w.alignTopButton = IconButton(
            imageName="icon-align-top",
            actionName="Align Top",
            actionCallback=self.alignTopCallback
        )
        w.alignYCenterButton = IconButton(
            imageName="icon-align-y-center",
            actionName="Align Y Center",
            actionCallback=self.alignYCenterCallback
        )
        w.alignBottomButton = IconButton(
            imageName="icon-align-bottom",
            actionName="Align Bottom",
            actionCallback=self.alignBottomCallback
        )

        # Align Vertical

        w.alignLeftButton = IconButton(
            imageName="icon-align-left",
            actionName="Align Left",
            actionCallback=self.alignLeftCallback
        )
        w.alignXCenterButton = IconButton(
            imageName="icon-align-x-center",
            actionName="Align X Center",
            actionCallback=self.alignXCenterCallback
        )
        w.alignRightButton = IconButton(
            imageName="icon-align-right",
            actionName="Align right",
            actionCallback=self.alignRightCallback
        )

        self.w.line1 = vanilla.HorizontalLine("auto")

        # Align Both

        w.alignTopLeftButton = IconButton(
            imageName="icon-align-top-left",
            actionName="Align Top Left",
            actionCallback=self.alignTopLeftCallback
        )
        w.alignTopCenterButton = IconButton(
            imageName="icon-align-top-center",
            actionName="Align Top Center",
            actionCallback=self.alignTopCenterCallback
        )
        w.alignTopRightButton = IconButton(
            imageName="icon-align-top-right",
            actionName="Align Top Right",
            actionCallback=self.alignTopRightCallback
        )

        w.alignCenterLeftButton = IconButton(
            imageName="icon-align-center-left",
            actionName="Align Center Left",
            actionCallback=self.alignCenterLeftCallback
        )
        w.alignCenterCenterButton = IconButton(
            imageName="icon-align-center-center",
            actionName="Align Center Center",
            actionCallback=self.alignCenterCenterCallback
        )
        w.alignCenterRightButton = IconButton(
            imageName="icon-align-center-right",
            actionName="Align Center Right",
            actionCallback=self.alignCenterRightCallback
        )

        w.alignBottomLeftButton = IconButton(
            imageName="icon-align-bottom-left",
            actionName="Align Bottom Left",
            actionCallback=self.alignBottomLeftCallback
        )
        w.alignBottomCenterButton = IconButton(
            imageName="icon-align-bottom-center",
            actionName="Align Bottom Center",
            actionCallback=self.alignBottomCenterCallback
        )
        w.alignBottomRightButton = IconButton(
            imageName="icon-align-bottom-right",
            actionName="Align Bottom Right",
            actionCallback=self.alignBottomRightCallback
        )

        self.w.line2 = vanilla.HorizontalLine("auto")

        # Align To Metrics

        w.alignAscenderButton = IconButton(
            imageName="icon-align-ascender",
            actionName="Align to Ascender",
            actionCallback=self.alignAscenderCallback
        )
        w.alignCapHeightButton = IconButton(
            imageName="icon-align-cap-height",
            actionName="Align to Cap Height",
            actionCallback=self.alignCapHeightCallback
        )
        w.alignXHeightButton = IconButton(
            imageName="icon-align-x-height",
            actionName="Align to x-Height",
            actionCallback=self.alignXHeightCallback
        )

        w.alignBaselineButton = IconButton(
            imageName="icon-align-baseline",
            actionName="Align to Baseline",
            actionCallback=self.alignBaselineCallback
        )
        w.alignDescenderButton = IconButton(
            imageName="icon-align-descender",
            actionName="Align to Descender",
            actionCallback=self.alignDescenderCallback
        )
        w.centerOnWidthButton = IconButton(
            imageName="icon-center-on-width",
            actionName="Center on Width",
            actionCallback=self.centerOnWidthCallback
        )

        self.w.line3 = vanilla.HorizontalLine("auto")

        # Distribute Vertical

        w.distributeVerticalSpacingButton = IconButton(
            imageName="icon-distribute-vertical-spacing",
            actionName="Distribute Vertical Spacing",
            actionCallback=self.distributeVerticalSpacingCallback
        )
        w.distributeTopsButton = IconButton(
            imageName="icon-distribute-tops",
            actionName="Distribute Tops",
            actionCallback=self.distributeTopsCallback
        )
        w.distributeYCentersButton = IconButton(
            imageName="icon-distribute-y-centers",
            actionName="Distribute Y Centers",
            actionCallback=self.distributeYCentersCallback
        )
        w.distributeBottomsButton = IconButton(
            imageName="icon-distribute-bottoms",
            actionName="Distribute Bottoms",
            actionCallback=self.distributeBottomsCallback
        )

        # Distribute Horizontal

        w.distributeHorizontalSpacingButton = IconButton(
            imageName="icon-distribute-horizontal-spacing",
            actionName="Distribute Horizontal Spacing",
            actionCallback=self.distributeHorizontalSpacingCallback
        )
        w.distributeLeftsButton = IconButton(
            imageName="icon-distribute-lefts",
            actionName="Distribute Lefts",
            actionCallback=self.distributeLeftsCallback
        )
        w.distributeXCentersButton = IconButton(
            imageName="icon-distribute-x-centers",
            actionName="Distribute X Centers",
            actionCallback=self.distributeXCentersCallback
        )
        w.distributeRightsButton = IconButton(
            imageName="icon-distribute-rights",
            actionName="Distribute Rights",
            actionCallback=self.distributeRightsCallback
        )

        # Distribute Random

        w.distributeRandomSpacingButton = IconButton(
            imageName="icon-distribute-random-spacing",
            actionName="Distribute Spacing Randomly",
            actionCallback=self.distributeRandomSpacingCallback
        )

        rules = [

            # Horizontal

            "H:|-margin-"
                "[alignTopButton(==iconButtonWidth)]"
                "[alignYCenterButton(==iconButtonWidth)]"
                "[alignBottomButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-"
                "[alignLeftButton(==iconButtonWidth)]"
                "[alignXCenterButton(==iconButtonWidth)]"
                "[alignRightButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-[line1]-margin-|",

            "H:|-margin-"
                "[alignTopLeftButton(==iconButtonWidth)]"
                "[alignTopCenterButton(==iconButtonWidth)]"
                "[alignTopRightButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-"
                "[alignCenterLeftButton(==iconButtonWidth)]"
                "[alignCenterCenterButton(==iconButtonWidth)]"
                "[alignCenterRightButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-"
                "[alignBottomLeftButton(==iconButtonWidth)]"
                "[alignBottomCenterButton(==iconButtonWidth)]"
                "[alignBottomRightButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-[line2]-margin-|",

            "H:|-margin-"
                "[alignAscenderButton(==iconButtonWidth)]"
                "[alignCapHeightButton(==iconButtonWidth)]"
                "[alignXHeightButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-"
                "[alignBaselineButton(==iconButtonWidth)]"
                "[alignDescenderButton(==iconButtonWidth)]"
                "[centerOnWidthButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-[line3]-margin-|",

            "H:|-margin-"
                "[distributeVerticalSpacingButton(==iconButtonWidth)]"
                "[distributeHorizontalSpacingButton(==iconButtonWidth)]"
                "[distributeRandomSpacingButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-"
                "[distributeTopsButton(==iconButtonWidth)]"
                "[distributeXCentersButton(==iconButtonWidth)]"
                "[distributeBottomsButton(==iconButtonWidth)]"
                "-margin-|",

            "H:|-margin-"
                "[distributeLeftsButton(==iconButtonWidth)]"
                "[distributeYCentersButton(==iconButtonWidth)]"
                "[distributeRightsButton(==iconButtonWidth)]"
                "-margin-|",

            # Vertical


            "V:|"
                "-margin-"
                "[alignTopButton(==iconButtonHeight)]"
                "[alignLeftButton(==iconButtonHeight)]"
                "-iconPadding-[line1]",
            "V:|"
                "-margin-"
                "[alignYCenterButton(==iconButtonHeight)]"
                "[alignXCenterButton(==iconButtonHeight)]"
                "-iconPadding-[line1]",
            "V:|"
                "-margin-"
                "[alignBottomButton(==iconButtonHeight)]"
                "[alignRightButton(==iconButtonHeight)]"
                "-iconPadding-[line1]",

            "V:[line1]"
                "-iconPadding-"
                "[alignTopLeftButton(==iconButtonHeight)]"
                "[alignCenterLeftButton(==iconButtonHeight)]"
                "[alignBottomLeftButton(==iconButtonHeight)]"
                "-iconPadding-[line2]",

            "V:[line1]"
                "-iconPadding-"
                "[alignTopCenterButton(==iconButtonHeight)]"
                "[alignCenterCenterButton(==iconButtonHeight)]"
                "[alignBottomCenterButton(==iconButtonHeight)]"
                "-iconPadding-[line2]",

            "V:[line1]"
                "-iconPadding-"
                "[alignTopRightButton(==iconButtonHeight)]"
                "[alignCenterRightButton(==iconButtonHeight)]"
                "[alignBottomRightButton(==iconButtonHeight)]"
                "-iconPadding-[line2]",

            "V:[line2]",

            "V:[line2]"
                "-iconPadding-"
                "[alignAscenderButton(==iconButtonHeight)]"
                "[alignBaselineButton(==iconButtonHeight)]"
                "-iconPadding-[line3]",

            "V:[line2]"
                "-iconPadding-"
                "[alignCapHeightButton(==iconButtonHeight)]"
                "[alignDescenderButton(==iconButtonHeight)]"
                "-iconPadding-[line3]",

            "V:[line2]"
                "-iconPadding-"
                "[alignXHeightButton(==iconButtonHeight)]"
                "[centerOnWidthButton(==iconButtonHeight)]"
                "-iconPadding-[line3]",

            "V:[line3]",

            "V:[line3]"
                "-iconPadding-"
                "[distributeVerticalSpacingButton(==iconButtonHeight)]"
                "[distributeTopsButton(==iconButtonHeight)]"
                "[distributeLeftsButton(==iconButtonHeight)]"
                "-margin-|",

            "V:[line3]"
                "-iconPadding-"
                "[distributeHorizontalSpacingButton(==iconButtonHeight)]"
                "[distributeYCentersButton(==iconButtonHeight)]"
                "[distributeXCentersButton(==iconButtonHeight)]"
                "-margin-|",

            "V:[line3]"
                "-iconPadding-"
                "[distributeRandomSpacingButton(==iconButtonHeight)]"
                "[distributeBottomsButton(==iconButtonHeight)]"
                "[distributeRightsButton(==iconButtonHeight)]"
                "-margin-|"
        ]
        return rules

    # -----
    # Align
    # -----

    # Horizontal

    def alignTopCallback(self, glyph):
        self._align(glyph, [self._alignTop])

    def alignYCenterCallback(self, glyph):
        self._align(glyph, [self._alignYCenter])

    def alignBottomCallback(self, glyph):
        self._align(glyph, [self._alignBottom])

    # Vertical

    def alignLeftCallback(self, glyph):
        self._align(glyph, [self._alignLeft])

    def alignXCenterCallback(self, glyph):
        self._align(glyph, [self._alignXCenter])

    def alignRightCallback(self, glyph):
        self._align(glyph, [self._alignRight])

    # Both

    def alignTopLeftCallback(self, glyph):
        self._align(glyph, [self._alignTop, self._alignLeft])

    def alignTopCenterCallback(self, glyph):
        self._align(glyph, [self._alignTop, self._alignXCenter])

    def alignTopRightCallback(self, glyph):
        self._align(glyph, [self._alignTop, self._alignRight])

    def alignCenterLeftCallback(self, glyph):
        self._align(glyph, [self._alignYCenter, self._alignLeft])

    def alignCenterCenterCallback(self, glyph):
        self._align(glyph, [self._alignYCenter, self._alignXCenter])

    def alignCenterRightCallback(self, glyph):
        self._align(glyph, [self._alignYCenter, self._alignRight])

    def alignBottomLeftCallback(self, glyph):
        self._align(glyph, [self._alignBottom, self._alignLeft])

    def alignBottomCenterCallback(self, glyph):
        self._align(glyph, [self._alignBottom, self._alignXCenter])

    def alignBottomRightCallback(self, glyph):
        self._align(glyph, [self._alignBottom, self._alignRight])

    def _align(self, glyph, methods):
        rects, selectedContours, selectedBPoints = getSelection(glyph)
        if len(rects) < 2:
            return
        for method in methods:
            method(rects, selectedContours, selectedBPoints)
        for bPoint in selectedBPoints:
            bPoint.round()
        for contour in selectedContours:
            contour.round()

    def _alignTop(self, rects, selectedContours, selectedBPoints):
        top = getEdgeCoordinate(rects, 3, max)
        for bPoint in selectedBPoints:
            d = top - bPoint.anchor[1]
            bPoint.moveBy((0, d))
        for contour in selectedContours:
            d = top - contour.bounds[3]
            contour.moveBy((0, d))

    def _alignBottom(self, rects, selectedContours, selectedBPoints):
        bottom = getEdgeCoordinate(rects, 1, min)
        for bPoint in selectedBPoints:
            d = bottom - bPoint.anchor[1]
            bPoint.moveBy((0, d))
        for contour in selectedContours:
            d = bottom - contour.bounds[1]
            contour.moveBy((0, d))

    def _alignYCenter(self, rects, selectedContours, selectedBPoints):
        y1 = getEdgeCoordinate(rects, 1, min)
        y2 = getEdgeCoordinate(rects, 3, max)
        center = (y1 + y2) / 2
        for bPoint in selectedBPoints:
            d = center - bPoint.anchor[1]
            bPoint.moveBy((0, d))
        for contour in selectedContours:
            d = center - rectCenter(contour.bounds)[1]
            contour.moveBy((0, d))

    def _alignLeft(self, rects, selectedContours, selectedBPoints):
        left = getEdgeCoordinate(rects, 0, min)
        for bPoint in selectedBPoints:
            d = left - bPoint.anchor[0]
            bPoint.moveBy((d, 0))
        for contour in selectedContours:
            d = left - contour.bounds[0]
            contour.moveBy((d, 0))

    def _alignRight(self, rects, selectedContours, selectedBPoints):
        right = getEdgeCoordinate(rects, 2, max)
        for bPoint in selectedBPoints:
            d = right - bPoint.anchor[0]
            bPoint.moveBy((d, 0))
        for contour in selectedContours:
            d = right - contour.bounds[2]
            contour.moveBy((d, 0))

    def _alignXCenter(self, rects, selectedContours, selectedBPoints):
        x1 = getEdgeCoordinate(rects, 0, min)
        x2 = getEdgeCoordinate(rects, 2, max)
        center = (x1 + x2) / 2
        for bPoint in selectedBPoints:
            d = center - bPoint.anchor[0]
            bPoint.moveBy((d, 0))
        for contour in selectedContours:
            d = center - rectCenter(contour.bounds)[0]
            contour.moveBy((d, 0))

    # Metrics

    def alignAscenderCallback(self, glyph):
        self._alignToMetric(glyph, glyph.font.info.ascender)

    def alignCapHeightCallback(self, glyph):
        self._alignToMetric(glyph, glyph.font.info.capHeight)

    def alignXHeightCallback(self, glyph):
        self._alignToMetric(glyph, glyph.font.info.xHeight)

    def alignBaselineCallback(self, glyph):
        self._alignToMetric(glyph, 0)

    def alignDescenderCallback(self, glyph):
        self._alignToMetric(glyph, glyph.font.info.descender)

    def centerOnWidthCallback(self, glyph):
        rects, selectedContours, selectedBPoints = getSelection(glyph)
        left = getEdgeCoordinate(rects, 0, min)
        right = getEdgeCoordinate(rects, 2, max)
        selectionWidth = right - left
        glyphWidth = glyph.width
        diff = glyphWidth - selectionWidth
        margin = int(round(diff / 2))
        offset = margin - left
        for bPoint in selectedBPoints:
            bPoint.moveBy((offset, 0))
        for contour in selectedContours:
            contour.moveBy((offset, 0))

    def _alignToMetric(self, glyph, metric):
        rects, selectedContours, selectedBPoints = getSelection(glyph)
        top = getEdgeCoordinate(rects, 3, max)
        bottom = getEdgeCoordinate(rects, 1, min)
        topDiff = abs(top - metric)
        bottomDiff = abs(metric - bottom)
        move = 0
        if top > metric and bottom < metric:
            if topDiff < bottomDiff:
                move = -topDiff
            else:
                move = bottomDiff
        elif top < metric:
            move = topDiff
        elif bottom > metric:
            move = -bottomDiff
        for bPoint in selectedBPoints:
            bPoint.moveBy((0, move))
        for contour in selectedContours:
            contour.moveBy((0, move))

    # ----------
    # Distribute
    # ----------

    # Vertical

    def distributeVerticalSpacingCallback(self, glyph):
        self._distributeSpacing(glyph, 1)

    def distributeTopsCallback(self, glyph):
        self._distribute(glyph, [self._distributeTop])

    def distributeYCentersCallback(self, glyph):
        self._distribute(glyph, [self._distributeYCenter])

    def distributeBottomsCallback(self, glyph):
        self._distribute(glyph, [self._distributeBottom])

    # Distribute Horizontal

    def distributeHorizontalSpacingCallback(self, glyph):
        self._distributeSpacing(glyph, 0)

    def distributeLeftsCallback(self, glyph):
        self._distribute(glyph, [self._distributeLeft])

    def distributeXCentersCallback(self, glyph):
        self._distribute(glyph, [self._distributeXCenter])

    def distributeRightsCallback(self, glyph):
        self._distribute(glyph, [self._distributeRight])

    # Distribute Random

    def distributeRandomSpacingCallback(self, glyph):
        print("Random spacing doesn't work yet. I just made this icon to make the interface look even.")

    # Guts

    def _distribute(self, glyph, methods):
        rects, selectedContours, selectedBPoints = getSelection(glyph)
        if len(rects) < 3:
            return
        for method in methods:
            method(rects, selectedContours, selectedBPoints)
        for bPoint in selectedBPoints:
            bPoint.round()
        for contour in selectedContours:
            contour.round()

    def _distributeTop(self, rects, selectedContours, selectedBPoints):
        self._distributeEdge(1, rects, selectedContours, selectedBPoints)

    def _distributeBottom(self, rects, selectedContours, selectedBPoints):
        self._distributeEdge(3, rects, selectedContours, selectedBPoints)

    def _distributeYCenter(self, rects, selectedContours, selectedBPoints):
        self._distributeCenter(1, rects, selectedContours, selectedBPoints)

    def _distributeLeft(self, rects, selectedContours, selectedBPoints):
        self._distributeEdge(0, rects, selectedContours, selectedBPoints)

    def _distributeRight(self, rects, selectedContours, selectedBPoints):
        self._distributeEdge(2, rects, selectedContours, selectedBPoints)

    def _distributeXCenter(self, rects, selectedContours, selectedBPoints):
        self._distributeCenter(0, rects, selectedContours, selectedBPoints)

    def _distributeEdge(self, index, rects, selectedContours, selectedBPoints):
        edge1 = getEdgeCoordinate(rects, index, min)
        edge2 = getEdgeCoordinate(rects, index, max)
        space = edge2 - edge1
        if space:
            ordered = [(bPoint.anchor[index % 2], bPoint.anchor, bPoint) for bPoint in selectedBPoints]
            ordered += [(contour.bounds[index], contour.bounds, contour) for contour in selectedContours]
            ordered.sort()
            interval = space / (len(ordered) - 1)
            for i, (pos, disambiguate, obj) in enumerate(ordered):
                e = edge1 + (i * interval)
                d = e - pos
                if index in (0, 2):
                    obj.moveBy((d, 0))
                else:
                    obj.moveBy((0, d))

    def _distributeCenter(self, index, rects, selectedContours, selectedBPoints):
        ordered = [(bPoint.anchor[index], (bPoint.anchor[0], bPoint.anchor[1], bPoint.anchor[0], bPoint.anchor[1]), bPoint) for bPoint in selectedBPoints]
        ordered += [(contour.bounds[index], contour.bounds, contour) for contour in selectedContours]
        ordered.sort()
        side1 = ordered[0]
        side2 = ordered[-1]
        center1 = rectCenter(side1[1])[index]
        center2 = rectCenter(side2[1])[index]
        space = center2 - center1
        if not space:
            return
        step = space / (len(ordered) - 1)
        prev = center1
        for pos, bounds, obj in ordered[1:-1]:
            alignTo = prev + step
            d = alignTo - rectCenter(bounds)[index]
            if index == 0:
                obj.moveBy((d, 0))
            else:
                obj.moveBy((0, d))
            prev = alignTo

    def _distributeSpacing(self, glyph, index):
        rects, selectedContours, selectedBPoints = getSelection(glyph)
        if len(rects) < 3:
            return
        widths = []
        heights = []
        edgeRect = None
        for rect in rects:
            xMin, yMin, xMax, yMax = rect
            widths.append(xMax - xMin)
            heights.append(yMax - yMin)
            if edgeRect is None:
                edgeRect = rect
            else:
                edgeRect = unionRect(edgeRect, rect)
        objectWidth = sum(widths)
        objectHeight = sum(heights)
        xMin, yMin, xMax, yMax = edgeRect
        overallWidth = xMax - xMin
        overallHeight = yMax - yMin
        availableXSpace = overallWidth - objectWidth
        availableYSpace = overallHeight - objectHeight
        xSpace = availableXSpace / (len(rects) - 1)
        ySpace = availableYSpace / (len(rects) - 1)
        spaceBetweenObjects = (xSpace, ySpace)[index]
        ordered = [(bPoint.anchor[index], (bPoint.anchor[0], bPoint.anchor[1], bPoint.anchor[0], bPoint.anchor[1]), bPoint) for bPoint in selectedBPoints]
        ordered += [(contour.bounds[index], contour.bounds, contour) for contour in selectedContours]
        ordered.sort()
        prevEdge = None
        for pos, bounds, obj in ordered[:-1]:
            xMin, yMin, xMax, yMax = bounds
            width = xMax - xMin
            height = yMax - yMin
            size = (width, height)[index]
            if prevEdge is None:
                newPos = (xMin, yMin)[index]
            else:
                newPos = prevEdge + spaceBetweenObjects
            d = newPos - pos
            if d != 0:
                if index == 0:
                    obj.moveBy((d, 0))
                else:
                    obj.moveBy((0, d))
            prevEdge = newPos + size
        for bPoint in selectedBPoints:
            bPoint.round()
        for contour in selectedContours:
            contour.round()

# ---------------
# Glyph Selection
# ---------------

def getSelection(glyph):
    rects = []
    selectedContours = []
    selectedBPoints = []
    if glyph is not None:
        for contour in glyph:
            if len(contour) == len(contour.selectedSegments):
                rects.append(contour.bounds)
                selectedContours.append(contour)
            else:
                for bPoint in contour.selectedBPoints:
                    x, y = bPoint.anchor
                    rects.append((x, y, x, y))
                    selectedBPoints.append(bPoint)
    if not selectedContours and not selectedBPoints:
        for contour in glyph:
            rects.append(contour.bounds)
            selectedContours.append(contour)
    return rects, selectedContours, selectedBPoints

def getEdgeCoordinate(rects, index, func):
    l = [rect[index] for rect in rects]
    return func(l)
