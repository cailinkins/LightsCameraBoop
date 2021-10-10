# Copyright (c) 2021 Cailín Walsh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy, mathutils

bl_info = {
    "name": "Lights, Camera, *boop*",
    "description": "Exports light and camera data to a JSON file.",
    "author": "Cailín Walsh",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "File > Export",
    "category": "Import-Export"
}

# auto-formats a JSON property for us
def write_json_property(key, value):
    output = "\"{}\": ".format(key)

    if isinstance(value, list) or isinstance(value, (mathutils.Vector, mathutils.Color, mathutils.Euler)):
        output += "[ "
        for index, v in enumerate(value):
            if isinstance(v, str):
                output += "\"{}\"".format(v)
            else:
                output += "{}".format(v)
            if index < len(value)-1:
                output += ", " 
        output += " ]" 
    else:
        if isinstance(value, str):
            output += "\"{}\"".format(value)
        else:
            output += "{}".format(value)
    return output

# outputs light and camera data, formatted as JSON, into the specified file

def write_some_data(context, filepath):
    f = open(filepath, 'w', encoding='utf-8')
    f.write("{\n")
    #export lights
    lights = []
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            lights.append(obj)
    f.write("\t\"lights\": [\n")
    for index, obj in enumerate(lights):
            f.write("\t\t{\n")            
            f.write("\t\t\t%s,\n" % write_json_property("type", obj.data.type))
            f.write("\t\t\t%s,\n" % write_json_property("location", obj.location))
            f.write("\t\t\t%s,\n" % write_json_property("color", obj.data.color))
            f.write("\t\t\t%s,\n" % write_json_property("diffuse", obj.data.diffuse_factor))
            f.write("\t\t\t%s,\n" % write_json_property("specular", obj.data.specular_factor))
            f.write("\t\t\t%s,\n" % write_json_property("volume", obj.data.volume_factor))
            if obj.data.type == 'POINT':
                f.write("\t\t\t%s,\n" % write_json_property("power", obj.data.energy))
                f.write("\t\t\t%s,\n" % write_json_property("radius", obj.data.shadow_soft_size))
            if obj.data.type == 'SUN':
                f.write("\t\t\t%s,\n" % write_json_property("strength", obj.data.energy))
                f.write("\t\t\t%s,\n" % write_json_property("angle", obj.data.angle))
                f.write("\t\t\t%s,\n" % write_json_property("rotation", obj.rotation_euler))
            f.write("\t\t}")
            if index < len(lights)-1:
                f.write(",")
            f.write("\n")
    f.write("\t],\n")
    #export cameras
    cameras = []
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            cameras.append(obj)
    f.write("\t\"cameras\": [\n")
    for index, obj in enumerate(bpy.data.objects):
        if obj.type == 'CAMERA':
            f.write("\t\t{\n")
            f.write("\t\t\t%s,\n" % write_json_property("type", obj.data.type))
            f.write("\t\t\t%s,\n" % write_json_property("location", obj.location))
            f.write("\t\t\t%s,\n" % write_json_property("rotation", obj.rotation_euler))
            f.write("\t\t\t%s,\n" % write_json_property("lens", obj.data.lens))
            f.write("\t\t\t%s,\n" % write_json_property("clip_start", obj.data.clip_start))
            f.write("\t\t\t%s,\n" % write_json_property("clip_end", obj.data.clip_end))
            if obj.data.type == 'ORTHO':
                f.write("\t\t\t%s ,\n" % write_json_property("ortho_scale", obj.data.ortho_scale))
            f.write("\t\t\t%s,\n" % write_json_property("sensor_fit", obj.data.sensor_fit))
            f.write("\t\t\t%s,\n" % write_json_property("sensor_width", obj.data.sensor_width))
            f.write("\t\t\t%s,\n" % write_json_property("sensor_height", obj.data.sensor_height))
            f.write("\t\t}")
            if index < len(cameras)-1:
                f.write(",")
            f.write("\n")
    f.write("\t]\n")
    f.write("}\n")
    f.close()

    return {'FINISHED'}


# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export.lights_camera_boop" 
    bl_label = "Boop!"

    # ExportHelper mixin class uses this
    filename_ext = ".json"

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    #use_setting: BoolProperty(
    #    name="Example Boolean",
    #    description="Example Tooltip",
    #    default=True,
    #)

    #type: EnumProperty(
    #    name="Example Enum",
    #    description="Choose between two items",
    #    items=(
    #        ('OPT_A', "First Option", "Description one"),
    #        ('OPT_B', "Second Option", "Description two"),
    #    ),
    #    default='OPT_A',
    #)

    def execute(self, context):
        return write_some_data(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="Lights, Camera, *boop* (.json)")


def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export.lights_camera_boop('INVOKE_DEFAULT')