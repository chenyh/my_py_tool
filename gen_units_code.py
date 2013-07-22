#-*- coding:utf-8 -*-

#from win32com.client import Dispatch


code_template = '''
using System;
using System.Collections.Generic;
using System.Text;
using Brainiac.Design.Attributes;
using StoryPlugin.Properties;
using StoryPlugin;
using Brainiac.Design;

namespace StoryPlugin.Nodes
{
    %(AllClasses)s	

    class ActionSet
    {
        public void AddActions(NodeGroup actions) {
            // actions.Items.Add(typeof(Nodes.ActionCharPlayAction));
	    %(ClassesAdd)s
        }
    }
}

'''

class_template = u'''
	class %(ClassName)s : StoryAction {
		%(ClassMembers)s
                protected override void CloneProperties(Brainiac.Design.Nodes.Node newnode)
                {
                    base.CloneProperties(newnode);
                    %(ClassName)s node = (%(ClassName)s)newnode;
		    %(MembersSetValue)s
                }
		public %(ClassName)s()
			: base("%(Label)s" , "%(Description)s")
		{
			_action_type = "%(ActionType)s";
		}
	}
'''

int_member_template = '''
	protected int _%(MemberName)s = %(DefaultValue)s;
 	[DesignerInteger("%(MemberName)s", "", "CategoryBasic", DesignerProperty.DisplayMode.List, 0, DesignerProperty.DesignerFlags.NoFlags, %(Min)d, %(Max)d, 1, "%(Unit)sMeters")]
        public int %(MemberName)s
        {
            get { return _%(MemberName)s; }
            set { _%(MemberName)s = value; }
        }
'''

str_member_template = '''
        protected string _%(MemberName)s = "%(DefaultValue)s";
        [DesignerString("%(MemberName)s", "", "CategoryBasic", DesignerProperty.DisplayMode.NoDisplay, 0, DesignerProperty.DesignerFlags.NoFlags)]       
        public string %(MemberName)s
        {
            get { return _%(MemberName)s; }
            set { _%(MemberName)s = value; }
        }
'''

def gen_int_member(membername, defaultval, min, max):
	params = {
		"MemberName" : membername, 
		"Min" : min, 
		"Max" : max, 
		"DefaultValue" : defaultval,
		"Unit" : ""
	}
	return int_member_template % params

def gen_str_member(membername, defaultval):
	params = {
		"MemberName" : membername, 
		"DefaultValue" : defaultval,
	}
	return str_member_template % params

def gen_class(classname, classmembers, label, description, actiontype):
	params = {
		"ClassName" : classname,
		"Label" : label,
		"Description" : description,
		"ActionType" : actiontype
	}
	ClassMembers = ""
	MembersSetValue = ""
	for member_str in classmembers: 
		member_list = member_str.split(",")
		name = member_list[0]
		type = member_list[1]
		size = len(member_list)
		member_code = ""
		if type == u"int":
			defaultvalue = ((size > 2) and [int(member_list[2])] or [1])[0]
			min = ((size > 3) and [int(member_list[3])] or [0])[0]
			max = ((size > 4) and [int(member_list[4])] or [9999999])[0]
			member_code = gen_int_member(name, defaultvalue, min, max)
		else:
			defaultvalue = ((size > 2) and [member_list[2]] or [1])[0]
			member_code = gen_str_member(name, defaultvalue)
		ClassMembers += member_code + "\n"
		MembersSetValue += "node._%s = _%s;\n"%(name, name)

	params["ClassMembers"] = ClassMembers
	params["MembersSetValue"] = MembersSetValue
			
	return class_template%params
	'''ClassName, ClassMembers, MembersSetValue, Label, Description, ActionType'''
	

def gen_class_name(actionkey):
	return "Action%s"%actionkey.upper()

def gen_code(file):
	sheet_name = "units"
	xls_mod = __import__("xls_parse")
	xls = xls_mod.easy_excel(file)
	sheet = xls.get_sheet(sheet_name)

	AllClasses = ""
	ClassesAdd = ""
	for row in range(1, sheet.nrows):
		name = sheet.cell_value(row, 0)
		label = sheet.cell_value(row, 1)
		description = sheet.cell_value(row, 2)

		members = []
		classname = gen_class_name(name)
		index = 1
		for col in range(3, sheet.ncols):
			arg_str	= sheet.cell_value(row, col)
			if not arg_str:
				break
			members.append(arg_str)
		class_code = gen_class(classname, members, label, description, name)
		AllClasses += class_code + "\n"
		ClassesAdd += "actions.Items.Add(typeof(Nodes.%s));\n"%(classname)
		
	return code_template%{"AllClasses":AllClasses, "ClassesAdd":ClassesAdd}
	
if __name__ == '__main__':
	data = gen_code("play_units.xls")
	Util = __import__("util")
	Util.write_file("ActionSet.cs", data, "gbk")
