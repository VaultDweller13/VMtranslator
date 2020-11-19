import sys

commands = ['pop', 'push', 'add', 'sub', 'neg',
            'eq', 'gt', 'lt', 'and', 'or', 'not']
segments = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT',
            'pointer': 'pointer'}


def main():
    filename = sys.argv[1]
    with open(filename + '.vm', 'r') as in_file, \
            open(filename + '.asm', 'w') as out_file:
        for line in in_file:
            if empty(line):
                continue
            out_file.write('// ' + line)
            line = parse(line)
            out_file.write(line + '\n')


def empty(line):
    if (line[:2] == '//') or (line.isspace()):
        return True


def parse(line):
    line = line.strip()
    components = line.split()
    command = components[0]
    mem_segment = 0
    num = 0
    if command in ('push', 'pop'):
        mem_segment = components[1]
        num = components[2]

    if command == 'push':
        line = push(mem_segment, num)
    if command == 'pop':
        line = pop(mem_segment, num)
    if command == 'add':
        line = add()
    if command == 'sub':
        line = sub()
    return line


# def push(mem_segment, num):
#     if mem_segment == 'constant':
#         s = '@{0}\n' \
#             'D=A\n' \
#             '@SP\n' \
#             'A=M\n' \
#             'M=D\n' \
#             '@SP\n' \
#             'M=M+1'.format(num)
#     else:
#         s = '@{0}\n' \
#             'D=A\n' \
#             '@{1}\n' \
#             'A=D+M\n' \
#             'D=M\n' \
#             '@SP\n' \
#             'A=M\n' \
#             'M=D\n' \
#             '@SP\n' \
#             'M=M+1'.format(num, segments.get(mem_segment))
#     return s

def push(mem_segment, num):
    if mem_segment == 'constant':
        label = 'D=A\n'
    else:
        if mem_segment == 'static':
            label = 'D=A\n' \
                    '@{0}\n' \
                    'A=D+M\n' \
                    'D=M\n'.format(sys.argv[1] + '.' + num)
        else:
            if mem_segment == 'temp':
                num = int(num) + 5
                label = 'D=A\n'
            else:
                label = 'D=A\n' \
                        '@{0}\n' \
                        'D=D+M\n'.format(segments.get(mem_segment))

    s = '@{0}\n' \
        '{1}'  \
        '@SP\n' \
        'A=M\n' \
        'M=D\n' \
        '@SP\n' \
        'M=M+1'.format(num, label)
    return s


def pop(mem_segment, num):
    if mem_segment == 'static':
        label = 'D=A\n' \
                '@{0}\n' \
                'A=D+M\n' \
                'D=M\n'.format(sys.argv[1] + '.' + num)
    else:
        if mem_segment == 'temp':
            num = int(num) + 5
            label = 'D=A\n'
        else:
            label = 'D=A\n' \
                    '@{0}\n' \
                    'D=D+M\n'.format(segments.get(mem_segment))

    s = '@{0}\n' \
        '{1}' \
        '@SP\n' \
        'A=M\n' \
        'M=D\n' \
        '@SP\n' \
        'M=M-1\n' \
        'A=M\n' \
        'D=M\n' \
        '@SP\n' \
        'M=M+1\n' \
        'A=M\n' \
        'A=M\n' \
        'M=D\n' \
        '@SP\n' \
        'M=M-1'.format(num, label)
    return s


def add():
    s = "@SP\n" \
        "M=M-1\n" \
        "A=M\n" \
        "D=M\n" \
        "@SP\n" \
        "M=M-1\n" \
        "A=M\n" \
        "M=M+D\n" \
        "@SP\n" \
        "M=M+1"
    return s


def sub():
    s = "@SP\n" \
        "M=M-1\n" \
        "A=M\n" \
        "D=M\n" \
        "@SP\n" \
        "M=M-1\n" \
        "A=M\n" \
        "M=M-D\n" \
        "@SP\n" \
        "M=M+1"
    return s


def translate(elements):
    pass


if __name__ == '__main__':
    main()