from ugens.ugen import Ugen, ugen_parser
import sys

def add(inputs):
    if all([type(k) in (Ugen, str, float) for k in inputs]):
        print('types', len(inputs)//4, inputs)
        while len(inputs)>1:
            inputs_ = []
            for x in range(0, len(inputs), 4):
                inputs_.append(inputs[x:x+4])
            inputs = inputs_
        print('inputs', inputs)

if __name__ == '__main__':

    args_def = {
            "in":{
                "help": "The array of channels or arrays.",
                "default":None,
                "nargs": '+'
                }
            }

    parse = ugen_parser(args_def)

    if len(sys.argv[1:])==1:
        print(sys.argv[1:][0],file=sys.stderr)
    else:
        argv = ['0', '--in']

        for arg in sys.argv[1:]:
            argv.append(arg)

        args = parse(argv)
        add(args['in'])
        print(args)


