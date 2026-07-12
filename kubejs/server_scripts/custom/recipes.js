// priority: 0
"use strict";


const registerCustomRecipes = (event) => 
{
	// Supplementaries
	event.remove({ id: 'supplementaries:rope' })
	event.remove({ id: 'supplementaries:slice_map' })

	//# rope
	event.shapeless('3x supplementaries:rope', ['firmaciv:rope_coil']).id('tfg:shapeless/firmaciv_rope_to_supplementaries_rope')
	event.shaped('firmaciv:rope_coil', [
		'AAA',
	], {
		A: 'supplementaries:rope',
	}).id('tfg:shaped/supplementaries_rope_to_firmaciv_rope')

	//# slice map
	event.shapeless('supplementaries:slice_map', ['minecraft:map']).id('tfg:shapeless/supplementaries_slice_map')
	event.shapeless('minecraft:map', ['supplementaries:slice_map']).id('tfg:shapeless/supplementaries_slice_map_to_map')


	// Map Atlases 
	event.remove({ mod: 'map_atlases' })
	event.shapeless('map_atlases:atlas', [
		'minecraft:writable_book', 
		'tfc:glue',
		'minecraft:map'
	]).id('tfg:shapeless/map_atlas')


	// Mech Trowel

	//# Trowel
	event.remove({ id: 'mechtrowel:mech_trowel' })
	event.remove({ input: 'mechtrowel:reach_upgrade_template' })
	event.remove({ input: 'mechtrowel:variant_conversion_template' })
	event.remove({ output: 'mechtrowel:wand_template' })

	event.shapeless('mechtrowel:mech_trowel', [
		'tfg:trowel',
		'#gtceu:circuits/lv',
		'#forge:cogwheels',
		'#forge:tools/wrenches'
	]).id('tfg:shapeless/mechtrowel')

	//# Templates
	event.shaped('mechtrowel:wand_template', [
		' A ',
		' PA',
		'S  '
	], {
		A: 'constructionwand:diamond_wand',
		P: '#forge:ender_pearls',
		S: 'minecraft:stick'
	}).id('tfg:shaped/trowel/wand_template')

	event.shaped('mechtrowel:wand_capacity_template', [
		' A ',
		' PA',
		'S  '
	], {
		A: 'constructionwand:infinity_wand',
		P: '#forge:ender_pearls',
		S: 'minecraft:stick'
	}).id('tfg:shaped/trowel/wand_capacity_template')
}