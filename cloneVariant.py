import unreal

########## CHANGE ME ####################
#src_location = "/YetAnotherClanMech/Objects/Mechs/Rifleman_IIC/"
src_location = "/SpecialVariants/Objects/Mechs/Hammer/"

srcVariant = "HMR-3M"
destVariants = [
	[ "HMR-3C", 3056, 976 ],
	[ "HMR-3P", 3060, 827 ],
	[ "HMR-3S", 3054, 638 ]
]
#prefix = 'YACM_'
prefix = ''
use_sub_folders = False
########## CHANGE ME ####################


def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o
	
def get_primary_asset_id(path):
	return unreal.SystemLibrary.get_primary_asset_id_from_object(unreal.AssetRegistryHelpers.get_asset(unreal.EditorAssetLibrary.find_asset_data(path)))

def clone_variant(srcVariant, dest_variant_stats):
	dest_location = src_location
	dest_variant = dest_variant_stats[0]
	dest_year = dest_variant_stats[1]
	dest_bv = dest_variant_stats[2]

	with unreal.ScopedEditorTransaction("Clone Variant Script") as trans:
		mda_path = src_location
		loadout_path = src_location
		uc_path = src_location
		if use_sub_folders:
			mda_path = mda_path + 'MDA/'
			loadout_path = loadout_path + 'Loadout/'
			uc_path = uc_path + 'UnitCard/'
			
		dest_mda_path = mda_path + prefix + dest_variant + "_MDA"
		dest_loadout_path = loadout_path + prefix + dest_variant + "_Loadout"
		dest_uc_path = uc_path + prefix + dest_variant + "_UnitCard"
		
		unreal.EditorAssetLibrary.duplicate_asset(mda_path + prefix + srcVariant + "_MDA", dest_mda_path)
		unreal.EditorAssetLibrary.duplicate_asset(uc_path + prefix + srcVariant + "_UnitCard", dest_uc_path)
		unreal.EditorAssetLibrary.duplicate_asset(loadout_path + prefix + srcVariant + "_Loadout", dest_loadout_path)
		
		destMda = get_asset(dest_mda_path)
		destLoadout = get_asset(dest_loadout_path)
		destCard = get_asset(dest_uc_path)
		
		#unreal.log(destMda.get_editor_property("mech_data").get_editor_property("variant_name"))
		#unreal.log(dir(destMda.mech_data.get_editor_property("variant_name")))
		#unreal.log(destMda.mech_data.default_mech.get_editor_property("id"))
		#unreal.log(type(destCard.unit_card.get_editor_property("mech_loadout_template")))
		#unreal.log(type(destMda.mech_data.default_mech))
		#tag = str(destMda.mech_data.get_editor_property("mech_type").get_editor_property('tag_name')).replace(srcVariant, destVariant)
		#unreal.log(tag)
		#new_tag = unreal.GameplayTag()
		#new_tag.set_editor_property('tag_name', tag)
		#destMda.mech_data.set_editor_property("mech_type", new_tag)
		
		destMda.get_editor_property("mech_data").set_editor_property("variant_name", unreal.Text(dest_variant))
		destMda.get_editor_property("mech_data").default_mech.set_editor_property("id", get_primary_asset_id(dest_loadout_path))

		destLoadout.get_editor_property("mech_loadout").mech_data_asset_id.set_editor_property("id", get_primary_asset_id(dest_mda_path))
		destCard.unit_card.get_editor_property("mech_loadout_template").set_editor_property("id", get_primary_asset_id(dest_mda_path))
		destCard.unit_card.set_editor_property("battle_value", dest_bv)
		destCard.unit_card.set_editor_property("intro_date", unreal.DateTime(dest_year, 1, 1))
		


for v in destVariants:
	clone_variant(srcVariant, v)
