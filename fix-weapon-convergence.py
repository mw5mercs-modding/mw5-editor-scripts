"""
This script will fix MW5 weapon convergence using the good old export/import trick.
This trick applies to all weapon blueprints which have a non-default translation matrix, causing
ballistic weapons to shoot crooked.

To this end the script will perform the following steps:
1. Find all weapon blueprints with non-default transformations
2. Check if the blueprint has its own skeleton (same folder, same name + '_SKM')
3. If not, then the skeleton will be cloned and the blueprint reference updated
4. The fire animation will be set to "None" since we cannot apply the trick to animations.
5. Then the skeleton will be exported to FBX in a temp folder
6. The non-default translation matrix will be copied to the skeleton's import settings
7. The skeleton will be re-imported with the translation applied
8. The blueprint's translation will be reset to defaults (except scale in case that could not be applied.)
9. Finally the material slots will be reset to their original values and the LODs will be regenerated.

Configure the script through the parameters below.
"""

import unreal

####### SCRIPT CONFIG ##############
asset_locations = [
	'/YetAnotherClanMech/Objects/Mechs/BlackLanner/Model/Weapons/',
	'/YetAnotherClanMech/Objects/Mechs/Cougar/Model/Weapons/',
	'/YetAnotherClanMech/Objects/Mechs/Nova/Model/Weapons/',
	'/YetAnotherClanMech/Objects/Mechs/Direwolf/Model/Weapons/',
	'/YetAnotherClanMech/Objects/Mechs/Adder/Model/Weapons/',
	'/YetAnotherClanMech/Objects/Mechs/MadCatMKII/Model/Weapons/',
	'/YetAnotherClanMech/Objects/Mechs/BloodAsp/Model/Weapons/',
	'/YetAnotherClanMech/Objects/Mechs/Maddog/Model/Weapons/'
]
tmp = 'D:/Downloads/MW5/tmp/weapon-skms'
ignore_missile = True
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


def update_skm_import_translation(weapon_bp_def, ignore_scale):
	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')
	skm_asset.get_editor_property('asset_import_data').set_editor_property('import_translation', weapon_bp_def.get_editor_property('relative_location'))
	skm_asset.get_editor_property('asset_import_data').set_editor_property('import_rotation', weapon_bp_def.get_editor_property('relative_rotation'))
	if ignore_scale:
		skm_asset.get_editor_property('asset_import_data').set_editor_property('import_uniform_scale', 1.0)
		# We need to scale the import translation by the 3d scaling which we cannot change
		skm_asset.get_editor_property('asset_import_data').set_editor_property('import_translation', unreal.Vector(
			weapon_bp_def.get_editor_property('relative_location').x / weapon_bp_def.get_editor_property('relative_scale3d').x,
			weapon_bp_def.get_editor_property('relative_location').y / weapon_bp_def.get_editor_property('relative_scale3d').y,
			weapon_bp_def.get_editor_property('relative_location').z / weapon_bp_def.get_editor_property('relative_scale3d').z
		))
	else:
		skm_asset.get_editor_property('asset_import_data').set_editor_property('import_uniform_scale', weapon_bp_def.get_editor_property('relative_scale3d').x)


def reset_weapon_transform(weapon_bp_def, ignore_scale):
	weapon_bp_def.set_editor_property('relative_location', unreal.Vector(0.0,0.0,0.0))
	weapon_bp_def.get_editor_property('relative_rotation').yaw = 0.0
	weapon_bp_def.get_editor_property('relative_rotation').pitch = 0.0
	weapon_bp_def.get_editor_property('relative_rotation').roll = 0.0
	if not ignore_scale:
		weapon_bp_def.set_editor_property('relative_scale3d', unreal.Vector(1.0,1.0,1.0))


def clone_skm_if_necessary(asset_path):
	"""
	Will clone a weapon blueprints skeletal mesh if its current path is not in the same folder.
	Will also set the fire animation to None in that case.
	
	Parameters:
	- asset_path: Path to the weapon blueprint asset
	"""
	weapon_bp = unreal.load_object(None, asset_path + '_C')
	weapon_bp_def = unreal.get_default_object(weapon_bp)

	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')
	weapon_bp_ref_dir = get_ref_dir(weapon_bp.get_path_name())
	
	current_skm_path = get_ref_dir(skm_asset.get_path_name()) + '/' + skm_asset.get_name()
	target_skm_path = weapon_bp_ref_dir + '/' + asset_path.split('.')[-1] + '_SKM'

	unreal.log('Current SKM path: ' + current_skm_path)
	unreal.log('Target SKM path: ' + target_skm_path)

	if current_skm_path != target_skm_path:
		unreal.log('New SKM location: ' + target_skm_path)
		unreal.EditorAssetLibrary.duplicate_asset(skm_asset.get_path_name(), target_skm_path)
		weapon_bp_def.set_editor_property('skeletal_mesh', unreal.load_object(None, target_skm_path))

	# clear the animation since we cannot transform that
	weapon_bp_def.set_editor_property('fire_animation', None)


def has_non_default_transform(weapon_bp_def, ignore_scale):
	"""
	Checks if a weapon blueprint has a non-default transform matrix which requires a re-import of the mesh
	to fix weapon convergence.
	
	Parameters:
	- weapon_bp_def: Default object of the weapon blueprint
	"""
	return weapon_bp_def.get_editor_property('relative_location').x != 0.0 \
		or weapon_bp_def.get_editor_property('relative_location').y != 0.0 \
		or weapon_bp_def.get_editor_property('relative_location').z != 0.0 \
		or weapon_bp_def.get_editor_property('relative_rotation').pitch != 0.0 \
		or weapon_bp_def.get_editor_property('relative_rotation').yaw != 0.0 \
		or weapon_bp_def.get_editor_property('relative_rotation').roll != 0.0 \
		or (not ignore_scale and weapon_bp_def.get_editor_property('relative_scale3d').x != 1.0) \
		or (not ignore_scale and weapon_bp_def.get_editor_property('relative_scale3d').y != 1.0) \
		or (not ignore_scale and weapon_bp_def.get_editor_property('relative_scale3d').z != 1.0)


def has_uniform_scaling(weapon_bp_def):
	"""
	Checks if the given weapon has different scaling factors for the different axis.
	
	Since the import settings only allow for a single scaling factor, that is what we verify
	"""
	return weapon_bp_def.get_editor_property('relative_scale3d').x == weapon_bp_def.get_editor_property('relative_scale3d').y == weapon_bp_def.get_editor_property('relative_scale3d').z


def export_weapon_skm(weapon_bp_def, tmp_dir):
	"""
	Exports the given weapon blueprint's skm to fbx in the given tmp folder
	
	Parameters:
	- weapon_bp_def: Default object of the weapon blueprint
	- tmp_dir: The path of the folder to export to
	"""
	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')
	export_path = tmp_dir + '/' + skm_asset.get_path_name().split('.')[-1] + '.FBX'
	unreal.log('Exporting to ' + export_path)
	
	task = unreal.AssetExportTask()
	task.object = skm_asset
	task.filename = export_path
	task.replace_identical = True
	task.prompt = False
	task.automated = True
	task.options = unreal.FbxExportOption()
	task.options.vertex_color = False
	task.options.collision = False
	
	unreal.Exporter.run_asset_export_task(task)
	
	return export_path


def import_weapon_skm(weapon_bp_def, import_path):
	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')

	# remember material slots since the import messes them up
	mat_slots = [str(mat.material_slot_name) for mat in skm_asset.get_editor_property('materials')]

	task = unreal.AssetImportTask()
	task.filename = import_path
	task.destination_path = get_ref_dir(weapon_bp_def.get_path_name())
	task.destination_name = skm_asset.get_path_name().split('.')[-1]
	task.automated = True
	task.replace_existing = True
	task.replace_existing_settings = False
	
	task.options = unreal.FbxImportUI()
	task.options.import_materials = False
	task.options.import_as_skeletal = True
	task.options.import_animations = False
	task.options.import_textures = False
	
	unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
	
	# remove fbx material slots which we do not need. 
	# This also fixes the LOD material slots which got messed up during import
	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')
	unreal.log(skm_asset.get_editor_property('materials'))
	new_mats = []
	for mat in skm_asset.get_editor_property('materials'):
		if str(mat.material_slot_name) in mat_slots:
			new_mats.append(mat)
	# restore original material list and rebuild the LODs
	skm_asset.set_editor_property('materials', new_mats)
	skm_asset.regenerate_lod()


def fix_weapon_convergence(asset_path):
	weapon_bp = unreal.load_object(None, asset_path + '_C')
	weapon_bp_def = unreal.get_default_object(weapon_bp)
	ignore_scaling = not has_uniform_scaling(weapon_bp_def)
	if has_non_default_transform(weapon_bp_def, ignore_scaling):
		unreal.log('Need to fix convergence on ' + asset_path)
		clone_skm_if_necessary(asset_path)
		fbx_file = export_weapon_skm(weapon_bp_def, tmp)
		update_skm_import_translation(weapon_bp_def, ignore_scaling)
		import_weapon_skm(weapon_bp_def, fbx_file)
		reset_weapon_transform(weapon_bp_def, ignore_scaling)


with unreal.ScopedEditorTransaction("Fix Weapon Convergence Script") as trans:
	for asset_location in asset_locations:
		assets = unreal.EditorAssetLibrary.list_assets(asset_location, True)
		for asset_path in assets:
			if isinstance(get_asset(asset_path), unreal.Blueprint) and not (ignore_missile and "MH" in asset_path):# and not 'BKL_1A_Upperarm_right_weapon_EH1' in asset_path:
				try:
					fix_weapon_convergence(asset_path)
				except Exception as ex:
					unreal.log('Not a weapon bp: ' + asset_path)
