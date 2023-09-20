// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.
@R14
D = M
@R15
D = D + M
// D = D -1
@end
M = D

@R14
D = M
@min
M = D
@max
M = D

@R14
D = M
@i
M = D

(LOOP)
@i
D = M
@end
D = D - M
@SWAP
D;JGE

@i
A = M
D = M
@min
A = M
D = D - M
@UPDATEMIN
D;JLT

@i
A = M
D = M
@max
A = M
D = D - M
@UPDATEMAX
D;JGT


(AFTERUPDATE)

@i
M = M + 1

@LOOP
0;JMP


(UPDATEMIN)
@i
D = M
@min //min holds adress of min
M = D

@AFTERUPDATE
0;JMP

(UPDATEMAX)
@i
D = M
@max //max holds adress of min
M = D

@AFTERUPDATE
0;JMP

(SWAP)
@min
A = M
D = M

@temp
M = D 

@max
A = M 
D = M 

@min 
A = M 
M = D 


@temp
D = M

@max
A = M 
M = D 


(FINNISH)
@FINNISH
0;JMP
