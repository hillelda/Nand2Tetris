// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// Multiplies R0 and R1 and stores the result in R2.
//
// Assumptions:
// - R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.
// - You can assume that you will only receive arguments that satisfy:
//   R0 >= 0, R1 >= 0, and R0*R1 < 32768.
// - Your program does not need to test these conditions.
//
// Requirements:
// - Your program should not change the values stored in R0 and R1.
// - You can implement any multiplication algorithm you want.

// Put your code here.
@R2
M = 0
@R0
D = M
@R3
M = D
(LOOP)
    // check if i=0;
    @R3
    D = M
    @EXIT
    D;JLE

    // add R1 to R2, reduce R3 by one
    @R1
    D = M
    @R2
    M = M + D
    @R3
    M = M -1
    @LOOP
    0;JMP


(EXIT)
    @EXIT
    0;JMP
