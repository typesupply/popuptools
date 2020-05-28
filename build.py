# -----------------
# Extension Details
# -----------------

name = "Pop Up Tools"
version = "0.1"
developer = "Type Supply"
developerURL = "http://typesupply.com"
roboFontVersion = "3.3"
pycOnly = False
menuItems = [
    dict(
        path="menu_alignDistribute.py",
        preferredName="Align & Distribute",
        shortKey=("a", "control")
    ),
	dict(
        path="menu_boolean.py",
        preferredName="Boolean Operations",
        shortKey=("o", "control")
    ),
	dict(
        path="menu_transform.py",
        preferredName="Transformations",
        shortKey=("t", "control")
    ),
]
mainScript = "launch.py"
launchAtStartUp = False
installAfterBuild = True

# ----------------------
# Don't edit below here.
# ----------------------

from AppKit import *
import os
import shutil
from mojo.extensions import ExtensionBundle

# Convert short key modifiers.

modifierMap = {
	"command": NSCommandKeyMask,
    "control": NSControlKeyMask,
    "option": NSAlternateKeyMask,
    "shift": NSShiftKeyMask,
    "capslock": NSAlphaShiftKeyMask,
}

for menuItem in menuItems:
	shortKey = menuItem.get("shortKey")
	if isinstance(shortKey, tuple):
		shortKey = list(shortKey)
		character = shortKey.pop(0)
		converted = [modifierMap.get(modifier) for modifier in shortKey]
		menuItem["shortKey"] = tuple(converted + [character])

# Make the various paths.

basePath = os.path.dirname(__file__)
sourcePath = os.path.join(basePath, "source")
libPath = os.path.join(sourcePath, "code")
licensePath = os.path.join(basePath, "license.txt")
requirementsPath = os.path.join(basePath, "requirements.txt")
resourcesPath = os.path.join(sourcePath, "resources")
if not os.path.exists(resourcesPath):
	resourcesPath = None
extensionFile = "%s.roboFontExt" % name
buildPath = os.path.join(basePath, "build")
extensionPath = os.path.join(buildPath, extensionFile)

# Build the extension.

B = ExtensionBundle()
B.name = name
B.developer = developer
B.developerURL = developerURL
B.version = version
B.launchAtStartUp = launchAtStartUp
B.mainScript = mainScript
docPath = os.path.join(sourcePath, "documentation")
haveDocumentation = False
if os.path.exists(os.path.join(docPath, "index.html")):
	haveDocumentation = True
elif os.path.exists(os.path.join(docPath, "index.md")):
	haveDocumentation = True
if not haveDocumentation:
	docPath = None
B.html = haveDocumentation
B.requiresVersionMajor = roboFontVersion.split(".")[0]
B.requiresVersionMinor = roboFontVersion.split(".")[1]
B.addToMenu = menuItems
with open(licensePath) as license:
    B.license = license.read()
with open(requirementsPath) as requirements:
    B.requirements = requirements.read()
print("Building extension...", end=" ")
v = B.save(extensionPath, libPath=libPath, pycOnly=pycOnly, htmlPath=docPath, resourcesPath=resourcesPath)
print("done!")
errors = B.validationErrors()
if errors:
	print("Uh oh! There were errors:")
	print(errors)

# Install the extension.

if installAfterBuild:
	print("Installing extension...", end=" ")
	installDirectory = os.path.expanduser("~/Library/Application Support/RoboFont/plugins")
	installPath = os.path.join(installDirectory, extensionFile)
	if os.path.exists(installPath):
		shutil.rmtree(installPath)
	shutil.copytree(extensionPath, installPath)
	print("done!")
	print("RoboFont must now be restarted.")
