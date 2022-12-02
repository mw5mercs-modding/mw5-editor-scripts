import unreal

def get_ref_dir(ref):
	return '/'.join(ref.split('/')[0:-1])

def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o

def update_src(weapon_bp_def, new_path):
	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')
	skm_asset.get_editor_property('asset_import_data').scripted_add_filename(new_path, 0, 'Source File (Geometry and Skinning Weights)')

def update_skm_import_translation(weapon_bp_def):
	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')
	#unreal.log(help(skm_asset.get_editor_property('asset_import_data')))
	skm_asset.get_editor_property('asset_import_data').set_editor_property('import_translation', weapon_bp_def.get_editor_property('relative_location'))
	skm_asset.get_editor_property('asset_import_data').set_editor_property('import_rotation', weapon_bp_def.get_editor_property('relative_rotation'))

def reset_weapon_transform(weapon_bp_def):
	weapon_bp_def.set_editor_property('relative_location', unreal.Vector(0.0,0.0,0.0))
	weapon_bp_def.get_editor_property('relative_rotation').yaw = 0.0
	weapon_bp_def.get_editor_property('relative_rotation').pitch = 0.0
	weapon_bp_def.get_editor_property('relative_rotation').roll = 0.0
	weapon_bp_def.set_editor_property('relative_scale3d', unreal.Vector(0.0,0.0,0.0))

def clone_skm_if_necessary(weapon_bp_def):
	"""
	Will clone a weapon blueprints skeletal mesh if its current path is not in the same folder.
	Will also set the fire animation to None in that case.
	
	Parameters:
	- weapon_bp_def: Default object of the weapon blueprint
	"""
	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')
	weapon_bp_ref_dir = get_ref_dir(weapon_bp_def.get_path_name())

	skm_ref_dir = get_ref_dir(skm_asset.get_path_name())
	unreal.log('Blueprint ref path: ' + weapon_bp_ref_dir)
	unreal.log('Skeleton ref path: ' + skm_ref_dir)

	if weapon_bp_ref_dir != skm_ref_dir:
		new_skm_ref = weapon_bp.get_path_name().split('.')[0] + '_SKM'
		unreal.log('New SKM location: ' + new_skm_ref)
		unreal.EditorAssetLibrary.duplicate_asset(skm_asset.get_path_name(), new_skm_ref)
		weapon_bp_def.set_editor_property('skeletal_mesh', unreal.load_object(None, new_skm_ref))
		weapon_bp_def.set_editor_property('fire_animation', None)

def has_non_default_transform(weapon_bp_ref):
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
		or weapon_bp_def.get_editor_property('relative_scale3d').x != 1.0 \
		or weapon_bp_def.get_editor_property('relative_scale3d').y != 1.0 \
		or weapon_bp_def.get_editor_property('relative_scale3d').z != 1.0
	
def can_weapon_convergance_be_fixed(weapon_bp_def):
	"""
	Checks if we can fix the weapon convergence with the export/import trick
	
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
	task.options.level_of_detail = False
	
	unreal.Exporter.run_asset_export_task(task)
	
	return export_path
	

def import_weapon_skm(weapon_bp_def, import_path):
	skm_asset = weapon_bp_def.get_editor_property('skeletal_mesh')

	task = unreal.AssetImportTask()
	task.filename = import_path
	task.destination_path = get_ref_dir(weapon_bp_def.get_path_name())
	task.destination_name = skm_asset.get_path_name().split('.')[-1]
	task.automated = True
	task.replace_existing = True
	task.replace_existing_settings = False
	task.options = unreal.FbxSkeletalMeshImportData()
	task.options.import_translation = weapon_bp_def.get_editor_property('relative_location')
	task.options.import_rotation = weapon_bp_def.get_editor_property('relative_rotation')
	task.options.import_uniform_scale = weapon_bp_def.get_editor_property('relative_scale3d').x
	
	unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])


asset_location = '/YetAnotherClanMech/Objects/Mechs/Direwolf/Model/Weapons/'
tmp = 'D:/Downloads/MW5/tmp/weapon-skms' 
with unreal.ScopedEditorTransaction("CollectEquipmentMetadata Script") as trans:
	assets = unreal.EditorAssetLibrary.list_assets(asset_location, True)
	for asset_path in assets:
		if isinstance(get_asset(asset_path), unreal.Blueprint):
			try:
				weapon_bp = unreal.load_object(None, asset_path + '_C')
				weapon_bp_def = unreal.get_default_object(weapon_bp)
				if has_non_default_transform(weapon_bp_def):
					unreal.log('Need to fix convergence on ' + asset_path)
					if can_weapon_convergance_be_fixed(weapon_bp_def):
						clone_skm_if_necessary(weapon_bp_def)
						fbx_file = export_weapon_skm(weapon_bp_def, tmp)
						#update_src(weapon_bp_def, fbx_file)
						update_skm_import_translation(weapon_bp_def)
						import_weapon_skm(weapon_bp_def, fbx_file)
						reset_weapon_transform(weapon_bp_def)
					else:
						unreal.log_warning('Cannot fix convergence on ' + asset_path + ' because of scaling factors')
			except:
				unreal.log('Not a weapon bp: ' + asset_path)
