--[[

	LUA VERSION 5.3.4

	The ShaderMap LUA API is released under The MIT License (MIT)
	http://opensource.org/licenses/MIT

	Copyright (c) 2017 Rendering Systems Inc.

	Permission is hereby granted, free of charge, to any person
	obtaining a copy of this software and associated documentation
	files (the "Software"), to deal	in the Software without
	restriction, including without limitation the rights to use,
	copy, modify, merge, publish, distribute, sublicense, and/or
	sell copies of the Software, and to permit persons to whom the
	Software is	furnished to do so, subject to the following
	conditions:

	The above copyright notice and this permission notice shall be
	included in	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
	OF MERCHANTABILITY,	FITNESS FOR A PARTICULAR PURPOSE AND
	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
	HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
	WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
	OTHER DEALINGS IN THE SOFTWARE.

]]

	-- Add the ShaderMap module
	package.path = package.path .. ";C:\\Program Files\\ShaderMap 4\\bin\\..\\lua\\?.lua"
	require("sm4")


	-- TODO Batch variables
	source_directory	= "C:\\Users\\aglat\\lightstage\\data\\"
	save_directory		= "C:\\Users\\aglat\\lightstage\\data\\"
	node_0_src_array	= {"blenderTexture.png"}
	node_1_save_array	= {"result.png"}
	loop_count			= # node_0_src_array
	batch_index			= 1 -- Lua uses 1 based indices


	-- New Project
	function sma() sm_new_project() end

	-- Begin Node: Source Map
	function sma() node_0 = sm_add_source_map_node("src_norm_map", "null", 0, 0) end

		-- Begin Node: Properties
		function sma() sm_set_node_property_list(node_0, 0, 0) end
		function sma() sm_set_node_property_coordsys(node_0, 1, 1, 1, 1) end
		function sma() sm_set_node_property_slider(node_0, 2, 0) end

	-- Begin Node: Map
	function sma() node_1 = sm_add_map_node("map_norm_to_disp", 1, 0) end

		-- Begin Node: Inputs
		function sma() sm_set_map_node_input(node_1, 0, node_0) end

		-- Begin Node: Properties
		function sma() sm_set_node_property_list(node_1, 0, 1) end
		function sma() sm_set_node_property_slider(node_1, 1, 100) end
		function sma() sm_set_node_property_slider(node_1, 2, 100) end
		function sma() sm_set_node_property_checkbox(node_1, 3, 1) end
		function sma() sm_set_node_property_checkbox(node_1, 4, 1) end
		function sma() sm_set_node_property_checkbox(node_1, 5, 0) end


	-- Begin Batch Loop
	function sma() sm_begin_loop(loop_count) end

		-- Change Source Map(s)
		function sma() sm_change_source_map_node(node_0, source_directory .. node_0_src_array[batch_index]) end

		-- Change Save Path(s)
		function sma() sm_set_map_node_save_path(node_1, save_directory .. node_1_save_array[batch_index], SM_MAP_FORMAT_PNG_RGBA_8) end

		-- Render Source Map(s) and Children
		function sma() sm_render_all_maps() end

		-- Save All Maps with Save Paths
		function sma() sm_save_all_maps() end

	-- End Batch Loop
	function sma()

		batch_index = batch_index + 1
		sm_end_loop()

	end

	-- Terminate SM
	function sma()
		
		sm_exit_sm()

	end

