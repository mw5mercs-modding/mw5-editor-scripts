import unreal

asset_location = "/YetAnotherClanMech/Objects/Mechs/BlackLanner/Target/Textures/"

with unreal.ScopedEditorTransaction("Rename Script Transaction") as trans:
	asset_names = unreal.EditorAssetLibrary.list_assets(asset_location)
	for asset_name in asset_names:
		#if asset_name.startswith("Cataphract"):
		new_name = asset_name.rpartition(".")[2].replace("Cataphract", "BlackLanner")
		new_path = asset_location + new_name + "." + new_name
		unreal.log(" Renaming {} into {}".format(asset_name, new_path))
		unreal.EditorAssetLibrary.rename_asset(asset_name, new_path)
	unreal.log("Done!");
