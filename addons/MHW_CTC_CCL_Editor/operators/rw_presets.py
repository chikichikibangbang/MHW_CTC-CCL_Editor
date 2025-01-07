#Author: NSA Cloud
import json
import os
import re
import bpy

from MHW_CTC_CCL_Editor.addons.MHW_CTC_CCL_Editor.operators.general_function import showErrorMessageBox, textColors, raiseWarning


def saveAsPreset(selection, presetName):
	if len(selection) == 1:
		activeObj = selection[0]
		ctcObjType = activeObj.get("TYPE", None)
		if not re.search(r'^[\w,\s-]+\.[A-Za-z]{3}$',
						 presetName) and not ".." in presetName:  # Check that the preset name contains no invalid characters for a file name
			presetDict = {}
			folderPath = None
			variableList = []

			if ctcObjType == "CTC_CHAIN":
				folderPath = "CTCChain"
				presetDict["presetType"] = "CTC_CHAIN"
				variableList = activeObj.ctc_settings.items()
			elif ctcObjType == "CTC_NODE":
				folderPath = "CTCNode"
				presetDict["presetType"] = "CTC_NODE"
				variableList = activeObj.ctc_node.items()
			# elif ctcObjType == "CCL_COLLISION":
			# 	folderPath = "CCLCollision"
			# 	presetDict["presetType"] = "CCL_COLLISION"
			# 	variableList = activeObj.ctc_node.items()
			else:
				showErrorMessageBox("Selected object can not be made into a preset.")

			if variableList != []:
				for key, value in variableList:

					if type(value).__name__ == "IDPropertyArray":
						presetDict[key] = value.to_list()
					else:
						presetDict[key] = value

				# Find ctc header in scene and get the version
				# ctcHeader = findHeaderObj()

				jsonPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]), "presets",
										folderPath, presetName + ".json")

				# print(presetDict)#debug
				try:
					os.makedirs(os.path.split(jsonPath)[0])
				except:
					pass
				with open(jsonPath, 'w', encoding='utf-8') as f:
					json.dump(presetDict, f, ensure_ascii=False, indent=4)
					print(textColors.OKGREEN + "Saved preset to " + str(jsonPath) + textColors.ENDC)
					return True
		else:
			showErrorMessageBox("Invalid preset file name.")
	else:
		showErrorMessageBox("A ctc object must be selected when saving a preset.")

def readPresetJSON(filepath, activeObj):
	try:
		with open(filepath) as jsonFile:
			jsonDict = json.load(jsonFile)

	except Exception as err:
		showErrorMessageBox("Failed to read json file. \n" + str(err))
		return False

	if jsonDict["presetType"] != activeObj.get("TYPE", None):
		showErrorMessageBox("Preset type does not match selected object")
		return False
	propertyGroup = {}

	if jsonDict["presetType"] == "CTC_CHAIN":
		propertyGroup = activeObj.ctc_settings

	elif jsonDict["presetType"] == "CTC_NODE":
		propertyGroup = activeObj.ctc_node
	else:
		showErrorMessageBox("Preset type is not supported")
		return False
	print("Applying preset to " + activeObj.name)

	for key in propertyGroup.keys():
		try:
			propertyGroup[key] = jsonDict[key]
		except:
			raiseWarning("Preset is missing key " + str(key) + ", cannot set value on active object.")
	return True


def reloadPresets(folderPath):
	presetsPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]),"presets")
	global presetList
	presetList = []
	relPathStart = os.path.join(presetsPath,folderPath)
	if os.path.exists(relPathStart):
		for entry in os.scandir(relPathStart):
			if entry.name.endswith(".json") and entry.is_file():
				# print(os.path.splitext(entry.name)[0].encode('utf-8'))
				presetList.append((os.path.relpath(os.path.join(relPathStart,entry),start = presetsPath),os.path.splitext(entry.name)[0],""))
	#print("Loading " + folderPath + " presets...")
	#print("DEBUG:" + str(presetList)+"\n")#debug
	# print(presetList)
	return presetList

