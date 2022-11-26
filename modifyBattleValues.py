import unreal

def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o
	
def get_primary_asset_id(path):
	return unreal.SystemLibrary.get_primary_asset_id_from_object(unreal.AssetRegistryHelpers.get_asset(unreal.EditorAssetLibrary.find_asset_data(path)))

#src_location = "/YetAnotherClanMech/Objects/Mechs/"
src_location = "/YetAnotherClanMech/Objects/Mechs/Phoenixhawk_IIC/"

with unreal.ScopedEditorTransaction("Clone Variant Script") as trans:
	assets = unreal.EditorAssetLibrary.list_assets(src_location, True)
	for asset_path in assets:
		asset = get_asset(asset_path)
		try:
			if "MWUnitCardAsset" in str(type(asset)):
				unreal.log(asset.get_editor_property("unit_card").get_editor_property("battle_value"))
				unreal.log(round(asset.get_editor_property("unit_card").get_editor_property("battle_value") * 0.7))
				asset.get_editor_property("unit_card").set_editor_property("battle_value", round(asset.get_editor_property("unit_card").get_editor_property("battle_value") * 0.7))
		except:
			pass