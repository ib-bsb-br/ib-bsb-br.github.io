---
title: DP-Q803P thermal printer manual
date: 2024-01-23 01:00:00 -02:00
categories:
- Tutorial
tags:
- linux
comment: http://dp-dapper.com/
info: fechado.
type: post
layout: post
---

# Safety instructions

4.  The printer should be kept away from water sources and away from direct sunlight, strong light and heat sources.

Xiamen Dapu Electronic Technology Co., Ltd.

1.  The printer should be installed on a flat and stable place.

1\. Introduction and overview

3.  Leave enough space around the printer for maintenance and operation.

To turn on printing

10.  Do not allow humid air to condense on the surface of the printer. If it has formed, do not allow it to condense until the dew is removed.

ÿ warning

The print head is a heating component. Do not touch the print head and surrounding components during the printing process and immediately after printing.

6.  If the printer will not be used for a long time, please disconnect the printer power.
    
7.  Do not use or store the printer in places with high temperature, high humidity, or serious pollution.
    

Please read the following precautions carefully before operating the printer.

ÿ Precautions

bg4.png

9.  When meeting the usage requirements, it is recommended to set the printing density as low as possible to avoid affecting the printing quality.
    
10.  The printer must not print without paper, otherwise the print head will be seriously damaged.
    

Do not touch the print head and connection plug-in to avoid damage to the print head due to static electricity.

8.  In order to ensure printing quality and product life, it is recommended to use recommended or equivalent quality paper.

1

2.  Avoid placing the printer in places subject to vibration and shock.

life.

Use of print head

bgf.png

11.  Avoid water or conductive substances (such as metal) from entering the printer. If this occurs, shut down immediately.

• With label verification function, send calibration instruction data to printing

damage.

The label paper needs to be recalibrated to find gaps in the label.

12.  When plugging or disconnecting each interface, the power must be turned off, otherwise the printer control circuit may be damaged.

Calibrate now. Paper of the same specification only needs to be calibrated once. Change to other specifications

• The paper shortage status will be automatically restored, and the paper shortage honey detector will beep three times.

14.  Keep this manual properly for reference.

DP-Q803 can support thermal label paper and thermal continuous paper, and the maximum printing paper width is 79mm. This product is mainly used for

electronically printed labels or

• Equipped with cutter function, you can set full or half cutting.

• Label and ticket mode.

13.  Users are not allowed to disassemble the printer for maintenance without authorization.

1.1 Main features

machine power supply.

• Low noise and reliable performance

• Integrated mechanism design

Receipts can also be used in other situations where labels or receipts need to be printed. Q803 connects devices through USB, TTL, and RS232 interfaces.

• Plug and play, easy to use

Turn off the power.

1F 63

79mm

• Paper roll outer diameter ÿ

bg10.png

90mm/s

The light will flash three times, and at the same time, the paper-out status data will be returned to the host computer.

Product number

RS232+TTL+USB

• Maximum printing speed

Communication Interface

Peak current

1.8-2.2A

Xiamen Dapu Electronic Technology Co., Ltd.

2

default

baud rate

bg5.png

2.1 Technical specifications

led

12V/24V

115200

2\. Main technical specifications

Operating Voltage

• Automatically reply to the printing completion and printing failure status. When printing is completed, the printing completion status data will be returned to the host

computer.

Q803

Normal working current

Working current

bg11.png

Black and white output

Paper roll specifications

printing method

Thermal Paper

/

(thickness)

bg6.png

Thermal printing

3 paper roll diameter

90mm/s

0.05mm

(width)

3A

Paper roll type

0.05~0.1mm

resolution

40~79mm

printing speed

203dpi 8 dots/mm 576 dots per line

±

Xiamen Dapu Electronic Technology Co., Ltd.

Print color

label

bg12.png

Platform support

100

Text, graphics, characters, barcodes, QR codes

Paper cutting method

Windows, linux, and Android, STM32, 51 microcontroller

USB/

Serial communication can be connected to an Android tablet

Automatic paper cutting supports full cutting and half cutting

2.2

Dimensions

The interface supports computer systems such as

XP/Win7/Win8

Paperless bin design

134x56x76mm (length x width x height)

You can use the driver to print,

kilometer

Remark

black

Product color

USB

Print, provide Android development kits, and provide technical support and guidance.

Service life

Print content

bg13.png

2.2.1 Paper roll parameters

maximum(

mm)

apaper width

:External

mm)

• Paper type: thermal label paper, thermal continuous paper

code name

b

Paper roll thickness

Printing consumables technical indicators

meaning

0.1

• Paper width

80

2.2.2 Continuous paper parameters

: 40mm-80mm

40

• Thermosensitive layer

minimum value (

bg14.png

4

Wait 5-10 minutes for the alcohol to completely evaporate, then close the printer blade.

2.2.3 Label paper parameters

The steps to clean the printing rubber roller are as follows:

Turn off the printer, slide the upper cover stopper, and open the printer upper cover assembly;

mm)

bg7.png

Printing is not clear;

maximum(

mm)

0.05

Paper feeding noise is loud.

minimum value (

Note: When cleaning the print head or paper feeding rubber roller, do not use hard objects (such as tweezers, etc.) to scratch the print head and rubber roller; to increase the

service life of the print head, print

code name

When any of the following conditions occurs in the print head, the printing rubber roller should be cleaned:

For self-adhesive printing paper, regular printing of self-adhesive paper will leave glue residue on the backing. It is recommended to clean the print head and rubber roller every

month. If the environment is harsh, increase the cleaning appropriately.

meaning

Xiamen Dapu Electronic Technology Co., Ltd.

Rotate the printing roller, and at the same time use an alcohol cotton ball (which should be wrung out) to wipe away dust and stains on the surface of the printing roller;

bg15.png

79

d

label width

110

Label height

5

3

40

80

2

bg8.png

a paper line width

40

Xiamen Dapu Electronic Technology Co., Ltd.

0.1

40e label gap

c label width

0.05

3

b

Print normally

bg16.png

4\. Load paper into the printer

Xiamen Dapu Electronic Technology Co., Ltd.

6\. Printer interface definition

Printer serial port Host computer device serial port

6.1 The 2pin interface input power supply is 12V/24V, and the current is above 2.5A.

6.3 When using the USB port to communicate with the computer, the printer's USB port is a virtual serial port. You can use the serial port debugging assistant

to send data to the printer.

The paper loading method must be consistent with the figure below to print the content correctly. Otherwise, the content will not be printed and only blank paper

will be printed.

Xiamen Dapu Electronic Technology Co., Ltd.

TX ------------------------------ RX

DTR

, Printing device installation steps

7

Empty (no answer)

6

GND ------------------------------ GND

bga.png

5\. Printing equipment solves paper jam problems

RX ------------------------------ TX

bg9.png

6.2 There are two types of printer serial ports: TTL and 232. The default baud rate is 115200. The following is the serial port wiring method.

bg17.png

Blank paper.

8.1

Refer to the driver installation manual.

Xiamen Dapu Electronic Technology Co., Ltd.

8

31 99

hexadecimal:

7\. Print the self-test page

7.3 The indicator light is always green, which is normal. When the paper is out of paper, the green light will flash three times and then stop.

Label calibration

Instruction code

data. If the printer serial port cannot be recognized on the computer. The printer driver is not installed automatically. You need to install the driver manually. Please

bgb.png

Decimal:

7.2 Switch between labels and receipts by sending instructions to the printer.

Tag Calibration Instructions

Send data to set receipt mode: 1F 2D 4D 01 02

Send hexadecimal data to set label mode: 1F 2D 4D 01 01

Command name

7.1 Press and hold the button for more than 3 seconds and a test page will automatically print out. There are relevant printer parameters in the test page. Press

the button and it will go out for a while

8 Detailed explanation of label instructions

bg18.png

Parameter range

Function description

8.2

tag start command

tag start command

Height\_L Height\_H

Rotate

Label paper calibration positioning. Locate the gap in the paper. It is recommended to use 3mm for paper gap. Replacement is not

Indicates the start of a label side and sets the label's size, reference point coordinates, and page rotation.

Usage example

1A 5B 01 x\_L x\_H

y\_L y\_H

1F 63

1F 63

Width\_L width\_H

default value

Instruction code

Input parameters:

If the gap cannot be found after one calibration, you can calibrate again. Calibration function is only available in label mode

Precautions

hexadecimal:

Function description

Label paper of the same size needs to be calibrated.

Command name

bg19.png

The reference origin of the label surface is relative to the upper left corner of the current position of the label paper.

x+Width

.

y

The value range is:

.

Rotate

x

Rotate

Width

Heigth

The value range is:

x

Label page width,

\[1, 1200\]

The reference origin of the label surface is relative to the upper left corner of the current position of the label paper.

Height

The value range is:

axis offset.

y

Label page height,

Label surface rotation angle,

\{0,1,2,3}

axis offset.

\[1,576 /384\]

bg1a.png

Rotate

90

When, the page

Xiamen Dapu Electronic Technology Co., Ltd.

°Print.

combined, representing the low-order byte and high-order byte of the parameter in turn

bit bytes. like

for

expressed in turn

1

\_L

and

. when

When, the page rotates

\_H

Does not rotate. when

9

2

for

Rotate

Double-byte parameters: specific characters and

x\_L x\_H ,

0

bgc.png

bg1b.png

X

1

384

.

point

1A 4F 00

8.3 Tag end command

The low-order byte and high-order byte.

tag end command

0x01=256

Usage example

1A 5B 01 00 00 00 00 80 01 40 01 00

Byte parameters

.

1A 5D 00

So low

Parameter range

Instruction code

high byte

x\_L=0x80=128,x\_H

Precautions

Command name

For example: the width is

\= 0.125mm

bg1c.png

Function description

1A 5B 01 00 00 00 00 80 01 40 01 00

none.

8.4 Label printing instructions

1A 5D 00

b:

1A 4F 01 PrintNum

Identifies the end of a tag side data.

Print the contents on the label onto label paper.

Precautions

Instruction code

Hexadecimal: a:

Hexadecimal: 1A 5D 00

Usage example

1A 4F 00

return value:

Command name

Parameter range

none.

Label printing instructions

Function description

1A 4F 00

Input parameters:

bg1d.png

bgd.png

The contents of the label side will be printed

Input parameters:

bÿ

Input parameters:

Usage example

1A 5B 01 00 00 00 00 80 01 40 01 00

none

1A 4F 00

1

return value:

none.

aÿ

all over.

Parameter range

Xiamen Dapu Electronic Technology Co., Ltd.

PrintNum

Print a blank page

Note: This command will only print the page content

10

Second-rate.

1A 5D 00

Return value: None

PrintNum

bg1e.png

y\_L y\_H

8.5 Label text printing

1A 54 01 x\_L x\_H

1A 5D 00

String00

a.

Input parameters:

1A 4F 00 02

Define text starting position

Hexadecimal: a.

FontType\_L FontType\_H

String00

1A 5B 01 00 00 00 00 80 01 40 01 00

1A 54 00 x\_L x\_H

Function description

Command name

y\_L y\_H

x

Instruction code

label text command

18 00

x

Coordinates, value range:

Print two blank pages

b:

bg1f.png

;

0x00

y

none

Terminated text string data stream.

Input parameters:

bge.png

y

11

String00

When the sum of is greater than the page width

, the text is truncated for printing.

\[0, Page\_Width-1\]

To be printed, use

b.

Coordinates, value range:

Note: When the text width and text starting coordinates

;

\[0, Page\_Height-1\]

x

Xiamen Dapu Electronic Technology Co., Ltd.

return value:

Define text starting position

bg20.png

Define text starting position

\[0, Page\_Height-1\]

To be printed, use

\[0, Page\_Width-1\]

;

x

When the sum of is greater than the page width

x

y

Return value: None.

Remark

X

Coordinates, value range:

:When the text width is equal to the text starting coordinate

;

0x00

Define text starting position

y

Terminated text string data stream.

, the text is truncated for printing.

Coordinates, value range:

FontType\_L

bg21.png

Precautions

1A 54 01

18 00 01 33

1B 40 1a 5B 01 00 00 00 00 80 01 40 01 00

00 00

1A 54 01 21 00 00 00 18 00 10 00 53 54 43 50 31 30 30 30 30 31 33 31 00 Font rotated 90°

1A 54 01 41 00 00 00 18 00 01 00 53 54 43 50 32 30 30 30 30 31 33 32 00 bold font

Usage example

1A 54 01 41 00 39 00 18 00 03 00 53 54 43 50 32 30 30 30 30 31 33 34 00 Underlined and bolded

B:

1a 4f 00

C:

Parameter range

1B 40 1a 5B 01 00 00 00 00 80 01 40 01 00

1A 5B 01 00 00 00 00 80 01 fa 00 00

1A 54 00 00 00 00 00 B0 AE CE D2 D6 D0 BB AA 00

C4E3BAC3 00

1A 54 01 41 00 56 00 18 00 04 00 53 54 43 50 33 30 30 30 30 31 33 35 00 reverse white printing

1a 4f 00

1a 5d 00

1a 5d 00

1A 54 01 41 00 1d 00 18 00 02 00 53 54 43 50 33 30 30 30 30 31 33 33 00 Underline

1A 5D 00 1A 4F 00

A:

00 00

bg22.png

1A 5B 01 00 00 00 00 80 01 fa 00 00

1A 54 01 41 00 99 00 18 00 00 44 53 54 43 50 32 30 30 30 30 31 33 36 00 The font is enlarged four times

1A 54 01 41 00 1D 00 18 00 00 22 53 54 43 50 32 30 30 30 30 31 33 36 00 Double the font size

8.6

1A 5D 00 1A 4F 00

1A 5C 00 StartX\_L StartrX\_H

StartY\_L StartrY\_H

1A 54 01 21 00 00 00 18 00 00 11 53 54 43 50 31 30 30 30 30 31 33 36 00 Font normal size default

EndY\_L EndY\_L

Xiamen Dapu Electronic Technology Co., Ltd.

Line segment drawing instructions

Instruction code

D:

12

Hexadecimal: a.

times

Line segment drawing instructions

b.

bgf.png

1A 54 01 41 00 56 00 18 00 00 33 53 54 43 50 33 30 30 30 30 31 33 36 00 The font is enlarged three times

Command name

EndX\_L EndX\_H

recognize

Font size range (11, 22, 33, 44, 55, 66)

bg23.png

StartY\_L StartY\_H

Width\_L Width\_H

a.

starting point of straight line segment

Input parameters:

starting point of straight line segment

y

EndX\_L EndX\_H

\[0,

Page

\[0, Page\_Width-1\]

.

1A 5C 01 StartX\_L StartX\_H

Page draws a straight line segment between two specified points.

StartY

Color

x

Page\_Height-1\]

exist

Function description

Coordinate value, value range:

Coordinate value, value range:

EndY\_L EndY\_H

StartX

bg24.png

EndX

Coordinate value, value range:

return value:

Coordinate value, value range:

\[0,Page\_Height-1\]

x

Coordinate value, value range:

end point of straight line segment

.

end point of straight line segment

Input parameters:

StartX

.

y

starting point of straight line segment

\[0, Page\_Width-1\]

none.

StartY

EndY

.

b.

\[0, Page\_Width-1\]

x

.

bg25.png

y

Page\_Height-1\]

\[0, Page\_Width-1\]

end point of straight line segment

.

bg10.png

Xiamen Dapu Electronic Technology Co., Ltd.

Coordinate value, value range:

\[1

x

\[0,Page\_Height-1\]

.

starting point of straight line segment

Coordinate value, value range:

Width

.

y

end point of straight line segment

EndX

Coordinate value, value range:

13 Line width of straight line segment, value range:

\[0,

EndY

bg26.png

Line segment color, value range:

0

Page\_Height-1\]

, the line segment is black. when

Color

1B 40 1a 5B 01 00 00 00 00 80 01 40 01 00

1A 5C 01 00 00 00 00 00 01 00 00 30 00 01

.

8.7 Rectangular frame drawing instructions

for

none.

Parameter range

,

1

Usage example

\{0, 1}

, the line segment is white.

Command name

Color

. when

Output parameters:

1a 4f 00

Color

for

bg27.png

Right\_L Right\_H

Top\_L Top\_H

Color

Instruction code

Bottom\_L Bottom\_H

The x coordinate value of the upper left corner of the rectangular box, value range: \[0, Page\_Width-1\].

Top

Hexadecimal: a.

Right

1A 26 01 Left\_L Left\_H

a.

Input parameters:

Rectangular frame drawing instructions

Top\_L Top\_H

Left

Right\_L Right\_H

Function description

The x-coordinate value of the lower right corner of the rectangular box. Value range: \[0, Page\_Width-1\].

b.

Bottom\_L Bottom\_H

Draws a rectangular box of the specified size at the specified location on the Page.

The y coordinate value of

the upper left corner of the rectangular box. Value range: \[0, Page\_Height-1\].

Bottom

1A 26 00 Left\_L Left\_H

Width\_L Width\_H

bg28.png

return value:

Top

Input parameters:

coordinate value. Ranges:

Rectangular box upper left corner

coordinate value. Ranges:

\[0, Page\_Width-1\]

none.

Bottom

Xiamen Dapu Electronic Technology Co., Ltd.

Right

Lower right corner of rectangle

The y coordinate value of

the lower right corner of the rectangular box. Value range: \[0, Page\_Height-1\].

14

x

Left

\[0, Page\_Height-1\]

Lower right corner of rectangle

bg11.png

The x coordinate value of the upper left corner of the rectangular box, value range: \[0, Page\_Width-1\].

.

.

b.

y

bg29.png

Width

coordinate value. Ranges:

When, draw a black rectangle with width,

When , draw a white rectangular frame.

Color=

1a 4f 00

8.8 One-dimensional barcode instructions

\[0, Page\_Height-1\]

\{0,

1}. when

Usage example

1a 5B 01 00 00 00 00 80 01 40 01 00

y

Color=1

1a 26 01 10 00 10 00 00 01 00 01 10 00 01

The line width of the rectangular frame.

Return parameters: none

Rectangular border color, straight range

Color

Parameter range

.

0

bg2a.png

1D barcode instructions

String00

1A 30 00 x\_L x\_H

Page

Function description

Coordinate value, value range:

\[0, Page\_Width-1\]

Instruction code

y

UnitWidth

x

upper left corner of barcode

Command name

Rotate

x

y\_L y\_H

Draw a one-dimensional barcode at the specified position on the page.

upper left corner of barcode

BarcodeHeight

BarcodeType

Input parameters:

.

y

hexadecimal:

exist

bg2b.png

\[0, Page\_Height-1\]

barcode value range

Identifies the barcode type, value range:

11

Remark

2

EAN13

.

48-57

type

UPC-E

6

Coordinate value, value range:

length

48-57

\[0,29\]

48-57

3

value

. Each value is defined as follows:

1

12

BarcodeType

0UPC-A

bg2c.png

5

CODE39

48-57

7

I25

7

CODE93

48-57

0-127

15

R

1-48-57,65-68,36,4

EAN8

6,37,43,45,46,47

3,45,46,47,58

1-48-57,65-90,32,3

6

8

Xiamen Dapu Electronic Technology Co., Ltd.

bg12.png

CODABA

1-255

4

1-even number

bg2d.png

2-255

Mode

EAN128

CODE11

\-> !096 - !105

Number-\[(sum of odd-digit numbers <from

Left to right)+(even number of digits

0-127

1439C

128M

25C

25C Check use mod 10-> odd

CODE128

Coding mode can be switched according to data

The number is first padded with 0 in front, which is a multiple of 10

10

Automatically switch encoding modes

The check code of code 39 must match

11

MSI

13

and)\*3\]

9

12

bg2e.png

As shown in the table, the relative value will be found

Show

Also includes

Yuan is the check code character.

39C

Interval between additional code and main code

7-12

After adding up and dividing by 43, we get

1011

special words

Pay attention to aspect ratio processing

16

"Check code relative value comparison table",

Symbols are represented by two representable words.

EAN13+2

15

Full

The interval is

Full ASCII 39 Code,

39

ASCII,

Unit, starting with

01

The remainder then finds the corresponding code word

,

bg2f.png

(\_0\*10+\_1) Mod 4->

EAN13+5

"abaab", "aabab

Same as EAN13+2

18

See specifications for details, it is a high and low bar

code, not wide and narrow barcode

0--AA 1--AB 2--BA 3--BB

UPCA+2

,

Same as EAN13+5

20

,

mod 10 ->"bbaaa", "babaa",

"baaba", "baaab", "abbaa", "aabba",

"aaabb", "ababa",

POST

twenty two

The additional code part is the same as above

19

Additional code see

model

((\_0+\_2+\_4)\*3+(\_1+\_3)\*9)

EAN8+5

twenty one

EAN

17

EAN8+2

bg30.png

Additional code see

26

Additional code see

Check code once

MSIC

28

ITF14

EAN

Variant, first digit prepended

25

16

27

UPCA+5

CPOST

PLESSEY

EAN

bg13.png

0

See EAN for additional code

24UPCE+5

Xiamen Dapu Electronic Technology Co., Ltd.

25C

Recalculate the check code as data

23UPCE+2

bg31.png

EAN14

bar width

The latter number, but still filled to the end

Multilevel barcode unit width

Degree (mm)

0.25

2

end

0.25

Define the barcode width. Value range: \[1, 4\]. Each value is defined as follows:

1

0.125

, the minimum amount needs to be deducted when calculating the check code

Width value

0.125

BarcodeHeight:

Binary barcode wide line

0.50

UnitWidth:

Define the barcode height.

bar width

0.25

3

29

Binary barcode narrow lines

bg32.png

0.50

1

0.375

definition

0

180

° draw.

0.75

String00:

Indicates the barcode rotation angle. Value range: \[0, 3\]. Each value is defined as follows:

° draw.

2

0.375

Rotate value

barcode rotation

0.50

barcode rotation

A stream of text character data terminated by 0x00.

Rotate:

1.0

90

3 barcodes are drawn rotated 270°.

4

Barcodes are drawn without rotation.

bg33.png

Usage example

0c55

none.

1a 30 00

20 00

bg14.png

Xiamen Dapu Electronic Technology Co., Ltd.

Parameter range

8.9 QRCode QR code command

1b 40

31 30 31 30 30 00

1a 5d 00

return value:

1a 5B 01 00 00 00 00 80 01 00 01 00

1a 4f 00

(

02

Command name

inch label paper)

2

00

17

Precautions

40 00

bg34.png

Barcode instructions

String00

version

version

Function description

1

L

Instruction code

7%, low error correction, lots of data.

UnitWidth

Specify the error correction level. Value range: \[1, 4\]. Each value is defined as follows:

ECC

QRCode

Rotate

error correction level

ECC

Specifies the character version. Value range: \[0,20\]. When version is 0, the printer prints the

2

y\_L y\_H

x\_L x\_H

Spend

:

Hexadecimal: 1A 31 00

Input parameters:

bg35.png

3Q

:

The y coordinate value of the

upper left corner of the QRCode code, the value range: \[0, Page\_Height-1\].

same.

UnitWidth

return value:

none.

15%

Precautions

The x coordinate value of the upper left corner of the QRCode code, the value range: \[0, Page\_Width-1\].

Same as Rotate.

String00

M

y

QRCode text character data stream terminated with 0x00.

: Optimization and error correction

Rotate

H: 30%, highest error correction, less data.

4

QRCode code rotation angle, value range: \[0, 3\]. Definition of each value and command input parameters

Parameter range

, medium error correction

QRCode code block, value range: \[1, 8\]. Definition of each value and command input parameter UniWidth

bg36.png

Bitmap instructions

1a 4f 00

aÿ1A 21 00

1B 40 1a 5B 01 00 00 00 00 80 01 40 01 00

Instruction code

b:

1A 21 01

1A 31 00 03 03 60 00 20 00 04 00 D6 D0 B9 FA CD F2 CB EA 00

y\_L y\_H

8.10 Picture printing

Width\_L Width\_H

Height\_L Height\_L

Usage example

Command name

Data

bg15.png

x\_L x\_H

Width\_L Width\_H

18

Xiamen Dapu Electronic Technology Co., Ltd.

y\_L y\_H

x\_L x\_H

Height\_L Height\_L

1a 5d 00

hexadecimal:

bg37.png

Data

Width

a:

\=26 00

Bitmap pixel width = picture pixel width divided by 8.

b:

Input parameters:

Function description

The x coordinate value of the upper left corner of the bitmap, value range: \[0, Page\_Width\].

y

Data

Bitmap bitmap data.

ShowType

The y coordinate

value of the upper left corner of the bitmap, value range: \[0, Page\_Height\].

Return value: None.

Input parameters:

Height

y

The x coordinate value of the upper left corner of the bitmap, value range: \[0, Page\_Width\].

x

The pixel height of the bitmap.

x

Draws a bitmap at the location specified by the label.

For example: the pixel width of the picture is 300, 300/8=37.5, if there are decimals, an integer + 1 is required, the width of the picture is 38

bg38.png

Xiamen Dapu Electronic Technology Co., Ltd.

Bitmap bitmap data.

Width

01

The picture is printed in reverse white

1a 21 01 40 00 40 00 18 00 18 00 07 22

0820800E38E00C30C80C34FC0DFF980E31102D32242DFDFE2CB58C6CB58C6CB

Bitmap pixel width = picture pixel width divided by 8.

C0C31060C3204082400

ShowType 00

Precautions

Usage example

The y coordinate

value of the upper left corner of the bitmap, value range: \[0, Page\_Height\].

Pictures print normally

1a 5B 01 00 00 00 00 80 01 40 01 00

19

Return value: None.

1A 5D 00

The pixel height of the bitmap.

Height

Parameter range

5AC4CB5AC0CFDAC0C31AC0C71AC0C71AC0CB9AC0CB5280D34400E30580C308

1a 4f 00

bg16.png

Data

bg39.png

27 64

Initialize printer

Function description

9.1

hexadecimal:

default value

none

Initialize printer

All models

ESC @

Restore default values for each parameter

Parameter range

9 Detailed explanation of small ticket instructions

Decimal:

none

Instruction code

Initialize the printer as follows:

:

ASCII

Clear print cache

Supported models

Command name

1B 40

bg3a.png

none

:

18 94

9.2

DC2T

Xiamen Dapu Electronic Technology Co., Ltd.

20

Usage example

Parameter range

Instruction code

Function description

The printer prints a self-test page, which contains the printer's program version, communication interface type, and code.

Precautions

ASCII

bg17.png

Print self-test page

hexadecimal:

none

Print self-test page

Command name

12 54

page and some other data

none

Decimal:

bg3b.png

Precautions

:

none

Set character printing method

Instruction code

Function description

Set the character printing method (font style, highlight, inversion, bold, double height, double width, and underline),

Supported models

n

9.3 Set character printing mode

27 33 n

hexadecimal:

default value

Command name

1B 21n

none

ESC! n

1B 40 12 54

Usage example

Decimal:

parameter

All models

ASCII

bg3c.png

The definition is as follows:

0

3Bold Unset

5

4

Parameter range

none

bit function value

\=

0n

2

undefined

7

bit

undefined

Underline unset

Normal font size small font

Double width cancel setting

undefined

1

6

default value

0 1

Double height cancel setting

bg3d.png

All models

1B 40 1B 21 10 30 31 32 0D 0A

The setting of this command becomes invalid after ESC @, printer reset, or power outage.

1B 40 1B 21 80 30 31 32 0D 0A

1B 40 1B 21 20 30 31 32 0D 0A

ASCII

:

Precautions

Decimal:

1B 40 1B 21 04 30 31 32 0D 0A

Command name

Set character size

Supported models

1B 40 1B 21 08 30 31 32 0D 0A

Instruction code

Usage example

9.4

29 33n

1B 40 1B 21 02 30 31 32 0D 0A

1B 40 1B 21 01 30 31 32 0D 0A

Set character size

GS! n

bg18.png

1B 40 1B 21 40 30 31 32 0D 0A

This command is valid for both Chinese fonts and foreign fonts

bg3e.png

twenty one

Function description

none

Supported models

default value

1b 40 1d 21 00

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 0d 0a

hexadecimal:

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 0d 0a

1d 21 01 font double height

This command is valid for both Chinese and foreign fonts except HRI characters.

The setting of this command becomes invalid after ESC @, printer reset, or power outage.

Xiamen Dapu Electronic Technology Co., Ltd.

Parameter range

Usage example

1d 21 00 normal font (default)

All models

1b 40 1d 21 10

1d 21 10 font double width

1d 21 11 times height times width

Precautions

1b 40 1d 21 11

1d 21n

\= 0

n

bg3f.png

1b 40 1d 21 01

ESC an

Set print alignment

hexadecimal:

Decimal:

n

model

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 0d 0a

On the left

ASCII

Align all data in a row,

n

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 0d 0a

:

The meaning of the value is as follows:

Command name

1B 61 n

1,49

Instruction code

Set printing alignment (left, center, right)

Function description

0,48

27 97 n

9.5

bg40.png

2,50

0 ÿ n ÿ 2 or 48 ÿ n ÿ 50

when

Usage example

ESC @

BF BF D3 D2 B6 D4 C6 EB 0D 0A

9.6

On the right

Command name

All models

1B 40 1B 61 01

BE D3 D6 D0 B6 D4 C6 EB 0D 0A

center

Precautions

1B 40 1B 61 02

default value

1B 40 1B 61 00

Print line segments in horizontal positions (curve print command)

Supported models

\= 0

n

C4 AC C8 CF D7 F3 B6 D4 C6 EB 0D 0A

Print line segments in horizontal positions (curve print command)

Parameter range

, the setting of this command becomes invalid after the printer is reset or powered off.

bg41.png

Xiamen Dapu Electronic Technology Co., Ltd.

1D 27 n x1sL x1eH x1eL x1eH ...xnsL xnsH xneL xneH

ASCII

Function description

hexadecimal:

For horizontal line segments, use this command continuously to print out the required curve.

xksL :K

twenty two

xksH :K

n x1sL x1eH x1eL x1eH ...xnsL xnsH xneL xneH

these point groups

become. Print

bg19.png

Decimal:

n

The low-order horizontal coordinate of the line end point;

:

Print the enlarged view as follows: Each horizontal curve segment can be regarded as consisting of a segment length of

The high-order horizontal coordinate of the starting point of the line;

GS

'

1

The low-order horizontal coordinate of the starting point of the line;

xkeL : K

Instruction code

29 39 n x1sL x1eH x1eL x1eH ...xnsL xnsH xneL xneH

bg42.png

The high-order horizontal coordinate of the line end point;

Char SendStr\[8\];

), maximum horizontal sitting

Short y1,y2,y1s,y2s;

Char SendStr2\[16\];

SendStr\[4\]=0; //Start point

SendStr\[5\]=104;

The coordinate starting position is usually the left side of the printing area. The minimum coordinate coordinate is (

PreSendData(SendStr,7);

xkeL+xkeH\*256

SendStr\[1\]=0x27;

SendStr\[2\]=1; // One line

xkeH :K

Row data may not be arranged in order within the specified range;

SendStr\[3\]=30

Standard value

//Print Y axis (a line)

bg1a.png

,

383

SendStr\[0\]=0x1D;

SendStr\[6\]=1; //End point

Xiamen Dapu Electronic Technology Co., Ltd.

Float i;

0,0

bg43.png

//Print curve

\{

SendStr\[2\]=3; //Three lines:X-axis, sin and cos function curve three lines:

If(i==1)\{y1s=y1;y2s=y2;}

y1=sin(i/180\*3.1416)\*(380-30)/2+180; //Calculate sin function coordinates

}

Else

SendStr\[0\]=0x1D;

PreSendData(&y1,2); //sin function at the starting point of the line

SendStr\[5\]=180; SendStr\[6\]=0;

\{

PreSendData(&y1s,2); //sin function is at the starting point of the line

twenty three

for(i=1;i<1200;i++)

PreSendData(&y1,2); //sin function at the end point of the line

X axis, sin and cos

PreSendData(SendStr,7);

PreSendData(&y1s,2); //sin function at the end point of the line

SendStr\[3\]=180; SendStr\[4\]=0; // X-axis position

function

If(y1s<y1)

\{

}

SendStr\[1\]=0x27;

y2=cos(i/180\*3.1416)\*(380-30)/2+180; //Calculate cos function coordinates

bg44.png

}

\{

y1s=y1; // When printing enters the next line, the abscissa of the starting point of the sin function curve

Parameter range

y2s=y2; //When printing enters the next line, the abscissa of the starting point of the cos function curve

Precautions

When printing a point, xkeL=xksL

PreSendData(&y2s,2); //cos function at the starting point of the line

Usage example

PreSendData(&y2s,2); //cos function at the end point of the line

none

Supported models

If(y2s<y2)

}

portable printer

Else

0ÿnÿ8

1d 27 01 00 00 00 00

PreSendData(&y2,2); //cos function at the starting point of the line

\{

default value

xkeH=xksH ,

1d 27 01 01 00 0f 00 1d 27 01 10 00 1f 00

PreSendData(&y2,2); //cos function at the end point of the line

}

bg45.png

1d 27 01 3b 00 44 00 1d 27 01 45 00 4c 00

1d 27 01 92 00 97 00 1d 27 01 98 00 9d 00

Xiamen Dapu Electronic Technology Co., Ltd.

1d 27 01 b5 00 b9 00 1d 27 01 ba 00 bf 00

1d 27 01 9e 00 a3 00 1d 27 01 a4 00 a9 00

1d 27 01 ea 00 ec 00 1d 27 01 ed 00 ef 00

1d 27 01 f0 00 f1 00 1d 27 01 f2 00 f3 00

1d 27 01 4d 00 54 00 1d 27 01 55 00 5c 00

1d 27 01 f8 00 f8 00 1d 27 01 f9 00 fa 00

1d 27 01 78 00 7d 00 1d 27 01 7e 00 84 00

1d 27 01 d5 00 d8 00 1d 27 01 d9 00 dc 00

1d 27 01 dd 00 df 00 1d 27 01 e0 00 e3 00

1d 27 01 20 00 2c 00 1d 27 01 2d 00 3a 00

1d 27 01 85 00 8a 00 1d 27 01 8b 00 91 00

1d 27 01 e4 00 e6 00 1d 27 01 e7 00 e9 00

1d 27 01 00 01 00 01 1d 27 01 01 01 01 01

1d 27 01 02 01 02 01 1d 27 01 03 01 03 01

twenty four

1d 27 01 c0 00 c4 00 1d 27 01 c5 00 c9 00

1d 27 01 fb 00 fb 00 1d 27 01 fc 00 fd 00

1d 27 01 6b 00 71 00 1d 27 01 72 00 77 00

1d 27 01 5d 00 63 00 1d 27 01 64 00 6a 00

1d 27 01 ca 00 cf 00 1d 27 01 d0 00 d4 00

1d 27 01 f4 00 f5 00 1d 27 01 f6 00 f7 00

1d 27 01 fe 00 fe 00 1d 27 01 ff 00 ff 00

bg1b.png

1d 27 01 aa 00 af 00 1d 27 01 b0 00 b4 00

bg46.png

1d 27 01 07 01 07 01 1d 27 01 06 01 06 01

1d 27 01 06 01 06 01 1d 27 01 06 01 06 01

1d 27 01 f9 00 fa 00 1d 27 01 f8 00 f8 00

1d 27 01 ed 00 ef 00 1d 27 01 ea 00 ec 00

1d 27 01 07 01 07 01 1d 27 01 07 01 07 01

1d 27 01 f2 00 f3 00 1d 27 01 f0 00 f1 00

1d 27 01 98 00 9d 00 1d 27 01 92 00 97 00

1d 27 01 a4 00 a9 00 1d 27 01 9e 00 a3 00

1d 27 01 7e 00 84 00 1d 27 01 78 00 7d 00

1d 27 01 04 01 04 01 1d 27 01 04 01 04 01

1d 27 01 03 01 03 01 1d 27 01 02 01 02 01

1d 27 01 e0 00 e3 00 1d 27 01 dd 00 df 00

1d 27 01 e7 00 e9 00 1d 27 01 e4 00 e6 00

1d 27 01 06 01 06 01 1d 27 01 05 01 05 01

1d 27 01 8b 00 91 00 1d 27 01 85 00 8a 00

1d 27 01 64 00 6a 00 1d 27 01 5d 00 63 00

1d 27 01 fe 00 fe 00 1d 27 01 fc 00 fd 00

1d 27 01 04 01 04 01 1d 27 01 05 01 05 01

1d 27 01 c5 00 c9 00 1d 27 01 c0 00 c4 00

1d 27 01 d9 00 dc 00 1d 27 01 d5 00 d8 00

1d 27 01 00 01 00 01 1d 27 01 ff 00 ff 00

1d 27 01 d0 00 d4 00 1d 27 01 ca 00 cf 00

1d 27 01 07 01 07 01 1d 27 01 07 01 07 01

1d 27 01 72 00 77 00 1d 27 01 6b 00 71 00

1d 27 01 f6 00 f7 00 1d 27 01 f4 00 f5 00

1d 27 01 b0 00 b4 00 1d 27 01 aa 00 af 00

1d 27 01 ba 00 bf 00 1d 27 01 b5 00 b9 00

bg47.png

1d 27 01 45 00 4c 00 1d 27 01 3b 00 44 00

1d 27 01 6b 00 71 00 1d 27 01 72 00 77 00

Xiamen Dapu Electronic Technology Co., Ltd.

1d 27 01 3b 00 44 00 1d 27 01 45 00 4c 00

1d 27 01 55 00 5c 00 1d 27 01 4d 00 5400

1d 27 01 5d 00 63 00 1d 27 01 64 00 6a 00

1d 27 01 d5 00 d8 00 1d 27 01 d9 00 dc 00

1d 27 01 ca 00 cf 00 1d 27 01 d0 00 d4 00

1d 27 01 e4 00 e6 00 1d 27 01 e7 00 e9 00

1d 27 01 10 00 1f 00 1d 27 01 01 00 0f 00

1d 27 01 00 00 00 00 1d 27 01 00 00 00 00

1d 27 01 85 00 8a 00 1d 27 01 8b 00 91 00

1d 27 01 78 00 7d 00 1d 27 01 7e 00 84 00

1d 27 01 2d 00 3a 00 1d 27 01 20 00 2c 00

1d 27 01 dd 00 df 00 1d 27 01 e0 00 e3 00

1d 27 01 f0 00 f1 00 1d 27 01 f2 00 f3 00

1d 27 01 20 00 2c 00 1d 27 01 2d 00 3a 00

bg1c.png

1d 27 01 aa 00 af 00 1d 27 01 b0 00 b4 00

1d 27 01 92 00 97 00 1d 27 01 98 00 9d 00

1d 27 01 01 00 0f 00 1d 27 01 10 00 1f 00

1d 27 01 9e 00 a3 00 1d 27 01 a4 00 a9 00

25

1d 27 01 ea 00 ec 00 1d 27 01 ed 00 ef 00

1d 27 01 4d 00 54 00 1d 27 01 55 00 5c 00

1d 27 01 c0 00 c4 00 1d 27 01 c5 00 c9 00

1d 27 01 b5 00 b9 00 1d 27 01 ba 00 bf 00

bg48.png

1d 27 01 00 01 00 01 1d 27 01 01 01 01 01

1d 27 01 03 01 03 01 1d 27 01 02 01 02 01

1d 27 01 f8 00 f8 00 1d 27 01 f9 00 fa 00

1d 27 01 07 01 07 01 1d 27 01 06 01 06 01

1d 27 01 04 01 04 01 1d 27 01 04 01 04 01

1d 27 01 fe 00 fe 00 1d 27 01 ff 00 ff 00

1d 27 01 d9 00 dc 00 1d 27 01 d5 00 d8 00

1d 27 01 e0 00 e3 00 1d 27 01 dd 00 df 00

bg1d.png

1d 27 01 04 01 04 01 1d 27 01 05 01 05 01

1d 27 01 06 01 06 01 1d 27 01 06 01 06 01

1d 27 01 fe 00 fe 00 1d 27 01 fc 00 fd 00

1d 27 01 00 01 00 01 1d 27 01 ff 00 ff 00

1d 27 01 02 01 02 01 1d 27 01 03 01 03 01

1d 27 01 d0 00 d4 00 1d 27 01 ca 00 cf 00

26

1d 27 01 07 01 07 01 1d 27 01 07 01 07 01

1d 27 01 f4 00 f5 00 1d 27 01 f6 00 f7 00

1d 27 01 f2 00 f3 00 1d 27 01 f0 00 f1 00

1d 27 01 f9 00 fa 00 1d 27 01 f8 00 f8 00

1d 27 01 07 01 07 01 1d 27 01 07 01 07 01

1d 27 01 f6 00 f7 00 1d 27 01 f4 00 f5 00

1d 27 01 fb 00 fb 00 1d 27 01 fc 00 fd 00

Xiamen Dapu Electronic Technology Co., Ltd.

1d 27 01 06 01 06 01 1d 27 01 05 01 05 01

1d 27 01 e7 00 e9 00 1d 27 01 e4 00 e6 00

1d 27 01 ed 00 ef 00 1d 27 01 ea 00 ec 00

bg49.png

1d 27 01 98 00 9d 00 1d 27 01 92 00 97 00

1d 27 01 00 00 00 00

1d 27 01 ba 00 bf 00 1d 27 01 b5 00 b9 00

1d 27 01 45 00 4c 00 1d 27 01 3b 00 44 00

1d 27 01 10 00 1f 00 1d 27 01 01 00 0f 00

1d 27 01 a4 00 a9 00 1d 27 01 9e 00 a3 00

Decimal:

HT

hexadecimal:

1d 27 01 7e 00 84 00 1d 27 01 78 00 7d 00

1d 27 01 72 00 77 00 1d 27 01 6b 00 71 00

Set horizontal tab position

9.7

1d 27 01 8b 00 91 00 1d 27 01 85 00 8a 00

9

1d 27 01 55 00 5c 00 1d 27 01 4d 00 5400

1d 27 01 c5 00 c9 00 1d 27 01 c0 00 c4 00

Instruction code

Command name

1d 27 01 64 00 6a 00 1d 27 01 5d 00 63 00

horizontal tabulation

1d 27 01 b0 00 b4 00 1d 27 01 aa 00 af 00

09

1d 27 01 2d 00 3a 00 1d 27 01 20 00 2c 00

:

ASCII

bg4a.png

Move the printing position to the next tabulation position

ESC D

default value

LF

none

If the tab position is not set (default is no horizontal tab position), this command will be treated as

Hexadecimal: 1B 44 \[d\]k 00

Decimal: 27 68 \[d\]k 0

Supported models

All models

If the tabulation position exceeds the printing area, the coordinates will be moved to the starting position of the next line (this line is considered to be full of data,

instruction

none

The tabulation position is given by

Function description

Command name

print and

Precautions

newline)

Parameter range

set up

ASCII: ESC D\[d\]k NUL

Instruction code

bg4b.png

Set the horizontal tab position. The meaning of the parameters is as follows:

XX58: 1 ÿ d ÿ 46 (d1 < d2 < …… dk, 1 ÿ k ÿ 16)

All models

bg1e.png

Parameter range

The tabulation position is as follows:

transmission

For illustration purposes only, no need to transmit

default value

\[d\]k = 0

27

Xiamen Dapu Electronic Technology Co., Ltd.

XX80: 1 ÿ d ÿ 70 (d1 < d2 < ...... dk, 1 ÿ k ÿ 16)

Supported models

Function description

Settings for tab positions

Most supported

(default no horizontal tab position)

16

d1 ... dk: horizontal tab position, in 8-point units, NULL as terminator

Precautions

k

Using this command will cancel the previous tab position settings.

bg4c.png

meet

HT

like

when

When the left margin changes, the tab position changes at the same time.

when, it is deemed to be over

Instruction description:

31 2E 30 09 32 30 09 31 38 32 30 2E 30 30 0D 0A

less than or equal to

dk-1

, the setting of this command becomes invalid after the printer is reset or powered off.

ESC @

dk

1B 44 0B 12 19 00 ==0B

The tabulation position can be determined by

\[d\]k

BF 09 BD F0 B6 EE 09 0D 0A C5 A3 C8 E2 CB C9 D0 A1 B1 B4 0D 0A 09 31 2E 30

Usage example

, is regarded as the end, and the remaining data is treated as ordinary data.

1B 44 0B 12 19 00 0D 0A 20 20 20 C6 B7 20 C3 FB 09 B5 A5 BC DB 09 CA FD C1

NULL

switch

09 32 09 32 30 34 2E 30 30 0D 0A D7 CF CA ED D4 B2 D4 B2 CB D8 0D 0A 09 39

09 32 09 32 2E 30 30 0D 0A C1 F1 C1 AB B5 B0 CC A2 0D 0A 09 31 30 32 2E 30

bg4d.png

12

Second example

is the width of the third column,

19

19

third column

09 ==09

Is a space, the first column of text content "product name"

00

end of schism

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_|\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_|\_\_\_\_\_\_\_\_\_\_\_\_\_|\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

last row

The remaining width is the width of the last column starting with

0B

is the width of the first column

0D 0A

|\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

first row

such as the width of a line

Second column width,

12

20 20 20 C6 B7 20 C3 FB ==02

newline

bg4e.png

B5 A5 BC DB

Column symbol

The fourth column text content "Amount"

0D 0A

09

Column symbol

Second example

31 2E 30

09

The third example text content "quantity"

09

C5 A3 C8 E2 CB C9 D0 A1 B1 B4

newline

CA FD C1 BF

1.0

BD F0 B6 EE

As a column symbol,

newline

The first column of text content is "Beef floss and scallops"

Column symbol

0D 0A

The text content of the second column is "unit price"

09

Column symbol

09

bg4f.png

32

fourth column

bg1f.png

newline

2

0D 0A

09

102.0

32

28

09

First row "Durian Egg Tart"

C1 F1 C1 AB B5 B0 CC A2

Xiamen Dapu Electronic Technology Co., Ltd.

Column symbol

32 2E 30 30

Column symbol

Column symbol

0D 0A

Column symbol

09

third column

2.00

Second example

31 30 32 2E 30

bg50.png

The first column is "Purple Sweet Potato Round Vegetables"

32 30 34 2E 30 30

09

2

Column symbol

newline

20

third column

Column symbol

204.00

0D 0A

39 31 2E 30

Column symbol

fourth column

09

D7 CF CA ED D4 B2 D4 B2 CB D8

third column

09

Second example

newline

91.0

09

0D 0A

32 30

Column symbol

bg51.png

HRI

newline

ASCII:GS H n

fourth column

0D 0A

Instruction code

3, above and below the 51 barcode

2\. Below the 50 bar code

One-dimensional barcode printing instructions

9.8.1 Set the one-dimensional barcode readable character (HRI) printing position

Hexadecimal: 1D 48 n

Decimal: 29 72 n

9.8

Set barcode readable characters (

31 38 32 30 2E 30 30

n print position

Function description

Command name

Set the barcode readable character (HRI) printing position. The meaning of the n parameter is as follows:

1820.00

) print position

1, above the 49 barcode

0, 48 do not print

bg52.png

0 ÿ n ÿ 3 or 48 ÿ n ÿ 51

Usage example

Supported models

Xiamen Dapu Electronic Technology Co., Ltd.

bg20.png

\= 0

n

Function description

Hexadecimal: 1D 68 n

Precautions

when

9.8.2 Set the height of one-dimensional barcode

29

All models

, the setting of this command becomes invalid after the printer is reset or powered off.

Parameter range

Instruction code

Command name

ESC @

Set the height of one-dimensional barcode

default value

none

Decimal: 29 104 n

ASCII:GShn

bg53.png

\= 64

none

Parameter range

ESC @

default value

Usage example

Set the barcode unit to n points, and the meaning of parameter n is as follows:

Function description

Supported models

All models

Command name

9.8.3 Set the width of one-dimensional barcode

n

Parameter range

when

Set the height of the barcode to n points. The meaning of parameter n is as follows:

ASCII:GSwn

Set 1D barcode width

Precautions

Instruction code

1ÿnÿ255

, the setting of this command becomes invalid after the printer is reset or powered off.

Hexadecimal: 1D 77 n

Decimal: 29 119 n

bg54.png

The setting of this command becomes invalid after ESC @, printer reset, or power outage.

6

9.8.4 Print one-dimensional barcode

ÿ

ÿ

none

Decimal:

GS km\[d\]k NUL

n=2

Supported models

bg21.png

Command name

default value

29 107 m\[d\]k NUL

Precautions

1

Instruction code

Xiamen Dapu Electronic Technology Co., Ltd.

All models

30

n

Usage example

:

(A) ASCII

bg55.png

1D 6B m\[d\]k NUL

Print one-dimensional barcode, the meaning of each parameter is as follows:

GS kmn \[d\]k

is the encoded data length, only

n

:

NULL

data segment for

29 107 mn\[d\]k

hexadecimal:

way to use,

(B)

Decimal:

Function description

hexadecimal:

(B)

(A)

1D 6B mn \[d\]k

and

(B) ASCII

m is the encoding method

(A)

The difference between instructions is that

bg56.png

for barcode data

SP

(B)

A)

\[d\]k

barcode data (

fixed

It is the length of barcode data, used for illustration and does not need to be transmitted.

The relationship between each parameter is shown in the following table:

data

represents a space)

k

instruction

character ends, while

character set

length

(

k

Use to indicate the length of the data

m coding system

0UPC-A

Data(d)

bg57.png

UPC-E

2

0~9

\[when k =

1

d1 = 48 \]

d

ÿ

6ÿkÿ8,

k=11,12

(EAN13)

JAN13

fixed

ÿ

48ÿdÿ57

k=11,12

,

fixed

0~9

k = 12

48ÿdÿ57

7,8,11,12,

48

130~9

bg58.png

JAN8

d

k=7

4

fixed

57

,

0~9

8

0~9

variable

CODE39

,

A~Z

ÿ

573

k

1

48

ÿ

(EAN8)

ÿ

255

ÿ

bg59.png

,

ÿ

48

90,

ÿ

/

d

ÿ

d=32

ÿ

65

SP,

$,

%,

57,

\-, .,

d

bg5a.png

(Interleav

(even)

36,

37,

42,

43,

45,

46,

0~9

ed 2 of 5)

47

48ÿdÿ57

variable

CODABAR

5

6

2ÿkÿ255

ITF

,

bg5b.png

variable

(65ÿd1ÿ68,

97ÿdkÿ100)

$,+,-,.,/,:

09, AD, a~d

97ÿd1ÿ100,

length

65ÿdÿ68,

97ÿdÿ100,

m coding system

(Instruction B)

48ÿdÿ57,

46, 47, 58

(NW-7)

SP

system

d = 36, 43, 45,

barcode data (

1ÿk

65ÿdkÿ68,

data

represents a space)

bg5c.png

fixed

)

12

character set

d

,

6

fixed

Xiamen Dapu Electronic Technology Co., Ltd.

31

48

0~9

bg22.png

ÿ

UPC-A

n

ÿ

ÿ

65

d

data(

\= 11n

66UPC-E

57

bg5d.png

ÿ

ÿ

,

when

\= 11n

\[

fixed

(EAN13)

0~9

0~9

48

\=

n

12

n = 12, 13

d

n

d1 = 48 \]

7,8,11,12

ÿ

,

8,

57

JAN13

67

bg5e.png

fixed

09ÿAZ

68

CODE39

(EAN8)

1ÿnÿ255

ITF

70

ved 2 of

n

0~9

/

SP,$,%,+,-,.,

\=7,8

(Interlea

69

48ÿdÿ57

d = 32, 36, 37,

48ÿdÿ57,

48ÿdÿ57

65ÿdÿ90,

JAN8

variable

47

42, 43, 45, 46,

bg5f.png

1

d

71

ÿ

n

57

255

ÿ

,

(even)

0~9

R

CODABA

255

0~9

ÿ

variable

1

(NW-7)

48

variable

ÿ

ÿ

n

ÿ

bg60.png

,

65

,

ÿ

$,

d

ÿ

d

68,

\-, ., /, :48

57,

A~D

ÿ

a~d

ÿ

bg61.png

ÿ

(65

100

ÿ

d1

ÿ

d=36

,

65

68,

,

58

97

ÿ

43,

45,

46,

47,

d

ÿ

bg62.png

ÿ

ÿ

72

ÿ

97

ÿ

0

00H~7FH

ÿ

100

variable

CODE93

d1

ÿ

97

dk

n

1

,

ÿ

68,

dk

255

ÿ

bg63.png

ÿ

variable

variable

C1H~C4H(FNC)

73CODE128

00H~7FH

6

00H~7FH

0ÿdÿ127

d = 193,

0ÿdÿ127

2ÿnÿ255

128

d

(A) 0

194,195,196

74UCC/EAN

Parameter range

127

2ÿnÿ255

mÿ

ÿ

bg64.png

ÿ

When this command is executed, paper will be fed as needed. It will not be affected by the line spacing settings of ESC 2 and ESC 3 and will not affect the line spacing.

default value

After this command is executed, the printing position returns to the printing starting position.

This command is not affected by ESC! Character style settings affect

74

Xiamen Dapu Electronic Technology Co., Ltd.

bg23.png

Supported models

All models

m parameter 0

~ 6(A) and 65 ~ 71(B) select the same encoding system and the printing effect is the same m

parameter 0

none

If the width of the barcode exceeds the printable area, the printer will not print the barcode.

(B) 65

k is used for illustration and does not need to be transmitted

~6(A), the barcode data ends with NULL

Precautions

m When parameter 65 ~ 74 (B), the barcode data uses n to represent the data length.

mÿ

Spacing settings

Regardless of whether the input data length is 11 or 12, check digits are automatically inserted or corrected.

When printing UPCA (m = 0 or 65), please note:

bg65.png

(

Start character, middle separator, and end character are automatically inserted

6

)

UPCE

NSC

or

66

Automatically insert

0

m = 1

When the data length is

32

11

When the data length is

), you need to pay attention to:

7,

8,

Print

when, system characters (

12

and

bg66.png

d1

12\. Automatically insert or correct check digits

11

No matter the input data length is

Must be

6,

7,

8,

still

When , the first system character (

0

NSC

)

No matter the input data length is

6,

7,

8,

bg67.png

The conversion relationship between transmission data and printing data is as follows:

)Only

for

still

HRI

d6

5~9

6

bit data, excluding system characters (

when, it should be ensured

1~9

show

) and check code;

11

0,

d7,d8,d9,d10

NSC

for

12\. Barcode readable characters (

when

for

d11

bg68.png

still

m=2

Print

Print

(

Start character, middle separator, and end character are automatically inserted

still

7

67

), you need to pay attention to:

(

EAN8

or

12

Start and end characters are automatically inserted

68

m = 3

No matter the input data length is

or

EAN13

13\. Automatically insert or correct check digits

No matter the input data length is

), you need to pay attention to:

bg69.png

Start character, middle separator, and end character are automatically inserted

d1

(

Not a starting character

dn

CODE39

”, the encoder regards it as the terminator, and the remaining data is regarded as ordinary numbers.

\*

or

69

end character "

/

m = 4

when

8\. Automatically insert or correct check digits

\*

\*

), you need to pay attention to:

", the encoder automatically inserts"

Print

or

When encountering "

"

bg6a.png

Check digits are not automatically calculated and added

Check digits are not automatically calculated and added

(

(

CODABAR

ITF25

"

A

or

70

)(

NW-7

m=5

~

Start and end characters are automatically inserted

data processing;

71

m = 6

), you need to pay attention to:

or

Print

Print

The start character and end character will not be automatically inserted and need to be added manually by the user. The range is "

), you need to pay attention to:

bg6b.png

a"

~"

Start and end characters are automatically inserted

D

(

or"

), you need to pay attention to:

Character

"

Check digits are not automatically calculated and added

When setting barcode readable characters (

Two check codes are automatically calculated and inserted

d

CODE93

"

/

HRI

Print

) when printing, do not set any indication of the start

"

m=72

HRI

finished

bg6c.png

When CODE128 (m = 73) is selected:

When setting barcode readable characters (

The character set (CODE A, CODE B and CODE C) must be selected before barcode data.

code character

) when printing, control characters will be replaced by spaces

ÿ Selecting the character set is completed by sending the character "\{" combined with another character; ASCII

SHIFT

decimal code

•When using CODE 128, follow these instructions for encoding:

bg24.png

Send data with special characters

"\{" is done by sending the character "\{" twice in succession.

•Refer to Appendix A, CODE 128 for relevant information and character sets.

33ÿ

symbol

send data

ASCII code hexadecimal code decimal code

Xiamen Dapu Electronic Technology Co., Ltd.

Special characters

HRI

one of).

hexadecimal code

ASCII code

bg6d.png

123,66

\{A

7B,43

7B,53

CODEA

\{C

123,50

7B,32

\{3

123,65

CODEB

FNC1

123,67

7B,41

FNC3

7B,42

\{S

123,49

\{1

\{B

7B,31

123,83

7B,33

CODEC

\{2

FNC2

bg6e.png

FNC4

123,52

In this example, the printer first prints "No." using CODE B, and then prints "No." using CODE C.

CODE 128:

7B,34

GS k 73 10 123 66 78 111 46 123 67 12 34 56

•If the characters received by the printer are not barcode character set data, the printer stops at the point of this command.

processing, and treat the remaining data as ordinary data.

\{\{

7B,7B

1d 6b 49 0A 7B 42 4E 6F 2E 7B 43 0C 22 38

1b 40 1d 48 02 1d 68 64 1d 77 03

"\{"

rationalize and leave the remainder

\[Example\] For example, print "No. 123456"

123,51

The data below are treated as ordinary data.

•If the character set is not selected at the beginning of the barcode data, the printer will stop processing this command.

123, 123

rationalize and leave the remainder

\{4

Print the remaining digits:

This command is

•If "\{" and the character immediately following it are not the combination specified above, the printer stops

bg6f.png

•When the printer prints HRI characters, it does not print shift characters and character set selection data.

1d 6b 01 30 31 32 33 34 35 36 37 38 39 31 00

3432

Be sure to ensure the left and right gaps of the barcode. The gaps vary depending on the barcode type.

•HRI characters of control characters (<00>H to <1F>H and <7F>H) are not printed either;

Xiamen Dapu Electronic Technology Co., Ltd.

36 0D 0A

1d 6b 05 30 31 32 33 34 35 36 37 38 39 31 32 00

1d 6b 06 43 31 32 33 34 35 36 34 38 39 00

1b 40 1d 48 02 1d 68 64 1d 77 03

30 0D 0A

1d 6b 02 30 31 32 33 34 35 36 37 38 39 31 32 00

0D0A

Usage example

1d 6b 06 2D 31 32 42 24 2B 2D 2E 00

31 0D 0A

The data below are treated as ordinary data.

34 0D 0A

33 0D 0A

1d 6b 00 30 31 32 33 34 35 36 37 38 39 31 00

1d 6b 03 30 31 32 33 34 35 36 37 00

• HRI characters for function characters are not printed.

36 35 0D 0A

bg25.png

35 0D 0A

1D 6B 04 30 31 32 41 42 20 24 25 2B 2D 2E 2F 00

bg70.png

1d 6b 43 0c 30 32 33 34 35 36 30 30 30 30 38 39

37 32 0d 0a

36 36 0D 0A

1d 6b 46 09 30 31 32 33 34 35 36 30 30

1d 6b 47 05 32 33 34 35 36

36 37 0D 0A

9.9

1d 6b 49 0A 7B 42 4E 6F 2E 7B 43 0C 22 38

9.9.1 Set the module type of QR code

1d 6b 44 08 30 32 33 34 35 36 30 30

36 39 20 20 4e 4f 20 24 25 2b 2d 2e 2f 31 32 33 34 35 36 30 30 0D 0A

37 33 0d0a

1d 6b 48 0b 32 33 34 35 36 41 42 2e 2f 2b 2c

36 38 0D 0A

QR code printing instructions

37 30 20 20 20 30 32 33 34 35 36 30 30 C5 BC CA FD 0D 0A

1d 6b 41 0c 31 32 33 34 35 36 37 38 39 30 31 32

:

1d 6b 49 0A 7B 42 4E 6F 2E 7B 43 0C 22 38

1d 6b 45 11 4e 4f 20 24 25 2b 2d 2e 2f 31 32 33 34 35 36 30 30

Code 128

1d 6b 42 0c 30 32 33 34 35 36 30 30 30 30 38 39

Command name

37 31 0d 0a

37 33 0d0a

1b 40 1d 48 02 1d 68 64 1d 77 03

bg71.png

ASCII:GS(k pL pH cn fn n

code module type

QR

Function description

QR

Instruction code

16

ÿ

Hexadecimal: 1D 28 6b pL pH cn fn n

bg26.png

pL=3, pH=0

Parameter range

Decimal: 29 40 107 pL pH cn fn n

default value

35

set up

0

cn=49

Xiamen Dapu Electronic Technology Co., Ltd.

fn=67

code module type

set up

n

ÿ

bg72.png

Supported models

ASCII

Usage example

Decimal:

Precautions

GS ( k pL pH cn fn n

pL=3, pH=0

Parameter range

9.9.2 Set the error correction level error of QR code

Command name

hexadecimal:

29 40 107 pL pH cn fn n

none

cn=49

Instruction code

n=3

set up

1D 28 6b pL pH cn fn n

Set error correction level error for QR code

Function description

All models

:

code error correction level error

QR

bg73.png

Precautions

ÿ

Function

48

n

n

15

m

default value

n=48

Approximate representation of recovery (%)

refer to:

51

50

All models

fn=69

7

48

Supported models

Error correction level error L

ÿ

Set error correction level error for QR code

error correction level error

49

bg74.png

q

error correction level error

Print

Instruction code

51

code

Print

Function description

Usage example

none

:

ASCII

h30

Command name

error correction level error

29 40 107 pL pH cn fn m

GS ( k pL pH cn fn m

9.9.3 Print QR code

Decimal:

25

QR

1D 28 6b pL pH cn fn m

hexadecimal:

bg75.png

code

none

cn=49

Precautions

All models

pL=3, pH=0

1d 28 6b 03 00 31 51 30

1d 28 6b 03 00 31 52 30

bg27.png

Xiamen Dapu Electronic Technology Co., Ltd.

Usage example

Print the QR code.

fn=81

9.9.4 Print QR code

default value

QR

1d 28 6b 03 00 31 45 30

1b 40

36m=48

1d 28 6b 03 00 31 43 03

Parameter range

Supported models

1b 61 01

1d 28 6b 06 00 31 50 30 41 42 43

bg76.png

v=0

Decimal: 29 107 97 v rnL nH d1…dk

nnJC

Print QR code

ASCII: GS kmv rnL nH d1…dk

r represents the error correction level

v

Function description

Print QR code

d1…

Indicates the data length

Hexadecimal: 1D 6B 61 vr nl nH d1…dk

Indicates the specifications of the QR code,

Command name

Parameter range

dk

v

Indicates the QR code data to be printed

Instruction code

Indicates automatic selection of QR code specifications

ÿ

0

bg77.png

17

All models

rÿ

Usage example

Print the QR code.

ÿ

Set line spacing to

Command name

k = nL + 256 \* nH

default value

1B 61 01

1b 40

4

Supported models

ÿ

9.10

1D 6B 61 08 04 18 00 CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 BF C6 BC BC D3

none

D0 CF DE B9 AB CB BE 0D 0A

1

Precautions

9.10.1 Set the line spacing to n points

Print setup instructions

bg78.png

Function description

:

Xiamen Dapu Electronic Technology Co., Ltd.

point

ASCII

bg28.png

\= 33

n

default value

Decimal:

27 51 n

Parameter range

37

ESC 3n

Supported models

1B 33 n

n

n

0

hexadecimal:

ÿ

Instruction code

Set the line spacing to n points

255

ÿ

bg79.png

Precautions

BE 0d 0a

character height

1b 33 50

If the set line spacing is less than the maximum character height in a line, then the line spacing is equal to the maximum

BE 0d 0a

ASCII:GS L nL nH

Instruction code

Usage example

1b 40

BE 0d 0a

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 BF C6 BC BC D3 D0 CF DE B9 AB CB

If ESC 2, ESC @, the printer is reset, or the printer is powered off, the line spacing will return to the default value.

Decimal: 29 76 nL nH

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 BF C6 BC BC D3 D0 CF DE B9 AB CB

All models

9.10.2 Set left margin

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 BF C6 BC BC D3 D0 CF DE B9 AB CB

1b 33 30

BE 0d 0a

The line spacing is as follows:

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 BF C6 BC BC D3 D0 CF DE B9 AB CB

Set print position

Command name

bg7a.png

Function description

ÿ

0

×256

255

none

Supported models

Set the left margin to (

Precautions

ÿ

ÿ

255

Hexadecimal: 1D 4C nLnH

nL

default value

)point

ÿ

0

Parameter range

nH

All models

nL + nH

,

bg7b.png

The legend is as follows:

38

1b 40 1d 4c 48 00

9.11

BE

ASCII: ESC \* m Hl Hh \[d\]k

Decimal: 27 42 m Hl Hh \[d\]k

If the setting exceeds the printable range, the maximum value of printable units is used

Function description

bg29.png

Command name

Graphic vertical modulo data filling

This command is only valid when processing at the beginning of a line.

Xiamen Dapu Electronic Technology Co., Ltd.

Instruction code

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 BF C6 BC BC D3 D0 CF DE B9 AB CB

graphics print instructions

Print the longitudinal impression image data. The parameter meanings are as follows:

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 BF C6 BC BC D3 D0 CF DE B9 AB CB

BE 0d 0a

9.11.1 Graphic vertical modulo data filling

Hexadecimal: 1B 2A m Hl Hh \[d\]k

Usage example

0d 0a

bg7c.png

m mode

×3

Order density ×

2

32 24

Hl

,

horizontal ratio vertical ratio

Point double density ×

Point double density×

1

m is the dot plot format:

1

×1

2

×1

8

×31

33 24

0 8

Order density ×

bg7d.png

Used to indicate the number of bytes of dot map data and does not participate in transmission.

256

:

is the number of points in the horizontal direction (

Parameter range

Hl

for dot plot data

1,

32,

331

ÿ

Hh

k

Hl + Hh

×hh

m = 0

\[d\]k

)

,

XX58

bg7e.png

ÿ

1

ÿ

(when

m = 0

,

384

k = Hl + Hh

×256 )

×3 (when

×256

×256

m = 32

d

)

255

ÿ

k = (Hl + Hh

,

0

bg7f.png

XX80

576

,

d

0

:

×256

k = Hl + Hh

×

ÿ

1,

32,

331

ÿ

Hl + Hh

ÿ

255

m = 0

ÿ

bg80.png

(when

,

none

1

The relationship between dot plot data and printing effect is as follows:

m = 0

×3 (when

Precautions

\[d\]k If the corresponding bit is 1, it means that the point is printed, and if the corresponding bit is 0, it means that the point is not printed.

256

m = 32

The portion of the image that exceeds the printing area horizontally will be ignored.

)

Supported models

×256 )

k = (Hl + Hh

All models

,

default value

bg81.png

1

The print buffer is cleared after printing is completed.

twenty four

Xiamen Dapu Electronic Technology Co., Ltd.

)

Print

After filling the dot plot, generally use

39

(

m = 0

,

33.  Dot images are printed separately

bg2a.png

,

After filling in the graphics data, you can continue to fill in other information so that the graphics and other information are

If the height of the image that needs to be printed is large, it can be split into several strips with a height of

(

(

8

m = 32

ESCJ

This command only fills the print buffer. The printing of the image will not start until the print command is received. Figure

or

bg82.png

n

will be offset. If there is a disconnection in the middle, please send data continuously)

1b 2a 00 0C 00 FF FF FF FF FF FF FF FF FF FF FF FF

refer to

Usage example

Instruction code

ASCII

) command to print, you can also use

GS v 0

Like discontinuity, you can set the line spacing to

9.11.2 Picture horizontal mold data printing

Command name

\= 24

0, it will not feed too much paper. (Start of dot matrix printer

Picture horizontal mold data printing

command to print, but

1B 33 00

Decimal:

The command will trigger the paper feeding operation (feeding paper according to the line spacing), so that the multi-line drawing

LF

0A

:

LF

1B 40

bg83.png

Print the horizontal mold image data. The meaning of the parameters is as follows:

\[d\]k is dot plot data

hexadecimal:

3,51 times width x height × 2 × 2

xL, xH are the number of bytes in the horizontal direction (xL + xH × 256)

0 ÿ yL ÿ255, 0 ÿ yH ÿ255

0 ÿ d ÿ 255

1D 76 30 m xL xH yL yH \[d\]k

XX80:

1,49 times wide × 2 × 1

XX58:

0 ÿ m ÿ 3; 48 ÿ m ÿ 51

29 118 48 m xL xH yL yH \[d\]k

2,50 times higher × 1 × 2

1 ÿ xL + xH×256 ÿ 48

m is bitmap mode:

k is the number of bytes of dot map data, k is used for illustration and does not need to be transmitted

0,48 normal × 1 × 1

m mode horizontal ratio vertical ratio

Parameter range

k = (Hl + Hh×256)×(yL + yH×256)

Function description

yL, yH are the number of points in the vertical direction (yL + yH × 256)

bg84.png

k = (Hl + Hh×256)×(yL + yH×256)

It means that the point is printed, and the corresponding bit is

1ÿ xL + xH×256 ÿ 72

\[d\]k

The corresponding bit is

When this command is executed, paper is fed according to the image size, regardless of

ESC 2

0 ÿ yL ÿ 255, 0 ÿ yH ÿ 255

ESC 3

All models

Xiamen Dapu Electronic Technology Co., Ltd.

40

0 ÿ m ÿ 3; 48 ÿ m ÿ 51

Precautions

If the horizontal bytes of the image exceed the printing area, the excess portion will be ignored.

default value

0, it means that the point is not printed

Supported models

none

bg2b.png

,

1

0 ÿ d ÿ 255

bg85.png

After this command is executed, the printing coordinates are reset to the left margin position and the image content is cleared.

Command name

Usage example

Decimal: 16 04 01

Check paper out status

Supported models

Precautions

The relationship between bitmap data and printing effects is as follows:

If the paper is successful, the paper status "FE 23 12" will be returned only once.

10 Printer status and settings

Check paper out status

Parameter range

The impact of line spacing settings

10.1 Out of paper status

default value

1B 40

Hexadecimal: 10 04 01

FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF

1d 76 30 00 03 00 09 00

Function description

When the printer is out of paper, it will automatically return to the paper out-of-paper status "EF 23 1A" once a second until it is loaded.

This command has a printing function. It prints while transmitting data. There is no need to use the printing command.

Instruction code

bg86.png

10.2

Supported models

Send the paper shortage check command: 10 04 01, and the data will be returned once sent.

Print status

Parameter range

Return data automatically:

FC 4F 4B

Return data: FE 23 12 (the printer has paper)

If there is a shortage of paper during the printing process of sending data, FC 6E 6F (printing failure) will be returned.

Instruction code

bg2c.png

Xiamen Dapu Electronic Technology Co., Ltd.

Usage example

Function description

41

Print status

Precautions

Print status

Command name

Send printer data. The printer completes printing after 500ms (milliseconds). If no data is sent, the printer will automatically

(Print completed)

default value

EF 23 1A (printer out of paper)

bg87.png

Set printer baud rate

Function description

10.3

31 45 85 1 m

hexadecimal:

baud rate

0

Set the printer serial port baud rate

15

US-U 1 m

M value

baud rate

Usage example

Decimal:

M value

Instruction code

M<29

307200

:

ASCII

Baud rate corresponding value

1200

Command name

1F 2D 55 01 m

bg88.png

2400

921600

23600

19

4

6

14400

16

19200

4800

9600

20

1

18

1843200

9

17

1228800

8

3

614400

5

7

28800

460800

7200

bg89.png

10

Parameter range

76800

Supported models

default value

10.4 Set the default serial port open or closed state when power is off

Command name

57600

Instruction code

14

1F 2D 55 01 m

Return data: 1F 2D 55 01 m (the return data format is the same as the delivery)

38400

230400

Usage example

12

Precautions

13153600

115200

Issue instructions:

Set serial port communication on and off

11

M=5 default baud rate 9600

bg8a.png

M=0, open the serial port M= 1, close the serial port

M=0 The default serial port is open

Decimal: 31 45 113 1 m

Work.

Parameter range

Issue command: 1F 2D 71 01 m

After sending the setting data, the printer will print out "Successfully Set The Uart open state is

Hexadecimal: 1F 2D 71 01 m

Return data: 1F 2D 71 01 m (the return data format is the same as the issued one)

Xiamen Dapu Electronic Technology Co., Ltd.

Valid after power cycle. This command is only used for preliminary settings and is not required during the printing process.

To call this command.

ASCII: US-q1m

42

Usage example

Prevent the device from communicating with the device's serial port if: the serial port close mode is set and the printer receives any

Supported models

bg2d.png

No data will be processed to prevent data interference from affecting the normal operation of the printer when not printing.

Precautions

"Close"

default value

Function description

bg8b.png

Set the serial port status (this command will not be saved when the power is turned off)

1F 77 m

ASCII

This command is used during the printing process. Before sending data, set the serial port to open mode and then send the data.

Function description

First open the serial port----send printing data---then close the serial port

Usage example

Command name

1F 77 00 (

31 119 m

default value

Supported models

10.5

hexadecimal:

Precautions

:

Print the data and then close the serial port before sending.

Decimal:

U w

Parameter range

Issue instructions:

M=0, open the serial port, M= 1, close the serial port

Instruction code

bg8c.png

CF C3 C3 C5 B4 EF C6 D5 B5 E7 D7 D3 BF C6 BC BC D3 D0 CF DE B9 AB CB

Set whether to feed paper, paper feeding function, and how long it takes to end data feeding

)

10.6

Set whether to feed paper, the number of paper feeding lines, and how long it takes to finish data feeding.

31 45 53 4 mk tL tH

hexadecimal:

1b 40

Function description

Close the serial port again

:

US - 5 nmk tL tH

Open the serial port first

)

Decimal:

BE

Instruction code

After data printing is completed, set whether to feed paper, the number of paper feeding lines, and how long after the data is completed to start paper feeding.

1F 77 01 (

0d 0a

ASCII

1F 2D 35 04 mk tL tH

Parameter range

Command name

1b 33 30

bg8d.png

43k :

Mainly used in small ticket mode

m: 0, paper feeding, 1, no paper feeding

m=0,k=2,tL+tH\*256 = 200=C8 00

Supported models

Command name

Cut the whole paper

bg2e.png

Decimal: 27 105

200ms

Return data:

1F 2D 35 04 00 05 C8 00 (The return data format is the same as the delivery)

10<=tL + tH \*256 <=1000;n=0,1;1<=k<=256;

default value

10.7 Full cut paper

Number of paper feeding lines

Usage example

Determine the end time of data, default

tL+tH\*256:

Issue command: 1F 2D 35 04 00 05 C8 00

Instruction code

Xiamen Dapu Electronic Technology Co., Ltd.

Precautions

bg8e.png

none

10.8 Half-cut paper

Function description

1B 40

30 30 30 0D 0A

Function description

cut in half with knife

The cutter cuts the paper completely

none

Instruction code

Decimal: 27 109

Hexadecimal: 1B 69

Usage example

Hexadecimal: 1B 6D

default value

Command name

Precautions

none

Cut the whole paper

, there is still a little bit of paper left that has not been cut off, gently pull out the paper with your hands.

Parameter range

1B 69

bg8f.png

none

10.9 Set whether to automatically cut the knife

Precautions

Instruction code

Command name

If you set the automatic cutter with the door closed, you need to add a cutter command before the paper will be cut after printing is completed.

bg2f.png

default value

44

30 30 30 0D 0A

Hexadecimal: 1F 2D 61 02 mn

Function description

Parameter range

1B 6D

If the automatic cutter is set to be turned on, the paper will be cut automatically without adding a cutter command after printing is completed.

none

ASCII: US-a 2 mn

1B 40

Usage example

Decimal: 31 45 97 2 mn

Xiamen Dapu Electronic Technology Co., Ltd.

none

Set whether to automatically cut the knife

bg90.png

Issue command: 1F 2D 61 02 01 00 (threshold is 0x0150)

M = 1 (turn on automatic cutter)

10.10

do

Return data: 1F 2D 61 02 01 00 (the return data format is the same as the delivery)

:

US-M lm

Parameter range

31 45 77 1 m

Supported models

Set printing mode

Instruction code

It is mainly used for driver printing. Some printer drivers do not have a cutter function. Need to add automatic cutter action

Precautions

ASCII

N = 0 (half cut)

Set printing mode

default value

N = 1 (all cut)

Command name

Decimal:

M = 0 (turn off automatic cutter)

Usage example

bg91.png

1F 2D 4D 01 m

m=0x01 (tag mode)

Parameter range

Issue instructions: 1F 2D 4D 01 01

Supported models

1B 40 1B 61 01 1D 48 02 1D 68 50 00 1D 77 02 00 1D 6B 49 0b 31 32 33 34 35 36 37 38 39 31 30

1B 40

Function description

1B 61 00//

(Small ticket mode)

11

Comprehensive printing example

hexadecimal:

default value

11.1 Barcode printing

m=0x01 (

Return data: 1F 2D 4D 01 01 (the return data format is the same as the delivery)

Barcode on the left

),m=0x02

Label mode

Usage example

Initialize printer

Set printing mode

Precautions

bg92.png

1D 48 00 //

1D 48 01 //

Xiamen Dapu Electronic Technology Co., Ltd.

Barcode centered

No numbers displayed, only barcodes

Note that barcodes do not support Chinese characters and Chinese characters.

11.2 Text printing

1B 61 02//

1B 40 1B 33 10 //Set line height distance 10 and line spacing range 10,20,30,40,50,60

1D 48 03 //

1D 77 02 00 //1D 77 sets the barcode width 03 00 to 2 width, the width range is 1-6

1D 6B 49 //Barcode type CODE128

1B 61 01//

Data is displayed above and below the barcode

0B 31 32 33 34 35 36 37 38 39 31 30 // 0B is the data length 11, barcode data 31 32 33 34 35 36 37 38 39 31 30 content "12345678910"

Data is displayed above the barcode

45

Data is displayed below the barcode

1D 48 02 //

1D 68 50 00 //1D 68 sets the barcode height 50 00 to 80 height, the height range is 10-200

1B 40 1B 33 10 1D 21 11 1B 61 01 BB B6 D3 AD B9 E2 C1 D9 0D 0A

Barcode on the left

bg30.png

bg93.png

1B 40 1B 33 60

0D 0A terminator, can also be used as line break

1B 40 1B 33 30

1B 61 01 //Center alignment of text

1B 61 02 //text right aligned

46

1d 28 6b 03 00 31 43 03//QR code size 43 02, 43 03, 43 04, 43 05, 43 06, 43 07, 43 08

1B 40 1B 33 40

1d 28 6b 06 00 31 50 30 41 42 43 //06 00 data length (31 50 30 41 42 43) 6 data lengths,

1D 21 01 //Double the font height

fixed

bg31.png

1B 40 1B 33 20

1B 61 00 //Text left aligned

Xiamen Dapu Electronic Technology Co., Ltd.

1D 21 00 //Normal font size

11.3 QR code printing

31 50 30 fixed, 41 42 43 QR code content "ABC"

1D 21 10 //Double the font width

1D 21 11 //Double the font size

1b 40//

1d 28 6b 03 00 31 45 30 //Fixed

1B 40 1B 33 50

BB B6 D3 AD B9 E2 C1 D9 Text print content "Welcome"

bg94.png

1b 40

1b 40//Fixed

1d 28 6b 06 00 31 50 30 41 42 43

1d 28 6b 03 00 31 52 30//Fixed

1d 28 6b 03 00 31 43 08

C9 A8 D2 BB C9 A8 B9 D8 D7 A2 0d 0a 0d 0a 0d 0a 0d 0a 0d 0a 1b 69

Scan to follow

1d 28 6b 03 00 31 51 30//Fixed

1D 76 30 00 07 00 2F 00

0d 0a //Newline

1d 28 6b 03 00 31 51 30

1b 40 1d 21 00

1b 61 01// 00 QR code is on the left 01 QR code is in the center 10 QR code is on the right

1b 69//Cut paper

1b 61 01

1b 61 01//00 Left 01 Center 10 Right

1b 61 01

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 07 F0 00 00 00 00 01 FF FF 58 00 00 00

C9 A8 D2 BB C9 A8 B9 D8 D7 A2//Text content "Scan to follow"

1d 21 00//00 Normal 01 times width 10 times height 11 times width and height

1d 28 6b 03 00 31 52 30

11.4 Horizontal image printing

1F DF FF FC

Text content printing

1d 28 6b 03 00 31 45 30

bg95.png

1F 80 07 E0 3F F8

00 00 7E 87 00 01 F8 00 00 3C 03 C1 C3 F0 00 00 00 01 FF E7 E0 00 00 00 00 7F F7 C0 00 00 00 00 1F F7 80 00 00

00 00 00 00 00

07 01 00 00 00 00 00 07 00 00 00 00 00 00 07 00 00 00 00 00 00 07 00 00 00 00 00 00 06 40 00 00 00 00 00 09 40

F6 00 00 00 00 00 00 C6 00 00 00 00 00 01 C2 00 00 00 00 00 01 C1 00 00 00 00 00 01 81 00 00 00 00 00 03 81 00

00 //Fourth digit data normal picture size

07 00 Picture width Divide the actual width of the picture by 8 to get the byte data

C0 1E C0 00 00 FF E1 80 1E 40 00 33 FF 07 00 1E 60 00 00 7F 00 00 7F 34 00 00 FE 00 00 7F 72 00 07 FC 00 00 7F

Next is the image data.

47

00 00 00 00

1b6d

00 00 00 E0 00 40 FC 00 00 07 80 00 01 FC 00 06 1E 00 7E 07 FE 00 01 7E 03 FE 1F FE 80 1C 44 07 FE 3F FE C0

00 00 00 00 00 01 FE 00 00 00 00 00 00 7E 00 00 00 00 00 00 7E 00 00 00 00 00 00 7E 00 00 00 00 00 00 6E 00

1D 76 30 //Print horizontal impression image data

1A 30 00 19 00 15 00 0c 85 03 00 31 38 30 31 30 36 30 30 30 30 32 00

1A 54 01 2b 00 a5 00 18 00 00 11 31 20 38 20 30 20 31 20 30 20 36 20 30 20 30 20 30 20 30 20 32 00

1A 5D 00 1A 4F 00

00 00 07 FF

00 00 00 00

11.5 Print label barcode

Xiamen Dapu Electronic Technology Co., Ltd.

bg32.png

00 09 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

2F 00 picture height

1A 5B 01 00 00 00 00 80 01 ff 00 00

CC 00 F1 FC

00 00 00 00

bg96.png

A 5B 01 00 00 00 00 80 01 ff 00 00 //1A 5B 01 00 00 00 00 Label start, 80 01 ff 00 Set label printing range width and height 80 01

width, ff

X, Y axis position

1B 6d //Half cutter 1B 69 //Full cut

48

bg33.png

1A 5D 00 1A 4F 00 1b 6d

Instruction parsing

00 high, ending with 00

The content below the "31 20 38 20 30 20 31 20 30 20 36 20 30 20 30 20 30 20 30 20 32" barcode 18010600002 ends with 00

1A 5B 01 00 00 00 00 80 01 EA 00 00

1A 31 00 05 04 15 00 15 00 04 00 53 54 4A 41 31 30 33 31 39 31 31 30 30 30 30 31 00

1B 6d

1A 5D 00 1A 4F 00 //End of label, must be present otherwise it will not print

1A 54 01 00 00 b0 00 00 60 00 11 53 54 4A 41 31 30 33 31 39 31 31 30 30 30 30 31 00

Standard, 0c 85 03 00 fixed value, 31 38 30 31 30 36 30 30 30 30 32 barcode content 18010600002, ending with 00

11.6 Print label QR code

Double the font size, "33", "44", "55", "66"

//1A 54 01 text printing, 2b 00 a5 00 text X, Y axis position coordinates, "18 00 00 11 " "11" is to set the font size, change "20" to double

the height, "22"

Command example:

1A 30 00 19 00 15 00 0c 85 03 00 31 38 30 31 30 36 30 30 30 30 32 00 //1A 30 00 barcode instruction 19 00 15 00 barcode

Xiamen Dapu Electronic Technology Co., Ltd.

bg97.png

05 Set the QR code version value range \[0-20\]. The larger the value, the denser the QR code.

00" sets the width and height of the printing area. 00 ends

00 End data stream

00 00 b0 00X,Y axis printing position

1A 54 01 00 00 b0 00 00 60 00 11 53 54 4A 41 31 30 33 31 39 31 31 30 30 30 30 31 00 Print text content label command

bg34.png

Xiamen Dapu Electronic Technology Co., Ltd.

1A 31 00 05 02 15 00 15 00 04 00 53 54 4A 41 31 30 33 31 39 31 31 30 30 30 30 31 00 //Print QR code

00 Rotation angle \[0-3\] 0, 90°, 180°, 270°

1A 5D 00 //label printing ends

1A 4F 00 //Print content onto paper.

1A 5B 01 00 00 00 00 80 01 EA 00 00 //Set the printing range "00 00 00 00" and set the initial position of X and Y axis printing. The default

is 0, "80 01 EA

53 54 4A 41 31 30 33 31 39 31 31 30 30 30 30 31 QR code content "STJA103191100001"

1b 6d cut paper

03 Error correction level value range \[1-4\] Low error correction, more data, high error correction, less data

00 60 00 Fixed

04 QR code size value range \[1-7\]

15 00 15 00 X, Y axis printing position

11, printing text size, 11, 22, 33, 44, 55, 66 have 6 font sizes, all are doubled

1A 31 00 Print QR code label

1A 54 01 Text printing label starts

bg98.png

11.7 Print label image

1A 21 01 52 00 00 00 c8 00 c8 00 00 11 Label picture printing command

1A 21 01 52 00 00 00 c8 00 c8 00 00

00 00 00 00

00

00 00 00 00

FF FC 00 00 00 00 00 00 00 00 00 01 FF F0 00 00 00 00 00 00 00 00 00 00 01 FF FC 00 00 00 00 00 00 00 00 00 03

Image width and height 200=C8 00

00 00 00 00 00 00 00 00 01 FF FC 00 00 00 00 00 00 00 00 00 07 FF F8 00 01 FF FF 00 7F FF FF E0 00 01 FF FC 00

Below is the image data

00 00 00 00 00 00 00 FF FE 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FE 00 00 00

00 00 00 00

49

1A 5B 01 00 00 00 00 80 01 E6 00 00

00 00 00 3F 80 00 00 00 00 00 00 00 00 00 00 00 FF FE 00 00 00 00 00 00 00 00 00 00 FF C0 00 00 00 00 00 00 00

FF FF F8 00 01

FF FC 00 00 00 00 1F FF FF FF 80 0F FF FC 00 1F FF FF 0F FF FF FF FC 00 01 FF FC 00 00 00 01 FF FF FF FF F0 0F

FF FE 00 1F FF FF

1A 21 01 Picture printing command starts

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FE 00 00 00 00 00 00 00 00 00 00 00 00

00 00 00 00 00

c8 00 c8 00 is the c8 00 width and C8 00 height of the image, calculated based on the actual image width.

52 00 00 00 is 52 00 is the X-axis lateral displacement 00 00 is the Y-axis longitudinal displacement

00 00 00 00

FF F8 00 00

00 00 00 07 FF FC 00 07 FF FF 03 FF FF FF F8 00 01 FF FC 00 00 00 00 00 00 00 00 00 0F FF FC 00 0F FF FF 07 FF

1A 5B 01 00 00 00 00 80 01 E6 00 00 Set the label paper size.

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

bg99.png

00 1F FF 00 7F

3F FF 00 3F FF 00 7F FC 00 00 03 FF F0 00 00 3F FE 00 01 FF F8 00 00 00 00 3F FF 00 3F FF 00 7F FC 00 00 07 FF

FC 00 07 FF FF

00 01 FF F8 00 00 00 00 3F FF 00 3F FF 00 7F FC 00 00 07 FF F0 00 00 3F FE 00 01 FF F8 00 00 00 00 3F FF 00 3F

0F FF FF FF FF F8

F8 03 FF F0

3F FF 00 3F FF

Xiamen Dapu Electronic Technology Co., Ltd.

FF F8 00 00 3F

00 0F FF F0 00 00 7F FE 00 01 FF F8 00 00 00 00 3F FF 00 3F FF 00 7F FC 00 00 1F FF F0 00 00 3F FE 00 01 FF F8

00 01 FF F8 00 7F

3F FF 00 7F FC

0F FF FC 00 3F FF 80 1F FF 80 FF FC 00 03 FF FF FF FF F0 1F FF FF FF FF F8 0F FF FC 00 3F FF 80 1F FF 00 7F FC 00

FF 00 3F FF 00 7F FC 00 07 FF FF FF FF F0 3F FE 00 01 FF F8 3F FF FE 00 3F FF 00 3F FF 00 7F FC 00 07 FF FF FF

0F FF C3 FF F0 7F

E0 1F FF FF FF FF F8 0F FF FC 00 3F FF 80 1F FF 00 7F FC 00 00 FF FF FF FF C0 3F FF 80 03 FF F8 07 FF FC 00 3F FF

F8 00 00 00 00

FF F8 3F FF FF 00 3F FF 00 3F FF 00 7F FC 00 07 FF FF FF FF F0 7F FE 00 01 FF F8 7F FF FF 00 3F FF 00 3F FF 00 7F

FC 00 00 03 FF FC 00 00 3F FF 00 03 FF F8 07 FF F8 00 3F FF 00 3F FF 00 7F FC 00 00 03 FF F8 00 00 3F FF 00 01 FF

0F FF FF FF FC 00 03 FF FF FF FF F0 07 FF FF FF FF F8 0F FF FE 00 1F FF C0 1F FF E1 FF FC 00 03 FF FF FF FF F0

F0 00 00 7F FE

FF FF F0 7F FE 00 01 FF F8 7F FF FF 00 3F FF 00 3F FF 00 7F FC 00 07 FF FF FF FF F0 7F FE 00 01 FF F8 7F FF FF 80

bg35.png

00 7F FC 00 00 1F FF E3 FF F0 3F FE 00 01 FF F8 00 FF FF 80 3F FF 00 3F FF 00 7F FC 00 00 0F FF E3 FF F0 3F FE

00 3F FF 00 3F FF 00 7F FC 00 00 03 FF F8 00 00 3F FF 00 01 FF F8 01 FF E0 00 3F FF 00 3F FF 00 7F FC 00 00 03

FF 00 7F FC 00

50

FE 00 01 FF F8 00 7F C0 00 3F FF 00 3F FF 00 7F FC 00 00 03 FF F8 00 00 3F FE 00 01 FF F8 00 0E 00 00 3F FF 00

00 00 00 00 3F

FF 80 3F FF 00 3F FF 00 7F FC 00 00 0F FF E3 FF F0 3F FE 00 01 FF F8 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00

FF F0 7F FE 00 01

01 FF FF FF FF

00 00 03 FF F8 00 00 3F FE 00 01 FF F8 00 00 00 00 3F FF 00 3F FF 00 7F FC 00 00 03 FF F8 00 00 3F FE 00 01 FF

bg9a.png

00 7F FC 00

01 FF FF 81 FF FC 3F FE 1F FF FF F0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 07 FF FF 81 FF FC 3F FE 1F FF FF E0

00 00 00 00 00

FF FF FF FF E0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 7F FF F0 00 00 00 00 00 3F FF F0 00 3F FF 80 3F FF 00 3F

00 00 00 00

FF 00 7F FC

00 3F FF 00 7F FC 00 07 FF FF 80 FF FC 3F FE 1F FF FF E0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 07 FF FF 80 FF FC

00 00 7F FF C0 00 00 00 00 00 1F FF F0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 7F FF 80 00 00 00 00 00 0F FF F0

00 3F FF 80

80 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 07 FF FF 00 FF FC 3F FE 1F FF FE 00 00 3F FF 80 3F FF 00 3F FF 00 7F FC

FF 00 3F FF

3F FF 00 3F FF 00 7F FC 00 00 7F FF 80 00 00 00 00 00 07 FF F0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 7F FF 00

00 3F F0 07 F0 1F FF 00 00 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3F FF 80

FF F8 3F FE

FF FF E0 00 3F

00 07 FF F0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 7F FF 00 00 00 00 00 00 07 FF F0 00 3F FF 80 3F FF 00 3F FF

00 7F FC 00

FF 00 7F FC 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 00 00 00 00 00 00

FF FF FF FF FF

00 3F FF 80 3F FF

FE 00 01 FF F8 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 1F FF C3 FF F8 7F FE 00 03 FF F8 00 3F FF 80 3F FF 00 3F

00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00

FF 00 7F FC

00 00 1F FF C3 FF F8 3F FE 00 03 FF F8 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 1F FF C1 FF F8 3F FE 00 03 FF F8

00 3F FF 80

3F FE 1F FF FF

00 00 00 00 00 00 00 00 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 03 FF FF FF FF FF FF FF FF FF 00 00 3F FF 80 3F

3F FF 00 3F FF 00 7F FC 00 00 1F FF C1 FF F8 3F FE 00 07 FF F8 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 1F FF C1

00 03 FF F8

00 7F FC 00 00 0F FF FF FF FF FF FF FF FF FF C0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 1F FF FF FF FF FF FF FF

00 00 00 00

FF 80 3F FF 00 3F FF 00 7F FC 00 00 3F FF FF FF FF FF FF FF FF FF E0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 3F

00 0F FF F8 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 3F FF 81 FF FC 3F FE 00 3F FF F0 00 3F FF 80 3F FF 00 3F FF

3F FF 00 3F

bg9b.png

00 00 00 00

3F FF 07 FF FC 00 00 7F FF 00 3F FF FF FF FF FF FF E0 00 3F FF 80 07 FF FE 3F FF 07 FF F8 00 00 7F FF 00 3F FF FF

7F FF 00 00 00

FF 80 00 3F FF FF FF FF FF FF FF FF FF E0 00 03 FF FF FF FF FF FF FF FF FF FF 00 00 1F FF FF FF FF FF FF FF FF

00 00 00 00

00 3F FF 80 3F

00 3F FF 80 03 FF FE 3F FF 07 FF F8 00 00 7F FF 00 3F FF FF FF FF FF FF C0 00 3F FF 80 00 7F FE 3F FF 07 FF E0

FF FF FF FF FF FF FF 00 00 1F FF FF FF FF FF FF FF FF FF E0 00 00 0F FF FF FF FF FF FF FF FF FE 00 00 07 FF FF

00 00 00 00

FF FF FF FF FF FF 00 00 3F FF 80 00 00 00 3F FF 00 00 00 00 00 7F FF 00 00 00 00 00 00 00 00 00 00 3F FF 80 00 00

00 00 00 00

E0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 FF FF FF FF FF FF FF FF FF C0 00 00 00 00 00 00 00 00 00 00 00

00 00 00 00 7F FF 00 00 00 00 00 00 00 00 00 00 3F FF 80 00 00 00 1F FF 00 00 00 00 00 7F FF 00 00 00 00 00 00

01 FF FC 00 00

00 7F FF E0 00

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

3F FF 80 0F FF FE

FF 80 00 00 00 1F FE 00 00 00 00 00 7F FF 00 00 00 00 00 00 00 00 00 00 3F FF 80 00 00 00 00 00 00 00 00 00 00

FF FF FF FF FF

FF FF FF FF E0

00 7F FF 00 00 00 00 00 00 07 FF E0 00 3F FF 80 3F FF 00 3F FF 00 7F FC 00 00 7F FF 00 00 00 00 00 00 07 FF E0

00 00 00 00 00 00 00 1F FF C0 00 00 00 00 00 00 00 00 00 00 7F FF 00 00 00 00 00 00 00 00 00 00 1F FF C0 00 00

FF E0 00 01 FF FF FF

FF 00 3F FF 00 7F FC 00 00 7F FF 00 00 00 00 00 00 07 FF E0 00 3F FF 80 1F FF 80 3F FF 00 FF FC 00 00 7F FF 00 00

FF FF FF FF FF FF FF

00 00 7F FF 00 3F

00 00 00 00 7F FF 00 00 00 00 00 00 00 00 00 00 1F FF E0 00 00 00 00 00 00 00 00 00 00 7F FF 00 00 00 00 00 00

00 3F FF 00

07 FF E0 00 3F FF 80 1F FF C0 3F FF 00 FF FC 00 00 7F FF 00 00 00 00 00 00 0F FF E0 00 3F FF 80 1F FF FE 3F FF

1F FF FC 00 00 00 00 00 00 00 00 00 00 7F FF 80 00 00 00 00 00 00 00 00 00 1F FF FF FF FF FF FF FF FF FF FF 80

00 00 00 00 00

00 00 00 00 00 00 00 00 0F FF FF FF FF FF FF FF FF FF FF 80 00 3F FF FF FF FF FF FF FF FF FF C0 00 07 FF FF FF FF

7F FF 00 00 00 00 00 00 1F FF E0 00 3F FF 80 1F FF FE 3F FF 07 FF FC 00 00 7F FF 00 3F FF FF FF FF FF FF E0 00

00 00 00 00 3F

bg9c.png

00 00 00 00

00 00 00 00 00 00 00 0F F0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 1F FC 00 00 00

E0 00 00 00 1F

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 3F FE 00 00 00 00 00 00 00 00 00 00 00 00 03 FF C0 00 00 03 FF

Xiamen Dapu Electronic Technology Co., Ltd.

00 00 00 00

00 07 FF E0 00

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

00 00 00 00

3F FF 00 00 01 FF FF FF FF FF 80 00 00 00 03 FF E0 00 00 03 FF E0 00 00 00 7F FF 80 00 0F FF FF FF FF FF F0 00

E0 00 00 0F FF

00 00 00 00

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

00 00 03 FF E0 00 00 00 7F FF C0 00 7F FF FF FF FF FF F8 00 00 00 07 FF E0 00 00 03 FF E0 00 00 00 3F FF E0 00

FF F0 00 00 FF FC

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

00 00 00 00

FF F8 00 00 00 07 FF E0 00 00 03 FF E0 00 00 00 3F FF E0 01 FF FF FF FF FF FF F8 00 00 00 07 FF E0 00 00 03 FF

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

bg36.png

00 00 00 00

FF F0 03 FF FC 00 00 3F FF FC 00 00 00 07 FF E0 00 00 03 FF E0 00 00 00 1F FF F0 03 FF F0 00 00 1F FF FC 00 00

51

00 03 FF E0 00 00 00 0F FF F8 07 FF F0 00 00 0F FF FC 00 00 00 07 FF F0 00 00 07 FF F0 00 00 00 03 FF F8 07 FF

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

C0 00 00 00

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

00 00 00 00

00 00 03 FF E0

FC 00 03 FF FF FF FF FF FF FF FF FF FF F0 00 01 FF FC 07 FF E0 00 00 0F FF FC 00 07 FF FF FF FF FF FF FF FF FF

FF FF FF FF FF

00 00 00 00

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 03 C0 00 00 00 00 00 00 00 00 00 00 00 00

bg9d.png

FF FF FF F0 03 FF

00 00 00 3F FF 00 FF FF C0 00 3F FF F8 00 03 FF FF FF FF FF FF FF FF FF FF F0 00 00 3F FF 00 7F FF E0 00 FF FF F8

FF FF FF 00 00

07 FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF C0 0F FF FC 00 07 FF FF FF 00 00 00 00 00 00 00 00

00 00 0F FF FC

FF FF FF FF FF FF

FF FF FF FF FF FF FF F0 00 00 7F FF 00 3F FF E0 01 FF FF F0 00 07 FF FF FF FF FF FF FF FF FF FF F0 00 00 7F FE

00 FF FF 80 1F FF C0 00 00 FF FF FC 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF FF 80 1F FE 00 00 00 00 00 00

0F FF FC 00 00 00

FF E0 00 07 FF FF FF FF FF FF FF FF FF FF F0 00 00 7F FE 00 0F FF 00 3F FF FF C0 00 07 FF FF FF FF FF FF FF FF

FF FF FF FF FF

00 00 00 00 00 00 00 00 01 FF FF 00 1F F0 00 00 00 00 00 00 00 03 FF FF FF FF FF FF FF FF FF FF C0 01 FF FE 00

FE 00 03 FC 00 FF FF FF 80 00 00 00 0F FF F0 00 00 07 FF F0 00 00 00 00 FF FE 00 00 00 07 FF FF FE 00 00 00 00

3F FE 03 FF FE

FF FF FF 80 07 FF

00 00 00 00 07 FF FF FF FF FF FF FF FF FF FF FF F0 01 FF FC 00 00 00 00 00 00 00 00 00 00 07 FF FF FF FF FF FF FF

00 07 FF E0 00

07 FF E0 00 00 00 01 FF FE 00 00 00 3F FF FF F0 00 00 00 00 07 FF E0 00 00 03 FF E0 00 00 00 03 FF FC 00 00 00

FF E0 07 FF FF 80

00 07 FF FF FF

07 FF E0 00 00 0F FF FC 00 07 FF FF FF FF FF FF FF FF FF FF F0 00 00 7F FE 07 FF E0 00 00 0F FF FC 00 07 FF FF

00 00 00 07 FF E0 00 00 03 FF E0 00 00 00 07 FF FC 00 00 07 FF FF F0 00 00 00 00 00 07 FF F0 00 00 07 FF F0 00

00 00 00 00 00

FF FF E0 00 00 7F FE 07 FF F0 00 00 0F FF FC 00 07 FF FF FF FF FF FF FF FF FF FF C0 00 00 3F FE 07 FF F0 00 00

00 00 00 00 00

00 1F FF C0 07 FF

00 00 3F FF FF 00 00 00 00 03 FF FF FF FF FF FF FF FF FF FF F0 00 1F FF F8 00 01 FF FF F8 00 00 00 00 07 FF FF FF

07 FF E0 00 00 07 FF F0 00 00 00 00 3F FE 03 FF F8 00 00 0F FF FC 00 00 00 07 FF E0 00 00 03 FF E0 00 00 00 00

FF FF E0 00 00 FF

FF FF F0 00 1F FF F8 00 07 FF FF C0 1F FF FF 00 07 FF FF FF FF FF FF FF FF FF FF F0 00 3F FF F0 00 3F FF FE 00

0F 80 00 00 00

FF FF FF FF FF FF FF FF FF E0 00 7F FF F0 00 FF FF F0 03 FF FF FF 80 07 FF FF FF FF FF FF FF FF FF FF E0 00 7F

00 00 1F FF FC 00 00 00 07 FF E0 00 00 03 FF E0 00 00 00 00 3F FF 01 FF FF 00 00 1F FF F8 00 00 00 07 FF E0 00

07 FF E0 00 00

bg9e.png

C4 9F FF F0 03 FF F0 00 00 00 00 7F FF 80 00 00 00 07 FF FF FF FF FF FF FF FF FF FF F0 03 FF F0 00 03 FF FF FF FF

00 7F FF 80 00

00 7F FF 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF C0 00 00 00 7F FF 80 00 00 00 00 00 00 00 00

FF C0 00 7F FF

FF FF FF FF FF

FF FF FF FF FF FF FF FF FF FF F0 03 FF F8 00 0F FF FF FF FF FF FF FF 80 07 FF FF FF FF FF FF FF FF FF FF F0 03 FF

00 00 00 00 00 3F 00 00 00 00 7F FF 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 40 00 7F FF

FF 80 00 00

FF FF FF FF 80 07 FF FF FF FF FF FF FF FF FF FF FF F0 01 FF FC 00 0F FF FF FF FF FF FF FF 80 00 00 00 00 00 00 00 00

FF FF FF FF FF

00 00 00 7F FC 00 07 FF E0 7F FC 00 00 00 00 00 07 FF FF FF FF FF FF FF 80 00 00 00 7F FC 00 07 FF E0 7F FE 00

FF FE 00 0F FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00 00 00 1F FF E0 01 FF FF 80 0F FF FF FF FF FF FF FE 00

F0 03 FF F0 00

FF 80 00 00 00 07

bg37.png

FF FF FF 7F

00 00 00 1F FF E0 00 FF FF C0 00 00 00 7F FF 80 00 00 00 00 00 00 00 00 00 00 00 00 3F FF E0 00 FF FF E0 00 00

03 FF C0 00 00

FF FF FF 00 07

FC 00 00 00 00 1F FE 00 00 00 00 07 FF FF FF FF FF FF FF FF FF FF F8 03 FF F8 00 00 00 00 7F FF 80 00 00 00 07 FF

00 00 00 00 00 00 00 00 00 00 00 7F FF C0 00 7F FF E0 00 00 00 7F FF 80 00 00 00 03 FF FF FF FF FF FF FF FF FF

00 00 00 00

FF FF FF FF F8 03 FF F8 00 00 00 00 7F FF 80 00 00 00 00 00 00 00 00 00 00 00 00 07 FF F8 03 FF F0 00 00 00 00 7F

80 00 00 00

F8 00 0F FF FF FF

E0 00 00 00 7F FF 80 00 00 00 07 FF FF FF FF FF FF FF FF FF FF 80 00 3F FF F0 00 00 00 7F FF 80 00 00 00 07 FF FF

00 3F FF E0 01

00 00 00 00 00 00 00 00 00 00 07 FF F0 03 FF F0 00 00 00 00 7F FF 80 00 00 00 00 00 00 00 00 00 00 00 00 07 FF

FF FF FF 00 00 1F FF F0 00 00 00 7F FF 80 00 00 00 07 FF FF FF FF FF FF FF FF FF FE 00 00 0F FF E0 00 00 00 7F

00 00 00 00 0F

FF FF FF FF FF FF FF FF FF F0 00 00 07 FF E0 00 00 00 7F FF 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

00 00 00 7F FF 80 00 00 00 00 00 00 00 00 00 00 00 00 07 FF F0 03 FF F0 00 00 00 00 7F FF 80 00 00 00 01 FF FF FF

00 00 00 00 00 00

bg9f.png

FF 80 00 00 00 3F FF F0 7F FE 00 03 FF F8 3F FF 80 00 07 FF F0 00 00 00 7F FF 80 00 00 00 3F FF F0 7F FE 00 03 FF

FF E0 7F FF

00 00 00 00 00 07 FF FF FF FE 01 FF F8 00 00 00 00 00 00 00 1F FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

00 00 7F FF 80

52

00 0F FF F8 00 00 00 7F FF 80 00 00 00 3F FF F0 7F FE 00 03 FF FC 3F FF 80 00 0F FF F8 00 00 00 7F FF 80 00 00 00

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

FE 00 07 FF F0 7F

FE 00 01 FF FC 1F FF C0 00 0F FF FC 00 00 00 7F FF 80 00 00 00 3F FF F0 7F FF 00 01 FF FC 1F FF C0 00 0F FF FC

FF F0 00 01 FF

1b 69 //Full tool command

80 00 00 00 3F FF F0 7F FF 00 01 FF FE 1F FF C0 00 0F FF FC 00 00 00 7F FF 80 00 00 00 3F FF F0 7F FF 00 01 FF

FF FE 00 1F FF E0

00 07 FF FF FF

F0 00 00 00 7F

0F FF F8 00 00 00 7F FF 80 00 00 00 3F FF F0 7F FF 80 01 FF FE 0F FF E0 00 0F FF F8 00 00 00 7F FF 80 00 00 00 1F

FF 80 00 00

F8 3F FF 80

Xiamen Dapu Electronic Technology Co., Ltd.

C0 01 FF FF 0F FF E0 00 0F FF F8 00 00 00 7F FF 80 00 00 00 0F FF C0 3F FF E0 03 FF FF 07 FF F0 00 07 FF F0 00

00 00 00 00 00

FF FF FF FF FF FF FF 80 01 FE 00 7F FE 00 07 FF E0 7F FE 00 00 00 00 00 0F FF FF FF FF FF FF FF 80 07 FF 80 7F

1A 5D 00 1A 4F 00 //Label printing end command

3F FF F0 7F

00 00 00 0F FF C0 3F FF FF FF FF FF 07 FF F0 00 03 FF F0 00 00 00 7F FF 80 00 00 00 03 FF 80 1F FF FF FF FF FF 87

FE 00 00 00 3F 00 0F FF FF FF FF FF FF FF 00 0F FF C0 7F FE 00 07 FF F0 7F FF 00 00 00 FF C0 0F FF FF FF FF FF

00 00 00 7F FF

E0 00 00 00 7F FF 80 00 00 00 01 FE 00 0F FF FF FF FF FF 83 FF F0 00 00 FF 80 00 00 00 7F FF 80 00 00 00 00 00

FF FF 83 FF F8 00 00 3E 00 00 00 00 7F FF 80 00 00 00 00 00 00 01 FF FF FF FF FF 83 FF F8 00 00 00 00 00 00 00 3F

7F FE 00 07 FF F0 7F FF 00 00 01 FF E0 00 00 00 7F FF 80 00 00 00 1F FF E0 7F FE 00 03 FF F8 3F FF 00 00 03 FF

FE 0F FF E0 00

bga0.png

1b 6D //Half knife command

Reverse printing: 1A 21 01 52 00 00 00 c8 00 c8 00 01, modified to 01
