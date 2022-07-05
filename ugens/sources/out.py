from ugens.ugen import Ugen, ugen_parser
import sys


def out(bus, channels):
    ugen = Ugen('Out',[bus, *channels])
    return ugen

if __name__ == '__main__':
    
    args_def = {
            'bus': {
                'help': 'The index of the bus to write out to. The lowest numbers are written to the audio hardware.',
                'default': 0,
                'type': float,
                },
            'channels': {
                'help': 'An Array of channels or single output to write out. You cannot change the size of this once a SynthDef has been built.',
                'default': None
                }
            }

    parse = ugen_parser(args_def, add_math_operators=False)
    argv = sys.argv[1:]
    args = parse(argv)
    args['bus'] = args['bus'][0] if type(args['bus']) == list else args['bus']
    args['channels'] = [args['channels']] if type(args['channels']) != list else args['channels']

    ugen = out(args['bus'], args['channels'])
    print(ugen)
