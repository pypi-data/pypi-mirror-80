import sys

if __name__ == "__main__":
    if len(sys.argv) == 0:
        sys.exit(0)

    else:

        f = sys.argv[1]
        in_block = False
        with open(f, 'r') as source:
            if len(sys.argv) == 1:
                for line in source.readlines():
                    if line.rstrip() == '~~~':
                        in_block = not in_block
                    elif in_block:
                        print(line.rstrip())

            elif sys.argv[2] == '--to-md':
                need_guard = True
                for line in source.readlines():
                    if line.rstrip() == '~~~':
                        in_block = not in_block
                    elif in_block:
                        print('    ' + line.rstrip())
                    else:
                        if line[:4] == '    ':
                            if need_guard:
                                print('    ---')
                            else:
                                need_guard = False
                        else:
                            need_guard = True

            elif sys.argv[2] == '--to-unu':
                for line in source.readlines():
                    if line.rstrip() == '~~~':
                        in_block = not in_block
                    elif in_block:
                        print(line.rstrip())
                    else:
                        pass
