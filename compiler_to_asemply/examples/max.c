#include <stdio.h> 
void main() 
{
int a,b,c,d,T_1,T_2,T_3; 
L_0:  //(begin_block, max, , )
L_1: if (x > y) goto L_3; //(>, x, y, 3)
L_2: goto L_6; //(jump, , , 6)
L_3: return x; //(RETV, , , x)
L_4: goto L_8; //(jump, , , 8)
L_5: goto L_8; //(jump, , , 8)
L_6: return y; //(RETV, , , y)
L_7: goto L_8; //(jump, , , 8)
L_8: {} //(end_block, max, , )
L_9:  //(begin_block, MAX, , )
L_10: a=1; //(:=, 1, , a)
L_11: b=2; //(:=, 2, , b)
L_12: c=3; //(:=, 3, , c)
L_13: d=4; //(:=, 4, , d)
L_26: c=T_3; //(par, a, CV, )
L_27: printf("%d",c); //(par, b, CV, )
L_28:  //(par, T_1, RET, )
L_29: {} //(call, max, , )
}