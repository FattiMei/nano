# Nano
This repository is about making the *XYZ daVinci nano* an actually usable machine. There are three main lines of work (in ascending order of time and resource investment):

  1. 3w file format conversion
  2. Open filament
  3. New firmware

Please note that most of the information you find here will apply to other XYZ machines.


## License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


## 3w file format
Many XYZ machines work only with 3w files that are obfuscated gcode. If you want to convert gcode to 3w and viceversa, I've got a solution for you.


### Python script
The scripts I wrote need:

  * python 3
  * pycryptodome (`pip install pycryptodome`)
  * patience

At the moment I support only version 5 of the format, if you have any problem contact me at: teomei68 ''at'' gmail ''dot'' com.

  `python /nano/3w_analysis/python/to_gcode.py <filename>`

Converts a 3w file to gcode and dumps to stdout. If the file does not follow the specification, you will see some stack traces.


### C program
If you want *speed* I've got some C programs for you.
Dependencies:

  * Nettle
  * Zlib (probably already installed on your system)
  * Make
  * More patience

Go to `/nano/3w_analysis/c/build` and `make clean build`. This step might fail because the compiler can't find the header files, you're on your own.
After that `make regression_test` will produce a to_gcode.out native executable, it works exactly like the python script.

  `./to_gcode.out <filename>`


## Open filament
XYZ machines use special NFC chips to identify filament type, length and working temperature. Users have to buy "proprietary" filament unless they buy a "proprietary" chip called OpenSmartTag, which unlocks all filaments ever existed.

We want to solve this problem either by reverse-engineering the OpenSmartTag or by removing filament check in the firmware.


## New firmware
How about cleansing the machine and installing a new firmware? Sound cool.
This is the most difficult part of the job, since we don't know yet the motherboard layout. I consider two options:

  1. Repetier firmware, following instructions on online forums (Boring)
  2. Marlin port (My favourite)
