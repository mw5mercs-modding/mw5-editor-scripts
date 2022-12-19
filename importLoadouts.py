import unreal
import json
import os

####### SCRIPT CONFIG ##############
ia_loadouts_path = 'C:/Users/trueg/AppData/Local/MW5Mercs/Saved/SavedLoadouts/InstantAction.json'
asset_path = '/YetAnotherClanMech/Objects/Mechs/Cougar'
#tmp_file = 'D:/Downloads/MW5/tmp/loadout.json'
tmp_folder = 'D:/Downloads/MW5/tmp/loadouts'
####### /SCRIPT CONFIG ##############

def get_ref_dir(ref):
	"""
	Strip the last component of an asset reference.
	"""
	return '/'.join(ref.split('/')[0:-1])


def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o

def import_loadout(asset_location, import_path):
	# sadly the import task does not work like this. Need to figure out how to do it instead.
	task = unreal.AssetImportTask()
	task.filename = import_path
	task.destination_path = get_ref_dir(asset_location)
	task.destination_name = asset_location.split('.')[-1]
	task.automated = True
	task.replace_existing = True
	task.replace_existing_settings = False
	task.factory = unreal.ReimportDataTableFactory()
	task.factory.automated_import_settings  = unreal.CSVImportSettings()
	task.factory.automated_import_settings.import_row_struct = unreal.MechLoadout
		
	unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

def parse_ia_loadouts():
	loadouts = {}
	with open(ia_loadouts_path) as f:
		data = json.load(f)
		#unreal.log(data)
		for loadout_data in data['Loadouts']:
			loadout = loadout_data['mechLoadout']
			mda = loadout['mechDataAssetId']['iD'].split(':')[-1]
			loadout['customName'] = ''
			loadouts[mda] = loadout
	return loadouts

def write_loadout_to_file(loadout, file_path):
	str = json.dumps(loadout)
	
	# replace the YAEC Clan DHS kit with the standard one for compatibility
	str.replace('MWHeatSinkDataAsset:CLAN_DHS_KIT', 'MWHeatSinkDataAsset:Cooling_diss100')

	with open(file_path, 'w') as json_tmp:
		json_tmp.write(str)

with unreal.ScopedEditorTransaction("Rename Script Transaction") as trans:
	os.mkdir(tmp_folder)

	loadouts = parse_ia_loadouts()
	for mda in loadouts:
		unreal.log("Found loadout for mda " + mda)

	asset_names = unreal.EditorAssetLibrary.list_assets(asset_path)
	for asset_name in asset_names:
		if 'Loadout' in asset_name:
			loadout_asset = get_asset(asset_name)
			if isinstance(loadout_asset, unreal.MWMechLoadoutAsset):
				unreal.log('Found loadout: ' + asset_name)
				mda = str(loadout_asset.get_editor_property('mech_loadout').get_editor_property('mech_data_asset_id').id.primary_asset_name)
				if mda in loadouts:
					unreal.log('Found IA loadout for ' + mda)
					tmp_file = tmp_folder + '/' + mda + '.json'
					write_loadout_to_file(loadouts[mda], tmp_file)
					#import_loadout(asset_name, tmp_file) # does not work yet
					loadout_asset.set_editor_property('reimport_file_name', tmp_file)
				else:
					unreal.log('No IA loadout found for ' + mda)
