// priority: 0
"use strict";


const registerSupplementariesRecipes = (event) => 
{
	event.remove({ id: 'supplementaries:rope' })
	event.remove({ id: 'supplementaries:slice_map' })

	// rope
	event.shapeless('3x supplementaries:rope', ['firmaciv:rope_coil']).id('tfg:shapeless/firmaciv_rope_to_supplementaries_rope')
	event.shaped('firmaciv:rope_coil', [
		'AAA',
	], {
		A: 'supplementaries:rope',
	}).id('tfg:shaped/supplementaries_rope_to_firmaciv_rope')

	// slice map
	event.shapeless('supplementaries:slice_map', ['minecraft:map']).id('tfg:shapeless/supplementaries_slice_map')
	event.shapeless('minecraft:map', ['supplementaries:slice_map']).id('tfg:shapeless/supplementaries_slice_map_to_map')
}

const registerMapAtlasRecipes = (event) =>
{
	event.remove({ mod: 'map_atlases' })
	event.shapeless('map_atlases:atlas', [
		'minecraft:writable_book', 
		'tfc:glue',
		'minecraft:map'
	]).id('tfg:shapeless/map_atlas')
}

const registerJadeSpyglassRecipes = (event) => {

}

ServerEvents.recipes(event => {
	registerMapAtlasRecipes(event)
	registerSupplementariesRecipes(event)
	registerJadeSpyglassRecipes(event)
})