import unreal

def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o
	
def get_primary_asset_id(path):
	return unreal.SystemLibrary.get_primary_asset_id_from_object(unreal.AssetRegistryHelpers.get_asset(unreal.EditorAssetLibrary.find_asset_data(path)))

def clone_variant(srcVariant, destVariant):
	src_location = "/YetAnotherClanMech/Objects/Mechs/Phoenixhawk_IIC/"
	#src_location = "/SpecialVariants/Objects/Mechs/Warhammer/"
	use_sub_folders = False
	dest_location = src_location

	with unreal.ScopedEditorTransaction("Clone Variant Script") as trans:
		mda_path = src_location
		loadout_path = src_location
		uc_path = src_location
		if use_sub_folders:
			mda_path = mda_path + 'MDA/'
			loadout_path = loadout_path + 'Loadout/'
			uc_path = uc_path + 'UnitCard/'
			
		unreal.EditorAssetLibrary.duplicate_asset(mda_path + srcVariant + "_MDA", dest_location + destVariant + "_MDA")
		unreal.EditorAssetLibrary.duplicate_asset(uc_path + srcVariant + "_UnitCard", dest_location + destVariant + "_UnitCard")
		unreal.EditorAssetLibrary.duplicate_asset(loadout_path + srcVariant + "_Loadout", dest_location + destVariant + "_Loadout")
		destMda = get_asset(mda_path + destVariant + "_MDA")
		destLoadout = get_asset(loadout_path + destVariant + "_Loadout")
		destCard = get_asset(uc_path + destVariant + "_UnitCard")
		
		#unreal.log(destMda.mech_data.default_mech)
		#unreal.log(dir(destMda.mech_data.default_mech))
		#unreal.log(destLoadout)
		#unreal.log(dir(destLoadout))
		#unreal.log(get_primary_asset_id(dest_location + destVariant + "_Loadout"))
		destMda.mech_data.set_editor_property("variant_name", destVariant);
		destMda.mech_data.default_mech.set_editor_property("id", get_primary_asset_id(dest_location + destVariant + "_Loadout"))

		destLoadout.mech_loadout.mech_data_asset_id.set_editor_property("id", get_primary_asset_id(dest_location + destVariant + "_MDA"))
		destCard.unit_card.set_editor_property("mech_loadout_template", destMda.mech_data.default_mech)
		
		#unreal.log(dir(o.mech_data))
		#unreal.log(o.mech_data.variant_name)
		#unreal.log(o.mech_data.default_mech)
		#unreal.log(get_primary_asset_id(asset_location + srcVariant + "_Loadout"))


srcVariant = "PXH-IIC-2"
destVariants = [
	"PXH-IIC-3",
	"PXH-IIC-4",
	"PXH-IIC-5",
	"PXH-IIC-6",
	"PXH-IIC-7",
	"PXH-IIC-8",
	"PXH-IIC-9",
	"PXH-IIC-10"
]

for v in destVariants:
	clone_variant(srcVariant, v)
