import sys

def videoCutter(filename, start, end):
    with open(filename) as f:
        lines = f.readlines()
        frames = []
        for frameID in range(start, end):
            frame = []
            for row in range(24):
                frame.append(lines[frameID * 24 + row])
            frames.append(frame)
    return frames

def writeVideo(filename, frames):
    with open(filename, 'w') as f:
        for frame in frames:
            for row in frame:
                f.write(row)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        filename = None
        start = None
        end = None
        output = None

        while not filename:
            filename = input('Enter filename: ')

        while not start:
            try:
                start = int(input('Enter start frame: '))
            except ValueError:
                print('Invalid input. Please enter an integer.')

        while not end:
            try:
                end = int(input('Enter end frame: '))
            except ValueError:
                print('Invalid input. Please enter an integer.')

        while not output:
            output = input('Enter output filename: ')
    else:
        filename = sys.argv[1]
        start = int(sys.argv[2])
        end = int(sys.argv[3])
        output = sys.argv[4]

    frames = videoCutter(filename + ".txt", start, end)
    writeVideo(output + ".txt", frames)
    print('Done')