# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

import bpy
from bpy.types import Operator
from bpy.props import StringProperty


class ConsoleExec(Operator):
    '''Execute the current console line as a python expression'''
    bl_idname = "console.execute"
    bl_label = "Console Execute"

    def execute(self, context):
        sc = context.space_data

        module = __import__("console_" + sc.language)
        execute = getattr(module, "execute", None)

        if execute:
            return execute(context)
        else:
            print("Error: bpy.ops.console.execute_%s - not found" %
                  sc.language)
            return {'FINISHED'}


class ConsoleAutocomplete(Operator):
    """Evaluate the namespace up until the cursor and give a list of """ \
    """options or complete the name if there is only one"""
    bl_idname = "console.autocomplete"
    bl_label = "Console Autocomplete"

    def execute(self, context):
        sc = context.space_data
        module = __import__("console_" + sc.language)
        autocomplete = getattr(module, "autocomplete", None)

        if autocomplete:
            return autocomplete(context)
        else:
            print("Error: bpy.ops.console.autocomplete_%s - not found" %
                  sc.language)
            return {'FINISHED'}


class ConsoleBanner(Operator):
    '''Print a message when the terminal initializes'''
    bl_idname = "console.banner"
    bl_label = "Console Banner"

    def execute(self, context):
        sc = context.space_data

        # default to python
        if not sc.language:
            sc.language = 'python'

        module = __import__("console_" + sc.language)
        banner = getattr(module, "banner", None)

        if banner:
            return banner(context)
        else:
            print("Error: bpy.ops.console.banner_%s - not found" %
                  sc.language)
            return {'FINISHED'}


class ConsoleLanguage(Operator):
    '''Set the current language for this console'''
    bl_idname = "console.language"
    bl_label = "Console Language"

    language = StringProperty(
            name="Language",
            maxlen=32,
            )

    def execute(self, context):
        sc = context.space_data

        # default to python
        sc.language = self.language

        bpy.ops.console.banner()

        # insert a new blank line
        bpy.ops.console.history_append(text="", current_character=0,
            remove_duplicates=True)

        return {'FINISHED'}
