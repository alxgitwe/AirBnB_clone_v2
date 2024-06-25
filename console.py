#!/usr/bin/python3

"""
Unique Console Module
"""

import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class UniqueConsole(cmd.Cmd):
    """
    Contains the functionality for the Unique Console
    """
    prompt = '(unique) ' if sys.__stdin__.isatty() else ''

    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }

    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(unique)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax"""
        _cmd = _cls = _id = _args = ''
        if '.' in line and '(' in line and ')' in line:
            try:
                pline = line[:]
                _cls = pline[:pline.find('.')]
                _cmd = pline[pline.find('.') + 1:pline.find('(')]
                if _cmd not in UniqueConsole.dot_cmds:
                    raise Exception
                pline = pline[pline.find('(') + 1:pline.find(')')]
                if pline:
                    pline = pline.partition(', ')
                    _id = pline[0].replace('"', '')
                    pline = pline[2].strip()
                    if pline:
                        if pline[0] == '{' and pline[-1] == '}' and type(eval(pline)) is dict:
                            _args = pline
                        else:
                            _args = pline.replace(',', '')
                line = ' '.join([_cmd, _cls, _id, _args])
            except Exception as e:
                pass
        return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(unique) ', end='')
        return stop

    def do_quit(self, command):
        """Method to exit the Unique Console"""
        exit()

    def help_quit(self):
        """Prints the help documentation for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit()

    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        pass

    def do_create(self, args):
        """Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        if args[0] not in UniqueConsole.classes:
            print("** class doesn't exist **")
            return
        attr = {}
        if len(args) > 1:
            for i in range(1, len(args)):
                key, value = args[i].split("=")
                if value[0] == '"':
                    value = value.replace('_', ' ')
                    value = value[1:-1]
                elif '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                attr.update({key: value})
        new_instance = UniqueConsole.classes[args[0]](**attr)
        new_instance.save()
        storage.save()
        print(new_instance.id)

    def help_create(self):
        """Help information for the create method"""
        print("Creates a class of any type")
        print("[Usage]: create \n")

    def do_show(self, args):
        """Method to show an individual object"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]
        if not c_name:
            print("** class name missing **")
            return
        if c_name not in UniqueConsole.classes:
            print("** class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show \n")

    def do_destroy(self, args):
        """Destroys a specified object"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]
        if not c_name:
            print("** class name missing **")
            return
        if c_name not in UniqueConsole.classes:
            print("** class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy \n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []
        if args:
            args = args.split()[0]
            if args not in UniqueConsole.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all(UniqueConsole.classes[args]).items():
                print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))
        print(print_list)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all \n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """Help information for the count command"""
        print("Usage: count ")

    def do_update(self, args):
        """Updates a certain object with new info"""
        c_name = c_id = att_name = att_val = kwargs = ''
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:
            print("** class name missing **")
            return
        if c_name not in UniqueConsole.classes:
            print("** class doesn't exist **")
            return
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        if key not in storage.all():
            print("** no instance found **")
            return
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] == '"':
                second_quote = args.find('"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]
                args = args.partition(' ')
            if not att_name and args[0] != ' ':
                att_name = args[0]
            if args[2] and args[2][0] == '"':
                att_val = args[2][1:args[2].find('"', 1)]
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]
            args = [att_name, att_val]
        new_dict = storage.all()[key]
        for i, att_name in enumerate(args):
            if i % 2 == 0:
                att_val = args[i + 1]
                if not att_name:
                    print("** attribute name missing **")
                    return
                if not att_val:
                    print("** value missing **")
                    return
                if att_name in UniqueConsole.types:
                    att_val = UniqueConsole.types[att_name](att_val)
                new_dict.__dict__.update({att_name: att_val})
        new_dict.save()

    def help_update(self):
        """Help information for the update class"""
        print("Updates an object with new information")
        print("Usage: update \n")

if __name__ == "__main__":
    UniqueConsole().cmdloop()
