bl_info = {
    "name": "RDC files checking tool",
    "author": "Long H B",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Tool to quickly check capture files",
    "warning": "",
    "doc_url": "",
    "category": "RDC file check",
}

#Base libraries
import bpy
import os




def screenshot_condition(self, context):
    #Set up image output
    bpy.context.scene.display_settings.display_device = 'sRGB'
    bpy.context.scene.view_settings.view_transform = 'Standard'
    bpy.context.scene.view_settings.look = 'Medium High Contrast'
        # Set up screenshot condition
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas: # iterate through areas in current screen
            if area.type == 'VIEW_3D':
                for space in area.spaces: # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D': # check if space is a 3D view
                        space.shading.type = 'SOLID'
                        space.shading.cavity_type = 'SCREEN'
                        space.shading.show_cavity = True
                        space.shading.show_xray = False
                        space.overlay.show_overlays = True
    return {'FINISHED'}
    

def purge_data(self, context):
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)
    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)
    return {'FINISHED'}
                            


PROPS = [
    ("rdc_name", bpy.props.StringProperty(name='Files name',default="",description="names of the rdc files, separated by comma")),
    ("folder", bpy.props.StringProperty(name='RDC path',default="",description="File path to the RDC files",maxlen=1024,subtype='FILE_PATH')),
    ("has3D", bpy.props.StringProperty(name='3D folder',default="",description="File path to the 3D files",maxlen=1024,subtype='FILE_PATH')),
    ("recapture", bpy.props.StringProperty(name='Recapture folder',default="",description="File path to the recapture list",maxlen=1024,subtype='FILE_PATH')),
]

#PANEL-----------------
class Import_RDC(bpy.types.Panel):
    """check quality of RDC model"""
    bl_label = "Import RDC"
    bl_idname = "OBJECT_PT_RDCpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RDC file check'
    
    def draw(self, context):
        layout = self.layout

        layout.label(text="General")
        boxSetup = layout.box()
        col3 = boxSetup.column()
        row = col3.row()
        row.prop(context.scene, "folder")
        row = col3.row()
        row.prop(context.scene, "has3D")
        row = col3.row()
        row.prop(context.scene, "recapture")
        row = col3.row()
        row.prop(context.scene, "rdc_name")
        row = col3.row()
        row.operator('opr.import_rdc', text='Import') 
        

  
    


class import_rdc(bpy.types.Operator):
    """import the rdc file"""
    bl_label = "import rdc"
    bl_idname = "opr.import_rdc"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        capture_list = list(map(str, bpy.context.scene.rdc_name.split(',')))
        recapture_list = []
        n = len(capture_list)
    # Iterates over the indices from 0 to n-1 

        for i in range(n):
            #convert list to string
            capture_string = str(capture_list[i])
            bpy.ops.import_rdc.google_maps(filepath=os.path.join(bpy.context.scene.folder+capture_string+'.rdc'))
            
        #check if any model is imported, save and take screenshot
            if bpy.context.selected_objects:
                    purge_data(self, context)          
                    #save file with 3D
                    bpy.ops.wm.save_as_mainfile(filepath = os.path.join(bpy.context.scene.has3D+'\\'+capture_string+'.blend'));                    
                    #Take screenshot
                    screenshot_condition(self, context)
                    bpy.context.scene.render.filepath = os.path.join(bpy.context.scene.has3D+'\\'+capture_string);
                    bpy.ops.render.opengl(animation=False, render_keyed_only=False, sequencer=False, write_still=True, view_context=True);
                    #Delete and purge
                    bpy.ops.object.select_all(action='SELECT')
                    bpy.ops.object.delete()
                    purge_data(self, context)

            
            #if no model is imported, put it in a list
            else:
                
                recapture_list.append(capture_list[i])
                
        #write the hotels names that need recapturing to a text file
                
            result = ','.join(recapture_list)
            # get path to render output (usually /tmp\)
            tempFolder = os.path.join(bpy.context.scene.recapture);
            # make a filename
            filename = os.path.join (tempFolder, "recapturelist.txt")
            # confirm path exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            # open a file to write to
            file = open(filename, "w")
            # write the data to file
            print(result)
            file.write(result)
            # close the file
            file.close()
                            
             
        return {'FINISHED'}
           

#Register the properties
CLASSES = [Import_RDC,import_rdc]

def register():

    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    for klass in CLASSES:
        bpy.utils.register_class(klass)


def unregister():

    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

    
if __name__ == "__main__":
    register()
    
