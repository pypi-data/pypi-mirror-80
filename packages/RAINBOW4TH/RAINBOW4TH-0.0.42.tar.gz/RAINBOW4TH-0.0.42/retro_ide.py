
license_txt = """ 

MIT License

Copyright (c) 2020 - 2020, linkedin.com/in/Scott-McCallum

Copyright (c) 2010 - 2020, Charles Childers

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: 

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

title_txt = "RETROFORTH IDE v1.0 (2020.4)"

#
# tkinter framework from www.geeksforgeeks.org/make-notepad-using-tkinter
#

import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *


class RETRO_VM:

    def __init__(self, words=100000):
        self.ip = [0]
        self.stack = [] * 256
        self.address = []
        self.memory = []
        self.memory_max = words

    def extractString(self, at):
        i = at
        s = ''
        while self.memory[i] != 0:
            s = s + chr(self.memory[i])
            i = i + 1
        return s

    def findEntry(self, named):
        header = self.memory[2]
        Done = False
        while header != 0 and not Done:
            if named == self.extractString(header + 3):
                Done = True
            else:
                header = self.memory[header]
        return header

    def injectString(self, s, to):
        i = to
        for c in s:
            self.memory[i] = ord(c)
            i = i + 1
        self.memory[i] = 0

    def execute(self):

        ip, stack, memory, address = (self.ip, self.stack, self.memory, self.address)

        def rxGetInput():
            return ord(sys.stdin.read(1))

        def rxDisplayCharacter():
            if stack[-1] > 0 and stack[-1] < 128:
                if stack[-1] == 8:
                    sys.stdout.write(chr(stack.pop()))
                    sys.stdout.write(chr(32))
                    sys.stdout.write(chr(8))
                else:
                    sys.stdout.write(chr(stack.pop()))
            else:
                sys.stdout.write("\033[2J\033[1;1H")
                stack.pop()
            sys.stdout.flush()

        def i_no():
            return True

        def i_li():
            ip[0] += 1
            stack.append(memory[ip[0]])
            return True

        def i_du():
            stack.append(stack[-1])
            return True

        def i_dr():
            stack.pop()
            return True

        def i_sw():
            a = stack[-2]
            stack[-2] = stack[-1]
            stack[-1] = a
            return True

        def i_pu():
            address.append(stack.pop())
            return True

        def i_po():
            stack.append(address.pop())
            return True

        def i_ju():
            ip[0] = stack.pop() - 1
            return True

        def i_ca():
            address.append(ip[0])
            ip[0] = stack.pop() - 1
            return True

        def i_cc():
            target = stack.pop()
            if stack.pop() != 0:
                address.append(ip[0])
                ip[0] = target - 1
            return True

        def i_re():
            ip[0] = address.pop()
            return True

        def i_eq():
            a = stack.pop()
            b = stack.pop()
            if b == a:
                stack.append(-1)
            else:
                stack.append(0)
            return True

        def i_ne():
            a = stack.pop()
            b = stack.pop()
            if b != a:
                stack.append(-1)
            else:
                stack.append(0)
            return True

        def i_lt():
            a = stack.pop()
            b = stack.pop()
            if b < a:
                stack.append(-1)
            else:
                stack.append(0)
            return True

        def i_gt():
            a = stack.pop()
            b = stack.pop()
            if b > a:
                stack.append(-1)
            else:
                stack.append(0)
            return True

        def i_fe():
            if stack[-1] == -1:
                stack[-1] = len(stack) - 1
            elif stack[-1] == -2:
                stack[-1] = len(address)
            elif stack[-1] == -3:
                stack[-1] = len(memory)
            elif stack[-1] == -4:
                stack[-1] = -9223372036854775808  # normal memory unbounded, 64bit for persistent memory
            elif stack[-1] == -5:
                stack[-1] = 9223372036854775807  # normal memory unbounded, 64bit for persistent memory
            else:
                stack[-1] = memory[stack[-1]]
            return True

        def i_st():
            mi = stack.pop()
            memory[mi] = stack.pop()
            return True

        def i_ad():
            t = stack.pop()
            stack[-1] += t
            return True

        def i_su():
            t = stack.pop()
            stack[-1] -= t
            return True

        def i_mu():
            t = stack.pop()
            stack[-1] *= t
            return True

        def i_di():
            a = stack[-1]
            b = stack[-2]

            q, r = divmod(abs(b), abs(a))
            if a < 0 and b < 0:
                r *= -1
            elif a > 0 and b < 0:
                q *= -1
            elif a < 0 and b > 0:
                r *= -1
                q *= -1

            stack[-1] = q
            stack[-2] = r
            return True

        def i_an():
            t = stack.pop()
            stack[-1] &= t
            return True

        def i_or():
            t = stack.pop()
            stack[-1] |= t
            return True

        def i_xo():
            t = stack.pop()
            stack[-1] ^= t
            return True

        def i_sh():
            t = stack.pop()
            if t < 0:
                stack[-1] <<= (t * -1)
            else:
                stack[-1] >>= t
            return True

        def i_zr():
            if stack[-1] == 0:
                stack.pop()
                ip[0] = address.pop()
            return True

        def i_ha():
            ip[0] = 9000000
            return True

        def i_ie():
            stack.push(1)
            return True

        def i_iq():
            stack.pop()
            stack.push(0)
            stack.push(0)
            return True

        def i_ii():
            stack.pop()
            rxDisplayCharacter()
            return True

        instructions = [i_no, i_li, i_du, i_dr, i_sw, i_pu, i_po, i_ju,
                        i_ca, i_cc, i_re, i_eq, i_ne, i_lt, i_gt, i_fe,
                        i_st, i_ad, i_su, i_mu, i_di, i_an, i_or, i_xo,
                        i_sh, i_zr, i_ha, i_ie, i_iq, i_ii]

        def inner(word):

            ip[0] = word
            address.append(0)

            while ip[0] < 100000 and len(address) > 0:
                opcode = memory[ip[0]]
                instructions[opcode & 0xFF]()
                instructions[(opcode >> 8) & 0xFF]()
                instructions[(opcode >> 16) & 0xFF]()
                instructions[(opcode >> 24) & 0xFF]()
                ip[0] = ip[0] + 1

        return inner

    def load(self, source):
        cells = int(os.path.getsize(source) / 4)
        f = open(source, 'rb')
        self.memory = list(struct.unpack(cells * 'i', f.read()))
        f.close()
        remaining = self.memory_max - cells
        self.memory.extend([0] * remaining)

    def load_muri(self, source):

        i_two = {}
        i_var = {}

        instructions = ['nop', 'lit', 'dup', 'drop', 'swap', 'push', 'pop', 'jump', 'call', 'ccall', 'ret',
                        'eq', 'neq', 'lt', 'gt', 'fetch', 'store', 'add', 'sub', 'mul', 'div', 'and', 'or', 'xor',
                        'shift', 'zret', 'halt',
                        'ienum', 'iquery', 'iinvoke']

        for instruction in instructions:
            i_two[instruction[:2]] = len(i_two)
            i_var[instruction] = len(i_var)

        i_two['..'] = 0

        lines = []
        include = False
        for line in open(source, encoding='utf-8').readlines():
            if line[:3] == '~~~':
                include = not include
                continue
            if not include:
                continue
            line = line.strip()
            if len(line):
                lines.append(line)

        print("Pass 1\n")

        offsets = {}
        for line in lines:
            print("%04i %s" % (len(self.memory), line))
            if line[0] == 'i':
                I0, I1, I2, I3 = (line[2:4], line[4:6], line[6:8], line[8:10])
                opcode = (i_two[I0]) + (i_two[I1] << 8) + (i_two[I2] << 16) + (i_two[I3] << 24)
                self.memory.append(opcode)
            elif line[0] == 'r':
                self.memory.append(-1)
            elif line[0] == 'd':
                self.memory.append(int(line[2:]))
            elif line[0] == 's':
                for c in iter(line[2:]):
                    self.memory.append(ord(c))
                self.memory.append(0)
            elif line[0] == 'a':  # alloc n words of 0
                self.memory.expand([0] * int(line[2:]))
            elif line[0] == ':':
                offsets[line[2:]] = len(self.memory)

        print("\n\nPass 2\n")

        offset = 0
        for line in lines:
            if line[0] == 'i':
                offset = offset + 1
            elif line[0] == 'r':
                print("%04i %s = %i" % (offset, line, offsets[line[2:]]))
                self.memory[offset] = offsets[line[2:]]
                offset = offset + 1
            elif line[0] == 'd':
                offset = offset + 1
            elif line[0] == 's':
                offset = offset + len(line[2:]) + 1
            elif line[0] == 'a':
                offset = offset + int(line[2])
            elif line[0] == ':':
                pass

        remaining = self.memory_max - len(self.memory)
        self.memory.extend([0] * remaining)

    def firmware_add(self, source):

        print()
        print(Fore.GREEN + source + Fore.RESET)

        POW4TH_engine = self.execute()

        interpret = self.memory[self.findEntry('interpret') + 1]
        include = False
        line_number = 0
        for line in open(source, encoding='utf-8').readlines():
            line_number = line_number + 1
            if line[:3] == '~~~':
                include = not include
                continue
            line = line.strip()
            if not include or len(line) == 0:
                continue
            print('%04i %s' % (line_number, line))
            for token in line.split(' '):
                if not token.strip == '':
                    self.injectString(token, 1025)
                    self.stack.append(1025)
                    POW4TH_engine(interpret)

    def interact(self):

        POW4TH_engine = self.execute()
        interpret = self.memory[self.findEntry('interpret') + 1]

        while True:
            line = input(Fore.GREEN + '\nPOW4TH' + Fore.RESET + ' ' + str(len(self.stack)) +'> ')
            if line == 'bye':
                return

            if line == '':
                print(Fore.GREEN + 'STACK: ' + Fore.YELLOW + repr(self.stack) + Fore.RESET)
                continue

            tokens = fson.loads(line)

            print(Fore.GREEN + 'RETRO: ' + Fore.YELLOW + ' '.join(tokens) + Fore.RESET)
            for token in tokens:
                self.injectString(token, 1025)
                self.stack.append(1025)
                POW4TH_engine(interpret)

def interact():
    vm = POW4TH_VM()

    if build:
        vm.load_muri("POW4TH-BIOS.muri")
        vm.load_retro("POW4TH-OS.retro")
    else:
        vm.load("ngaImage")

    vm.interact()


class RETRO_IDE:

    __root = Tk()

    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __thisTextArea = Text(__root)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisREPLMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    # To add scrollbar
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self ,**kwargs):

        # Set window size (the default is 600x600)

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.__root.title("Untitled - " + title_txt)

        # Center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # For left-alling
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # For right-allign
        top = (screenHeight / 2) - (self.__thisHeight /2)

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                              self.__thisHeight,
                                              left, top))

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__thisTextArea.grid(sticky=N + E + S + W)

        # To open new file
        self.__thisFileMenu.add_command(label="New",
                                        command=self.__newFile)

        # To open a already existing file
        self.__thisFileMenu.add_command(label="Open",
                                        command=self.__openFile)

        # To save current file
        self.__thisFileMenu.add_command(label="Save",
                                        command=self.__saveFile)

        # To create a line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit",
                                        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File",
                                       menu=self.__thisFileMenu)

        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut",
                                        command=self.__cut)

        # to give a feature of copy
        self.__thisEditMenu.add_command(label="Copy",
                                        command=self.__copy)

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste",
                                        command=self.__paste)

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit",
                                       menu=self.__thisEditMenu)

        # To give a feature of cut
        self.__thisREPLMenu.add_command(label="Try: Always Rollback",
                                        command=self.__cut)

        # to give a feature of copy
        self.__thisREPLMenu.add_command(label="Apply: Rollback on Failure",
                                        command=self.__copy)

        # To give a feature of paste
        self.__thisREPLMenu.add_command(label="Undo: Rollback Success",
                                        command=self.__paste)

        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="REPL [F5=Try, F6=Apply. F7=Undo]",
                                       menu=self.__thisREPLMenu)

        # To create a feature of description of the notepad
        self.__thisHelpMenu.add_command(label="About RETROFORTH IDE",
                                        command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help",
                                       menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar will adjust automatically according to the content
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __quitApplication(self):
        self.__root.destroy()

    # exit()

    def __showAbout(self):
        showinfo("POW4TH", license_txt.strip())

    def __openFile(self):

        self.__file = askopenfilename(defaultextension=".forth",
                                      filetypes=[("All Files", "*.*"),
                                                 ("RETROFORTH Source", "*.forth")])

        if self.__file == "":

            # no file to open
            self.__file = None
        else:

            # Try to open the file
            # set the window title
            self.__root.title(os.path.basename(self.__file) + " - " + title_txt)
            self.__thisTextArea.delete(1.0, END)

            file = open(self.__file, "r")

            self.__thisTextArea.insert(1.0, file.read())

            file.close()

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):

        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.pow4th',
                                            defaultextension=".pow4th",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents", "*.forth")])

            if self.__file == "":
                self.__file = None
            else:

                # Try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisTextArea.get(1.0, END))
                file.close()

                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - POW4TH")


        else:
            file = open(self.__file, "w")
            file.write(self.__thisTextArea.get(1.0, END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):

        # Run main application
        self.__root.mainloop()


ide = RETRO_IDE(width=600, height=600)
ide.run()
