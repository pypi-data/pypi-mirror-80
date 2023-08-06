# from .olatsm import ola
# from .wsolatsm import wsola
# from .pvtsm import phase_vocoder, phase_vocoder_int
# from .hptsm import hptsm
import argparse
import soundfile as sf


def run():
    parser = argparse.ArgumentParser(description='Processing time-scale modification for given audio file.')
    parser.add_argument('algorithm', nargs='?', choices=['ola', 'wsola', 'pv', 'pv_int', 'hp'])
    # parser.add_argument('--help', action='store_true')

    args, sub_args = parser.parse_known_args()

    if args.algorithm == 'ola':
        parser = argparse.ArgumentParser()
        parser.add_argument('input_file', nargs=1)
        parser.add_argument('output_file', nargs=1)
        parser.add_argument('alpha', nargs=1, type=float)
        parser.add_argument('--win_type', '-wt', default='hann', type=str)
        parser.add_argument('--win_size', '-ws', default=1024, type=int)
        parser.add_argument('--syn_hop_size', '-sh', default=512, type=int)
        pass
    elif args.algorithm == 'wsola':
        parser = argparse.ArgumentParser()
        parser.add_argument('input_file', nargs=1)
        parser.add_argument('output_file', nargs=1)
        parser.add_argument('alpha', nargs=1, type=float)
        parser.add_argument('--win_type', '-wt', default='hann', type=str)
        parser.add_argument('--win_size', '-ws', default=1024, type=int)
        parser.add_argument('--syn_hop_size', '-sh', default=512, type=int)
        parser.add_argument('--tolerance', '-t', default=512, type=int)
        pass
    elif args.algorithm == 'pv':
        parser = argparse.ArgumentParser()
        parser.add_argument('input_file', nargs=1)
        parser.add_argument('output_file', nargs=1)
        parser.add_argument('alpha', nargs=1, type=float)
        parser.add_argument('--win_type', '-wt', default='sin', type=str)
        parser.add_argument('--win_size', '-ws', default=2048, type=int)
        parser.add_argument('--syn_hop_size', '-sh', default=512, type=int)
        parser.add_argument('--zero_pad', '-z', default=0, type=int)
        parser.add_argument('--restore_energy', '-e', action='store_true')
        parser.add_argument('--fft_shift', '-fs', action='store_true')
        parser.add_argument('--phase_lock', '-pl', action='store_true')
        pass
    elif args.algorithm == 'pv_int':
        pass
    elif args.algorithm == 'hp':
        pass
    else:
        pass

    print(args)
    print(sub_args)
    print(parser.parse_args(sub_args))


if __name__ == '__main__':
    run()
