# 🌈 FORTH aka RAINBOW4TH is the big brother of 🐬 DOLPHIN [RETROFORTH](https://github.com/scott91e1/RETROFORTH) for Win32, Win64, Linux, MaxOS & WINE

### It is a Windows/UNIX, C++/Python/JAVA Powered FORTH Focused Polygot Environment with Multiple IDEs

https://github.com/scott91e1/RAINBOW4TH/blob/approved/LICENSE.md

MIT License

(c) 2020 - 2020, Scott McCallum [(https linkedin.com in Scott-McCallum)](https://linkedin.com/in/Scott-McCallum)

(c) 2008 - 2020, Charles Childers [(https github.com crcx)](https://github.com/crcx)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# VERSION: 1.0 ALPHA 

## "approved" branch is volatile and under routine development

Currently targeting generic Python 3.6+, Win32 and Win64 with Borland RAD Studio.  Higher performance for Python is achived when a more complete Python runtime (such as [Anaconda](https://www.anaconda.com/products/individual), [Active State](https://platform.activestate.com/Pizza-Team/Top-10-ML-Packages-Win) or *pip install numba*, *pip install pandas*, et al. ) is hosting.

# SPONSORSHIP: https://www.patreon.com/_crc

## Charles Childers is creating Retro, a modern, pragmatic Forth
 
http://forth.works/book.html

# TLDR

Building on Python all words become infinite precision.  Stack and memory under/over runs are checked.  Virtual Machine OS (VMOS) can be booted from its assembly and retroforth files in addition to pre-compiled .nga images.

Construindo em Python todas as palavras tornam-se precisão infinita.  A pilha e a memória são verificadas.  O SO de máquina virtual (VMOS) pode ser inicializado a partir dos seus ficheiros de montagem e retroforth, além de imagens .nga pré-compiladas.

Pythonで構築すると全ての単語が無限精度になります。スタックとメモリのアンダー/オーバーランをチェックします。Virtual Machine OS (VMOS)は、コンパイル済みの.ngaイメージに加えて、そのアセンブリとretroforthファイルから起動することができます。

# Raison D'être

## Architecture

RETRO has a multilayer design. At the heart of the system is a virtual machine called Nga. This emulates a 32-bit stack processor with a MISC based instruction set.

The core RETRO language is stored as a memory image for Nga. The *image file* contains this and is loaded on startup. It holds all of the compiled words and data and interacts with Nga.

The third layer is the user interface. RETRO doesn't specify any required I/O other than a console log capable of receiving a single character at a time. Each host system can implement this and any additional desired I/O by extending Nga.

## ENHANCEMENTS

# PROJECT LAYOUT

## Files in the top level

### embed.exe

### ngaImage

## pforth.dic

## pforth.exe

### retro.py

### retro_ide.py

### retro_ide_qt.py

### retro_ide.exe

### retro_ide_x86.exe

## Directories

### books

### build

### demos

### games

### image

### licenses

### tools

### vm

# FAQ

## Why is the main branch called approved?

As the major version numbers increment the policy for the default "approved" branch differs.  Consider 1.x to be internal develpment with approved being highly volatile.  The 2.x series is the beta testing/qa version and 3.x being the first stable version.  This comes from a software development addage that v1.0 is released too fast, v2.0 is what v1.0 should have been and v3.0 is the first real version.

All participants in the eco-system can simply clone the reposity and run the python code in the approved branch.  Development/testing will be performed in seperate branches and merged into approved with the changes are ready to go live.
