import json
import argparse
import re
import sys
import uuid

class Ugen:
    def __init__(self, name, inputs, calculation_rate=0, special_index=0, id_=None):
        self.name = name

        if type(inputs) != list or not all([type(k) == Ugen or type(k) == float for k in inputs]):
            raise Exception('inputs contain unsupported type.', [type(k) for k in inputs])
        self.inputs = inputs
        self.id = id_ if id_ != None else str(uuid.uuid1().int)[:10]
        self.calculation_rate = calculation_rate
        self.special_index = special_index
        self.type = 'ugen'
    
    def serialize(self):
        ugen_ = {
                'id': self.id,
                'type': self.type,
                "name": self.name,
                "inputs": [ inp.serialize() if type(inp) == Ugen else inp for inp in self.inputs],
                "calculation_rate": self.calculation_rate,
                "special_index": self.special_index,
                }
        return ugen_

    def __str__(self):
        data =  json.dumps(self.serialize())
        if sys.stdout.isatty():
            return data
        else:
            return data.replace(' ','\x01')


def ugen_float_list(arg):
    if type(arg) == list:
        # check if everything it's a number or a list of ugens/floats
        try:
            arg = [float(k)  for k in arg]
        except ValueError:
            argn = []
            for a in arg:
                try:
                    a = float(a)
                except ValueError:
                    a = a.replace('\0x01',' ')
                    a = json.loads(a.replace('\x01',' '))
                    a = Ugen(a['name'], a['inputs'], a['calculation_rate'], a['special_index'], a['id'])
                    argn.append(a)
            arg = argn

    else:
        # a string argument
        try:
            arg = float(arg)
        except ValueError:
            arg = arg.replace('\x01',' ')
            arg = json.loads(arg)

            if type(arg) == list:
                argn = []
                for a in arg:
                    try:
                        a = float(a)
                    except (ValueError, TypeError):
                        a = Ugen(a['name'], a['inputs'], a['calculation_rate'], a['special_index'], a['id'])
                        argn.append(a)
                arg = argn
            else:
                arg = Ugen(arg['name'], arg['inputs'], arg['calculation_rate'], arg['special_index'], arg['id'])

    return arg


def expand_arg_repeat(arg, m):
    for i in range(m-len(arg)):
        arg.append(arg[i])
    return arg


def preprocess_args(args):
    # replace math operators
    args = [k.replace('+', '--add') for k in args] 
    args = [k.replace('*', '--mult') for k in args] 

    args = [k.split() for k in args]

    if all([len(k) == 1 for k in args]):
        args = [k[0] for k in args]

    args = [k[0] if len(k) == 1 and type(k[0]) == str else k for k in args]

    return args


def ugen_parser(args_def, add_math_operators=True):
    parser = argparse.ArgumentParser()
    parser_optional = argparse.ArgumentParser()

    for arg in args_def:
        parser.add_argument(arg,
                help=f"{args_def[arg]['help']} default: {args_def[arg]['default']}",
                default=args_def[arg]['default'],
                type=ugen_float_list if args_def.get('type') == None else args_def.get('type')
                )

    for arg in args_def:
        parser.add_argument(
                f'--{arg}',
                help=f"same as {arg}",
                nargs='+',
                type=ugen_float_list if args_def.get('type') == None else args_def.get('type')
                )

    if add_math_operators:
        parser.add_argument(
                f'--add',
                help=f"This value will be added to the output.",
                type=ugen_float_list
                )

        parser.add_argument(
                    f'--mult',
                help=f"Output will be multiplied by this value.",
                type=ugen_float_list
                )

    def wrapper(args):
        args = preprocess_args(args)
        args = parser.parse_args(args)
        
        arg_dest = {}

        maxl = 1
        for arg in args_def:
            arg_dest[arg] = getattr(args, arg) 
            maxl = max(maxl, len(arg_dest[arg]) if type(arg_dest[arg]) == list else 1)

        for arg, value in arg_dest.items():
            arg_dest[arg] = expand_arg_repeat(value if type(value) == list else [value], maxl)


        if all([len(k)==1 for k in arg_dest.values()]):
            for arg in arg_dest:
                arg_dest[arg] = arg_dest[arg][0]

        return arg_dest

    return wrapper
