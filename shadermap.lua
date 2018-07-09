--[[
    Lua script for Shader Map 4 automation.
    Creates a displacement map with set height and constrast
    from a specular normal map,
    as part of the 3D Facial Reconstruction pipeline
	at https://github.com/lattas/3d-facial-reconstruction
	@author Alexander Lattas
]]

HEIGHT   = 100
CONTRAST = 100

-- Add the ShaderMap module
package.path = package.path .. ";C:\\Program Files\\ShaderMap 4\\bin\\..\\lua\\?.lua"
require("sm4")


-- New Project
function sma() sm_new_project() end

-- Begin Node: Source Map
function sma() node_0 = sm_add_source_map_node("src_norm_map", "..\\data\\blenderTexture.png", 0, 0) end

	-- Begin Node: Properties
	function sma() sm_set_node_property_list(node_0, 0, 0) end
	function sma() sm_set_node_property_coordsys(node_0, 1, 1, 1, 1) end
	function sma() sm_set_node_property_slider(node_0, 2, 0) end

-- Begin Node: Map
function sma() node_1 = sm_add_map_node("map_norm_to_disp", 1, 0) end

	-- Begin Node: Inputs
	function sma() sm_set_map_node_input(node_1, 0, node_0) end

	-- Add Save Path
	function sma() sm_set_map_node_save_path(node_1, "..\\data\\blenderTexture", SM_MAP_FORMAT_PNG_RGBA_8) end

	-- Begin Node: Properties
	function sma() sm_set_node_property_list(node_1, 0, 1) end
	function sma() sm_set_node_property_slider(node_1, 1, CONTRAST) end
	function sma() sm_set_node_property_slider(node_1, 2, HEIGHT) end
	function sma() sm_set_node_property_checkbox(node_1, 3, 1) end
	function sma() sm_set_node_property_checkbox(node_1, 4, 1) end
	function sma() sm_set_node_property_checkbox(node_1, 5, 0) end

-- Render All Maps
function sma() sm_render_all_maps() end
