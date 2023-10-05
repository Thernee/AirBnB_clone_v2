#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) '

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_quit(self, line):
        """ Method to exit the HBNB console"""
        return

    def do_EOF(self, line):
        """ Handles EOF to exit program """
        print()
        return

    def do_create(self, line):
        """Creates a new instance of a class"""
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """ Method to show an individual object """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            if my_list[0] not in classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        """ Destroys a specified object """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")
            if my_list[0] not in classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """ Shows all objects, or all objects of a class"""
        if not line:
            obj = storage.all()
            print([obj[k].__str__() for k in obj])
            return
        try:
            args = line.split(" ")
            if args[0] not in classes:
                raise NameError()

            obj = storage.all(eval(args[0]))
            print([obj[k].__str__() for k in obj])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        """ Updates a certain object with new info """
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key not in objects:
                raise KeyError()
            if len(my_list) < 3:
                raise AttributeError()
            if len(my_list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[my_list[2]] = eval(my_list[3])
            except Exception:
                v.__dict__[my_list[2]] = my_list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        """count the number of class instances"""
        counter = 0
        try:
            my_list = split(line, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            obj = storage.all()
            for key in obj:
                name = key.split('.')
                if name[0] == my_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def default(self, line):
        """Process instances of a class."""
        new_list = line.split('.')
        if len(new_list) >= 2:
            if new_list[1] == "all()":
                self.do_all(new_list[0])
            elif new_list[1] == "count()":
                self.count(new_list[0])
            elif new_list[1][:4] == "show":
                self.do_show(self._parse(new_list))
            elif new_list[1][:7] == "destroy":
                self.do_destroy(self._parse(new_list))
            elif new_list[1][:6] == "update":
                tokens = self._parse(new_list)
                if isinstance(tokens, list):
                    obj = storage.all()
                    key = tokens[0] + ' ' + tokens[1]
                    for k, v in tokens[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(tokens)
        else:
            cmd.Cmd.default(self, line)

    def _parse(self, args):
        """Strip given arguments to return a string."""
        my_list = []
        my_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            cmd_string = args[1][args[1].find('(')+1:args[1].find(')')]
            my_list.append(((cmd_string.split(", "))[0]).strip('"'))
            my_list.append(my_dict)
            return my_list
        cmd_string = args[1][args[1].find('(')+1:args[1].find(')')]
        my_list.append(" ".join(cmd_string.split(", ")))
        return " ".join(cmd for cmd in my_list)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
