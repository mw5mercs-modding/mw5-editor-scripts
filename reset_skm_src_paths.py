import unreal

def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o

def update_src(asset_path):
	asset = get_asset(asset_path)
	unreal.log(asset_path)
	unreal.log(asset.get_editor_property('asset_import_data').get_editor_property('source_data').to_tuple())
	unreal.log(asset.get_editor_property('asset_import_data').get_first_filename())
	fbx_path = 'E:/Games/MechWarrior5Editor/MW5Mercs/Plugins/YetAnotherMechlab/Content/Mechs/Thunderbolt/Model/' + asset_path.split('.')[-1] + '.FBX'
	unreal.log(fbx_path)
	asset.get_editor_property('asset_import_data').scripted_add_filename(fbx_path, 0, 'Source File (Geometry and Skinning Weights)')

asset_location = '/YetAnotherMechlab/Mechs/Thunderbolt/Model/'
with unreal.ScopedEditorTransaction("CollectEquipmentMetadata Script") as trans:
	assets = unreal.EditorAssetLibrary.list_assets(asset_location, True)
	for asset_path in assets:
		if 'SKM' in asset_path:
			update_src(asset_path)
	#update_src('/YetAnotherClanMech/Objects/Mechs/Phoenixhawk_IIC/Model/Weapons/Weapon_Mech_PXH_Head_BH1_AC10_SKM.Weapon_Mech_PXH_Head_BH1_AC10_SKM')
