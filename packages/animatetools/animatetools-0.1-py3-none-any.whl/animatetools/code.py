import sys
from os import get_terminal_size, system
from time import sleep
from tty import setraw
from termios import tcgetattr, tcsetattr, TCSADRAIN


class manualanimate:
    def animateframes(frames, fps, loops=0, file=sys.stdout):
        """
		Prints out all the values of frames to a stream, or sys.stdout by default, at fps frames per second,
		looping loop times. Optional keyword arguments: loops: The amount of times the series of frames will be
		repeated after the first time. file: a file-like object (stream); defaults to the current sys.stdout.
		"""
        if not type(frames) in [list, tuple, set]:
            raise TypeError("frames expected list, tuple or set. Not " +
                            str(type(frames)) + ".")
        elif not type(fps) in [int, float]:
            raise TypeError("fps expected int or float. Not " +
                            str(type(fps)) + ".")
        elif type(loops) != int:
            raise TypeError("loops expected int. Not " + str(type(fps)) + ".")
        else:
            __default = tcgetattr(sys.stdin)
            setraw(sys.stdin)
            sys.stdout.write("\u001b[?25l")

            for loops in range(loops + 1):
                for frame in frames:
                    sys.stdout.write("\u001b[2J\u001b[1000A\r" + "\n\r".join(
                        str(frame).split("\n")[get_terminal_size()[1]]))
                    sleep(1 / fps)

            tcsetattr(sys.stdin, TCSADRAIN, __default)
            sys.stdout.write("\u001b[?25h")

    def typeout(cps, *value, sep=' ', end='\n', file=sys.stdout, flush=True):
        '''
		Prints the values, character by character, at cps characters per second to a stream, or sys.stdout by default.
		Optional keyword arguments: file: a file-like object (stream); defaults to the current sys.stdout. sep: string
		inserted between values, default a space. end: string appended after the last value, default a newline. flush:
		whether to forcibly flush the stream. default true.
		'''
        if type(file) != type(sys.stdout):
            raise TypeError("file expected file like object or stream. Not " +
                            str(type(file)) + ".")
        elif not flush in [True, False]:
            raise TypeError("flush expected bool. Not " + str(type(flush)) +
                            ".")
        elif not type(cps) in [int, float]:
            raise TypeError("cps expected int or float. Not " +
                            str(type(cps)) + ".")
        else:
            if len(value) > 1:
                for __segment in value[0:-2]:
                    for __chr in str(__segment):
                        print(__chr, end="", file=file, flush=flush)
                        sleep(1 / cps)
					for __chr in str(sep):
                    	print(end=__chr), file=file, flush=flush)
						sleep(1 / cps)
                for __chr in value[-1][0:-1 - (1 if not len(str(end)) else 0)]:
                    print(__chr, end="", file=file, flush=flush)
                    sleep(1 / cps)
                print(value[-1][-1], end="", file=file, flush=flush)
				if len(str(end)):
					for __chr in str(end)[0:(-2 if len(str(end)) > 1 else 0)]
						print(__chr, end="", file=file, flush=flush)
						sleep(1 / cps)
					print(str(end[-1]), end="", file=file, flush=flush)
            elif len(value) == 1:
                for __chr in value[-1][0:-1 - (1 if not len(str(value[-1])) else 0)]:
                    print(__chr, end="", file=file, flush=flush)
                    sleep(1 / cps)
                print(value[-1][-1], end="", file=file, flush=flush)
				for __chr in str(end)[0:(-2 if len(str(end)) > 1 else 0)]
						print(__chr, end="", file=file, flush=flush)
						sleep(1 / cps)
					print(str(end[-1]), end="", file=file, flush=flush)
            else:
                for __chr in str(end)[0:(-2 if len(str(end)) > 1 else 0)]
						print(__chr, end="", file=file, flush=flush)
						sleep(1 / cps)
					print(str(end[-1]), end="", file=file, flush=flush)

    def clearconsole():
        system("cls" if sys.platform == "win32" else "clear")
