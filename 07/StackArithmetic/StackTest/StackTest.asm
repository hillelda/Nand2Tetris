// Push constant17
@17
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant17
@17
D = A
@SP
M = M + 1
A = M - 1
M = D
// eq
@SP
AM = M - 1
D = M
@SP
A = M - 1
D = D - M
@TRUE_JEQ1
D;JEQ
@SP
A = M - 1
M = 0
@CONTINUE1
0;JMP
(TRUE_JEQ1)
@SP
A = M - 1
M = -1
(CONTINUE1)
// Push constant17
@17
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant16
@16
D = A
@SP
M = M + 1
A = M - 1
M = D
// eq
@SP
AM = M - 1
D = M
@SP
A = M - 1
D = D - M
@TRUE_JEQ2
D;JEQ
@SP
A = M - 1
M = 0
@CONTINUE2
0;JMP
(TRUE_JEQ2)
@SP
A = M - 1
M = -1
(CONTINUE2)
// Push constant16
@16
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant17
@17
D = A
@SP
M = M + 1
A = M - 1
M = D
// eq
@SP
AM = M - 1
D = M
@SP
A = M - 1
D = D - M
@TRUE_JEQ3
D;JEQ
@SP
A = M - 1
M = 0
@CONTINUE3
0;JMP
(TRUE_JEQ3)
@SP
A = M - 1
M = -1
(CONTINUE3)
// Push constant892
@892
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant891
@891
D = A
@SP
M = M + 1
A = M - 1
M = D
// lt
@SP
M = M - 1
A = M
D = M
@R13
M = D
@SP
A = M - 1
D = M
@R14
M = D
@TOP_VALUE_POSITIVE4
D;JGE
@R13
D = M
@REGULAR4
D;JLE
@TRUE_JL4
0;JMP
(TOP_VALUE_POSITIVE4)
@R13
D = M
@FALSE_JL4
D;JLT
(REGULAR4)
@R14
D = M - D
@TRUE_JT4
D;JLT
(FALSE_JL4)
@SP
A = M - 1
M = 0
@CONTINUE4
0;JMP
(TRUE_JL4)
@SP
A = M - 1
M = -1
(CONTINUE4)
// Push constant891
@891
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant892
@892
D = A
@SP
M = M + 1
A = M - 1
M = D
// lt
@SP
M = M - 1
A = M
D = M
@R13
M = D
@SP
A = M - 1
D = M
@R14
M = D
@TOP_VALUE_POSITIVE5
D;JGE
@R13
D = M
@REGULAR5
D;JLE
@TRUE_JL5
0;JMP
(TOP_VALUE_POSITIVE5)
@R13
D = M
@FALSE_JL5
D;JLT
(REGULAR5)
@R14
D = M - D
@TRUE_JT5
D;JLT
(FALSE_JL5)
@SP
A = M - 1
M = 0
@CONTINUE5
0;JMP
(TRUE_JL5)
@SP
A = M - 1
M = -1
(CONTINUE5)
// Push constant891
@891
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant891
@891
D = A
@SP
M = M + 1
A = M - 1
M = D
// lt
@SP
M = M - 1
A = M
D = M
@R13
M = D
@SP
A = M - 1
D = M
@R14
M = D
@TOP_VALUE_POSITIVE6
D;JGE
@R13
D = M
@REGULAR6
D;JLE
@TRUE_JL6
0;JMP
(TOP_VALUE_POSITIVE6)
@R13
D = M
@FALSE_JL6
D;JLT
(REGULAR6)
@R14
D = M - D
@TRUE_JT6
D;JLT
(FALSE_JL6)
@SP
A = M - 1
M = 0
@CONTINUE6
0;JMP
(TRUE_JL6)
@SP
A = M - 1
M = -1
(CONTINUE6)
// Push constant32767
@32767
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant32766
@32766
D = A
@SP
M = M + 1
A = M - 1
M = D
// gt
@SP
M = M - 1
A = M
D = M
@R13
M = D
@SP
A = M - 1
D = M
@R14
M = D
@TOP_VALUE_POSITIVE7
D;JGE
@R13
D = M
@REGULAR7
D;JLE
@FALSE_JT7
0;JMP
(TOP_VALUE_POSITIVE7)
@R13
D = M
@TRUE_JT7
D;JLT
(REGULAR7)
@R14
D = M - D
@TRUE_JT7
D;JGT
(FALSE_JT7)
@SP
A = M - 1
M = 0
@CONTINUE7
0;JMP
(TRUE_JT7)
@SP
A = M - 1
M = -1
(CONTINUE7)
// Push constant32766
@32766
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant32767
@32767
D = A
@SP
M = M + 1
A = M - 1
M = D
// gt
@SP
M = M - 1
A = M
D = M
@R13
M = D
@SP
A = M - 1
D = M
@R14
M = D
@TOP_VALUE_POSITIVE8
D;JGE
@R13
D = M
@REGULAR8
D;JLE
@FALSE_JT8
0;JMP
(TOP_VALUE_POSITIVE8)
@R13
D = M
@TRUE_JT8
D;JLT
(REGULAR8)
@R14
D = M - D
@TRUE_JT8
D;JGT
(FALSE_JT8)
@SP
A = M - 1
M = 0
@CONTINUE8
0;JMP
(TRUE_JT8)
@SP
A = M - 1
M = -1
(CONTINUE8)
// Push constant32766
@32766
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant32766
@32766
D = A
@SP
M = M + 1
A = M - 1
M = D
// gt
@SP
M = M - 1
A = M
D = M
@R13
M = D
@SP
A = M - 1
D = M
@R14
M = D
@TOP_VALUE_POSITIVE9
D;JGE
@R13
D = M
@REGULAR9
D;JLE
@FALSE_JT9
0;JMP
(TOP_VALUE_POSITIVE9)
@R13
D = M
@TRUE_JT9
D;JLT
(REGULAR9)
@R14
D = M - D
@TRUE_JT9
D;JGT
(FALSE_JT9)
@SP
A = M - 1
M = 0
@CONTINUE9
0;JMP
(TRUE_JT9)
@SP
A = M - 1
M = -1
(CONTINUE9)
// Push constant57
@57
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant31
@31
D = A
@SP
M = M + 1
A = M - 1
M = D
// Push constant53
@53
D = A
@SP
M = M + 1
A = M - 1
M = D
// add
@SP
M = M - 1
A = M
D = M
@SP
A = M - 1
D = D + M
M = D
// Push constant112
@112
D = A
@SP
M = M + 1
A = M - 1
M = D
// sub
@SP
M = M - 1
A = M
D = M
@SP
A = M - 1
D = M - D
M = D
// neg
@SP
A = M - 1
M = - M
// and
@SP
M = M - 1
A = M
D = M
@SP
A = M - 1
D = D&M
M = D
// Push constant82
@82
D = A
@SP
M = M + 1
A = M - 1
M = D
// or
@SP
M = M - 1
A = M
D = M
@SP
A = M - 1
D = D|M
M = D
// neg
@SP
A = M - 1
M = !M
