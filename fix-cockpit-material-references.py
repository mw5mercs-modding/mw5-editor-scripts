import unreal

x = '/YetAnotherClanMech/Objects/Mechs/Maddog/Model/Cockpit/Maddog_cockpit_SKM.Maddog_cockpit_SKM'
with unreal.ScopedEditorTransaction("CollectEquipmentMetadata Script") as trans:
	bp = unreal.load_object(None, x)
	new_mats = []
	for mat in bp.get_editor_property('materials'):
		#unreal.log(mat.get_editor_property("material_interface"))
		name = mat.get_editor_property("material_interface").get_full_name()
		new_name = name.replace("BlackLanner", "YetAnotherClanMech")
		unreal.log("Renaming " + name + " to " + new_name)
		new_mat = unreal.load_object(None, new_name.split(" ")[1])
		#unreal.log(mat)
		mat.set_editor_property('material_interface', new_mat)
		new_mats.append(mat)
	bp.set_editor_property('materials', new_mats)
