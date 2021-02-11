#include "base.h"

int main() {

	init(8192, 0, 8192);
	globals[0];
	
	int index = 0;

	goto endfor1;

for1:

	debug_reg(globals[0]);

	
	push(globals[0]);
	push(iconst(1));
	pop(r1);
	pop(r2);
	iadd(r1,r2,r1);
	globals[0]=r1;
	push(r1);
	pop(r1);
	goto endfor1;

endfor1:
	if (index==0) {	
	push(globals[0]);
	push(iconst(0));;
	index++;
	}
	push(globals[0]);
	push(iconst(10));
	pop(r1);
	pop(r2);
	ilt(r1,r2,r1);
	push(r1);
	pop(r1);
	if(asbool(r1)) goto for1;

	goto endfor2;

for2:

	debug_reg(globals[0]);

	
	push(globals[0]);
	push(iconst(2));;
	pop(r1);
	pop(r2);
	iadd(r1,r2,r1);
	globals[0]=r1;
	push(r1);
	pop(r1);
	goto endfor2;

endfor2:
	push(globals[0]);
	push(iconst(20));
	pop(r1);
	pop(r2);
	ilt(r1,r2,r1);
	push(r1);
	pop(r1);
	if(asbool(r1)) goto for2;

	return 0; 
 }
