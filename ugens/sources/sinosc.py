from ugens.ugen import Ugen, ugen_parser
import sys
import json

def sinosc(freq, phase):
    if type(freq) == list:
        ugen = [Ugen('SinOsc',[freq[i], phase[i]]) for i in range(0, len(freq)) ]
    else:
        ugen = Ugen('SinOsc', [freq, phase])
    return ugen

if __name__ == '__main__':


    args_def = {
            'freq': {
                'help':'Frequency in Hert.',
                'default':440.0
                },
            'phase': {
                'help':'Phase in radians within the range +-8pi.',
                'default':0.0
                },
            }

    parse = ugen_parser(args_def)
    argv = sys.argv[1:]

    if len(argv) == 0:
        argv = ['400', '0.0']
    elif len(argv) == 1:
        argv = [argv[0], '0.0']

    args = parse(argv)
    
    ugen = sinosc(args['freq'], args['phase'])

    if type(ugen) == list:
        ugen = [u.serialize() for u in ugen]
        ugen = json.dumps(ugen)

        if sys.stdout.isatty():
            print(ugen)
        else:
            ugen = ugen.replace(' ','\x01')
    print(ugen)
