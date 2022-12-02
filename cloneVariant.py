import unreal

########## CHANGE ME ####################
src_location = "/YetAnotherClanMech/Objects/Mechs/Direwolf/"
#src_location = "/SpecialVariants/Objects/Mechs/Warhammer/"

srcVariant = "DWF-LW"
destVariants = [
	"DWF-UV"
]
prefix = 'YACM_'
use_sub_folders = True
########## CHANGE ME ####################


def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o
	
def get_primary_asset_id(path):
	return unreal.SystemLibrary.get_primary_asset_id_from_object(unreal.AssetRegistryHelpers.get_asset(unreal.EditorAssetLibrary.find_asset_data(path)))

def clone_variant(srcVariant, destVariant):
	dest_location = src_location

	with unreal.ScopedEditorTransaction("Clone Variant Script") as trans:
		mda_path = src_location
		loadout_path = src_location
		uc_path = src_location
		if use_sub_folders:
			mda_path = mda_path + 'MDA/'
			loadout_path = loadout_path + 'Loadout/'
			uc_path = uc_path + 'UnitCard/'
			
		dest_mda_path = mda_path + prefix + destVariant + "_MDA"
		dest_loadout_path = loadout_path + prefix + destVariant + "_Loadout"
		dest_uc_path = uc_path + prefix + destVariant + "_UnitCard"
		
		unreal.EditorAssetLibrary.duplicate_asset(mda_path + prefix + srcVariant + "_MDA", dest_mda_path)
		unreal.EditorAssetLibrary.duplicate_asset(uc_path + prefix + srcVariant + "_UnitCard", dest_uc_path)
		unreal.EditorAssetLibrary.duplicate_asset(loadout_path + prefix + srcVariant + "_Loadout", dest_loadout_path)
		
		destMda = get_asset(dest_mda_path)
		destLoadout = get_asset(dest_loadout_path)
		destCard = get_asset(dest_uc_path)
		
		#unreal.log(help(destMda.mech_data.get_editor_property("mech_type")))
		#unreal.log(dir(destMda.mech_data.get_editor_property("mech_type")))
		#tag = str(destMda.mech_data.get_editor_property("mech_type").get_editor_property('tag_name')).replace(srcVariant, destVariant)
		#unreal.log(tag)
		#new_tag = unreal.GameplayTag()
		#new_tag.set_editor_property('tag_name', tag)
		#destMda.mech_data.set_editor_property("mech_type", new_tag)
		
		destMda.mech_data.set_editor_property("variant_name", destVariant)
		destMda.mech_data.default_mech.set_editor_property("id", get_primary_asset_id(dest_loadout_path))

		destLoadout.mech_loadout.mech_data_asset_id.set_editor_property("id", get_primary_asset_id(dest_mda_path))
		destCard.unit_card.set_editor_property("mech_loadout_template", destMda.mech_data.default_mech)
		


for v in destVariants:
	clone_variant(srcVariant, v)
