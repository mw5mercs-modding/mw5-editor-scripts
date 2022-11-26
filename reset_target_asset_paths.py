import unreal

positions = [
	'HeadArmor',
	'HeadInternal',
	'CenterTorsoArmor',
	'CenterTorsoInternal',
	'LeftTorsoArmor',
	'LeftTorsoInternal',
	'RightTorsoArmor',
	'RightTorsoInternal',
	'LeftArmArmor',
	'LeftArmInternal',
	'RightArmArmor',
	'RightArmInternal',
	'LeftLegArmor',
	'LeftLegInternal',
	'RightLegArmor',
	'RightLegInternal',
	'RearCenterTorsoArmor',
	'RearCenterTorsoInternal',
	'RearLeftTorsoArmor',
	'RearLeftTorsoInternal',
	'RearRightTorsoArmor',
	'RearRightTorsoInternal'
]
	
part_map = {
	'HeadArmor': 'nva_hd_ext.png',
	'HeadInternal': 'nva_hd_int.png',
	'CenterTorsoArmor': 'nva_ct_ext.png',
	'CenterTorsoInternal': 'nva_ct_int.png',
	'LeftTorsoArmor': 'nva_rt_ext.png',
	'LeftTorsoInternal': 'nva_rt_int.png',
	'RightTorsoArmor': 'nva_lt_ext.png',
	'RightTorsoInternal': 'nva_lt_int.png',
	'LeftArmArmor': 'nva_ra_ext.png',
	'LeftArmInternal': 'nva_ra_int.png',
	'RightArmArmor': 'nva_la_ext.png',
	'RightArmInternal': 'nva_la_int.png',
	'LeftLegArmor': 'nva_rl_ext.png',
	'LeftLegInternal': 'nva_rl_int.png',
	'RightLegArmor': 'nva_ll_ext.png',
	'RightLegInternal': 'nva_ll_int.png',
	'RearCenterTorsoArmor': 'nva_ct(rear)_ext.png',
	'RearCenterTorsoInternal': 'nva_ct(rear)_int.png',
	'RearLeftTorsoArmor': 'nva_rt(rear)_ext.png',
	'RearLeftTorsoInternal': 'nva_rt(rear)_int.png',
	'RearRightTorsoArmor': 'nva_lt(rear)_ext.png',
	'RearRightTorsoInternal': 'nva_lt(rear)_int.png'
}

png_location = 'D:/Downloads/MW5/Will9761s_Mech_Paperdolls/Will9761s_Mechpaperdolls_Part_1_1/Clan OmniMechs/Medium OmniMechs/Nova/'
mech_name = 'Nova'

def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o

def copy_textures(target_path, mech_name):
	p = '/Game/Objects/Mechs/Cataphract/Target/Textures/'
	assets = unreal.EditorAssetLibrary.list_assets(p, True)
	for asset_path in assets:
		p2 = target_path + asset_path.split('.')[-1].replace('Cataphract', mech_name)
		unreal.EditorAssetLibrary.duplicate_asset(asset_path, p2)

def fix_texture_references(texture_path, target_asset_ref, mech_name):
	target = get_asset(target_asset_ref)
	blueprint = unreal.load_object(None, target_asset_ref)
	some_actor_cdo = unreal.get_default_object(blueprint)
	for pos in positions:
		old_name = str(some_actor_cdo.get_editor_property(pos).get_fname())
		new_tex_p = texture_path + old_name.replace('Vulcan', mech_name)
		unreal.log('Replacing ' + old_name + ' with ' + new_tex_p)
		new_tex = unreal.load_object(None, new_tex_p)
		some_actor_cdo.set_editor_property(pos, new_tex)
		
		new_src_p = png_location + part_map[pos]
		new_tex.get_editor_property('asset_import_data').scripted_add_filename(new_src_p, 0, 'New target pos texture')


with unreal.ScopedEditorTransaction("CollectEquipmentMetadata Script") as trans:
	texture_location = '/YetAnotherClanMech/Objects/Mechs/' + mech_name + '/Target/Textures/'
	target_asset_ref = '/YetAnotherClanMech/Objects/Mechs/' + mech_name + '/Target/' + mech_name + '_Target.' + mech_name + '_Target_C'
	
	#copy_textures(texture_location, mech_name)
	fix_texture_references(texture_location, target_asset_ref, mech_name)
