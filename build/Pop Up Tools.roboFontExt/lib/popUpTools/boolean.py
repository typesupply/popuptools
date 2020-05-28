import vanilla
from .base import BaseActionWindowController, IconButton
from mojo import tools as booleanOperations


class BooleanOperationsController(BaseActionWindowController):

    def buildInterface(self, w):
        w.unionButton = IconButton(
            imageName="icon-booleanOperation-union",
            actionName="Union",
            actionCallback=self.unionActionCallback
        )
        w.differenceButton = IconButton(
            imageName="icon-booleanOperation-difference",
            actionName="Difference",
            actionCallback=self.differenceActionCallback
        )
        w.intersectionButton = IconButton(
            imageName="icon-booleanOperation-intersection",
            actionName="Intersection",
            actionCallback=self.intersectionActionCallback
        )
        w.xorButton = IconButton(
            imageName="icon-booleanOperation-xor",
            actionName="Xor",
            actionCallback=self.xorActionCallback
        )
        rules = [
            "H:|-margin-"
                "[unionButton(==iconButtonWidth)]"
                "[differenceButton(==iconButtonWidth)]"
                "[intersectionButton(==iconButtonWidth)]"
                "[xorButton(==iconButtonWidth)]"
                "-margin-|",

            "V:|-margin-[unionButton(==iconButtonHeight)]-margin-|",
            "V:|-margin-[differenceButton(==iconButtonHeight)]-margin-|",
            "V:|-margin-[intersectionButton(==iconButtonHeight)]-margin-|",
            "V:|-margin-[xorButton(==iconButtonHeight)]-margin-|"
        ]
        return rules

    def _getContours(self, glyph):
        contours = glyph.selectedContours
        if not contours:
            contours = glyph.contours
        subjectContours = contours[:1]
        clipContours = contours[1:]
        return subjectContours, clipContours

    def _performAction(self, glyph, action):
        subjectContours, clipContours = self._getContours(glyph)
        action(glyph, subjectContours, clipContours)

    def unionActionCallback(self, glyph):
        self._performAction(glyph, booleanOperations.union)

    def differenceActionCallback(self, glyph):
        self._performAction(glyph, booleanOperations.difference)

    def intersectionActionCallback(self, glyph):
        self._performAction(glyph, booleanOperations.intersection)

    def xorActionCallback(self, glyph):
        self._performAction(glyph, booleanOperations.xor)