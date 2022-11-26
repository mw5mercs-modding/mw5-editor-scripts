import unreal

def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o
	
def get_primary_asset_id(path):
	return unreal.SystemLibrary.get_primary_asset_id_from_object(unreal.AssetRegistryHelpers.get_asset(unreal.EditorAssetLibrary.find_asset_data(path)))

def change_blueprint_default_value(blueprint_generated_class, variable_name, new_value):
    blueprint = unreal.load_object(None, blueprint_generated_class)
    some_actor_cdo = unreal.get_default_object(blueprint)
    some_actor_cdo.set_editor_property(variable_name, new_value)
    #blueprint.set_editor_property(variable_name, new_value)

asset_location = "/YetAnotherClanMech/Objects/Mechs/Shadowhawk_IIC/Model/Weapons/"

def fix_weapon_refs(weapon):
	skel_ref = weapon.replace('.', '_SKM.') + '_SKM'
	#ani_ref = weapon.replace('.', '_ANI.') + '_ANI'
	unreal.log('Skeleton : ' + skel_ref)
	#unreal.log('Animation: ' + ani_ref)
	#phy_ref = weapon.replace('_SKM', '_PHY')
	#unreal.log('PHY: ' + phy_ref)
	change_blueprint_default_value(weapon + '_C', 'skeletal_mesh', unreal.load_object(None, skel_ref))
	change_blueprint_default_value(weapon + '_C', 'fire_animation', None)
	#change_blueprint_default_value(weapon, 'fire_animation', unreal.load_object(None, ani_ref))
	#change_blueprint_default_value(weapon, 'physics_asset', unreal.load_object(None, weapon))
	#unreal.log(unreal.load_object(None, weapon + '_C').get_editor_property('scale'))

def is_weapon(ref):
	try:
		blueprint = unreal.load_object(None, ref + '_C')
		some_actor_cdo = unreal.get_default_object(blueprint)
		#unreal.log(some_actor_cdo.get_editor_property('skeletal_mesh'))
		return some_actor_cdo.get_editor_property('skeletal_mesh') != None
		#return blueprint.get_editor_property('physics_asset') != None
	except:
		return False

x = '/YetAnotherClanMech/Objects/Mechs/Shadowhawk_IIC/Model/Weapons/Weapon_Mech_SHD_Torso_Left_MH1_Missile10_SKM.Weapon_Mech_SHD_Torso_Left_MH1_Missile10_SKM'
asset_location = '/YetAnotherClanMech/Objects/Mechs/Phoenixhawk_IIC/Model/Weapons/'
with unreal.ScopedEditorTransaction("CollectEquipmentMetadata Script") as trans:
	#bp = unreal.load_object(None, x)
	#bpd = unreal.get_default_object(bp)
	#unreal.log(bp.get_editor_property('physics_asset'))
	#exit(0)
	#unreal.log(bpd.get_editor_property('skeletal_mesh'))
	#unreal.log(bpd.get_editor_property('fire_animation'))
	assets = unreal.EditorAssetLibrary.list_assets(asset_location, True)
	for asset_path in assets:
		if is_weapon(asset_path):
			asset = get_asset(asset_path)
			#unreal.log(dir(asset))
			try:
				unreal.log('Weapon: ' + asset_path)
				fix_weapon_refs(asset_path)
			except:
				unreal.log('Not: ' + asset_path)
				
	#		unreal.log(asset.name)
#			unreal.log("Intro year: {}".format(asset.intro_date.to_tuple()[0]))
			#unreal.log("Tons: {}".format(asset.tons))
			#unreal.log("Slots: {}".format(asset.slots))
			#unreal.log("Description: {}".format(asset.description))
			#unreal.log("Base Price: {}".format(asset.c_bill_base_value))
			
			#if str(asset.short_name).startswith("C-"):
			#	unreal.log("Renaming to " + str(asset.short_name)[2:] + " (C)")
			#	asset.set_editor_property("short_name", unreal.Text(str(asset.short_name)[2:] + " (C)"))
		
	#unreal.log(o.mech_data.variant_name)
	#unreal.log(o.mech_data.default_mech)
	#unreal.log(get_primary_asset_id(asset_location + srcVariant + "_Loadout"))
