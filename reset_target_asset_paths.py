import unreal
import shutil
import subprocess

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

####### SCRIPT CONFIG ##############
part_map = {
	'HeadArmor': 'ebj_hd_ext.png',
	'HeadInternal': 'ebj_hd_int.png',
	'CenterTorsoArmor': 'ebj_ct_ext.png',
	'CenterTorsoInternal': 'ebj_ct_int.png',
	'LeftTorsoArmor': 'ebj_lt_ext.png',
	'LeftTorsoInternal': 'ebj_lt_int.png',
	'RightTorsoArmor': 'ebj_rt_ext.png',
	'RightTorsoInternal': 'ebj_rt_int.png',
	'LeftArmArmor': 'ebj_ra_ext.png',
	'LeftArmInternal': 'ebj_ra_int.png',
	'RightArmArmor': 'ebj_la_ext.png',
	'RightArmInternal': 'ebj_la_int.png',
	'LeftLegArmor': 'ebj_rl_ext.png',
	'LeftLegInternal': 'ebj_rl_int.png',
	'RightLegArmor': 'ebj_ll_ext.png',
	'RightLegInternal': 'ebj_ll_int.png',
	'RearCenterTorsoArmor': 'ebj_ct(rear)_ext.png',
	'RearCenterTorsoInternal': 'ebj_ct(rear)_int.png',
	'RearLeftTorsoArmor': 'ebj_lt(rear)_ext.png',
	'RearLeftTorsoInternal': 'ebj_lt(rear)_int.png',
	'RearRightTorsoArmor': 'ebj_rt(rear)_ext.png',
	'RearRightTorsoInternal': 'ebj_rt(rear)_int.png'
}

png_location = 'D:/Downloads/MW5/Will9761s_Mech_Paperdolls/Will9761s_Mechpaperdolls_Part_1_1/Clan OmniMechs/Heavy OmniMechs/Ebon Jaguar/'
mech_name = 'EbonJaguar'
mech_path = '/YetAnotherClanMech/Objects/Mechs/'
tmp_folder = 'D:/Downloads/MW5/tmp/loadouts'
img_magick_path = 'C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\magick.exe'
####### /SCRIPT CONFIG ##############

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

def scale_img(img_path, target_path, width, height):
	subprocess.call('{0} "{1}" -resize {2}x{3}\\! -background none {4}'.format(img_magick_path, img_path, width, height, target_path))

def fix_texture_references(texture_path, target_asset_ref, mech_name):
	target = get_asset(target_asset_ref)
	blueprint = unreal.load_object(None, target_asset_ref)
	some_actor_cdo = unreal.get_default_object(blueprint)
	for pos in positions:
		old_name = str(some_actor_cdo.get_editor_property(pos).get_fname())
		new_tex_p = texture_path + old_name.replace('Cataphract', mech_name)
		unreal.log('Replacing ' + old_name + ' with ' + new_tex_p)
		new_tex = unreal.load_object(None, new_tex_p)
		some_actor_cdo.set_editor_property(pos, new_tex)
		
		new_src_p = png_location + part_map[pos]

		# create a tmp copy of the images and rescale to 128x128
		#tmp_file_p = tmp_folder + '/target-' + mech_name + '-' + pos + '.png'
		#shutil.copy(new_src_p, tmp_file_p)
		#scale_img(new_src_p, tmp_file_p, 128, 128)

		new_tex.get_editor_property('asset_import_data').scripted_add_filename(new_src_p, 0, 'New target pos texture')


with unreal.ScopedEditorTransaction("CollectEquipmentMetadata Script") as trans:
	texture_location = mech_path + mech_name + '/Target/Textures/'
	target_asset_ref = mech_path + mech_name + '/Target/' + mech_name + '_Target.' + mech_name + '_Target_C'
	
	#copy_textures(texture_location, mech_name)
	fix_texture_references(texture_location, target_asset_ref, mech_name)
