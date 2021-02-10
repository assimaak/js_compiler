#include "base.h"

int main() {

	init(8192, 0, 8192);
	globals[0] = iconst(0);


iftest1:
	push(globals[0]);
	push(iconst(0));
	pop(r1);
	pop(r2);
	ieq(r1,r2,r1);
	lneg(r1,r1);
	push(r1);
	pop(r1);
	if(asbool(r1)) {
		printf("iftrue1\n");
	push(globals[0]);
	push(iconst(1));
	pop(r1);
	pop(r2);
	iadd(r1,r2,r1);
	globals[0]=r1;
	push(r1);

	pop(r1);
	debug_reg(r1);
	}

	else {
		printf("iffalse1\n");
	push(globals[0]);
	push(iconst(1));
	pop(r1);
	pop(r2);
	iadd(r1,r2,r1);
	globals[0]=r1;
	push(r1);

	pop(r1);
	debug_reg(r1);
	}


iftest2:
	push(globals[0]);
	push(iconst(1));
	pop(r1);
	pop(r2);
	ieq(r1,r2,r1);
	push(r1);
	pop(r1);
	if(asbool(r1)) {
	printf("iftrue2\n");
	push(globals[0]);
	push(iconst(2));;
	pop(r1);
	pop(r2);
	isub(r1,r2,r1);
	globals[0]=r1;
	push(r1);

	pop(r1);
	debug_reg(r1);
	}


	goto endwhile1;

while1:
	push(globals[0]);
	push(iconst(1));
	pop(r1);
	pop(r2);
	iadd(r1,r2,r1);
	globals[0]=r1;
	push(r1);

	pop(r1);
	debug_reg(r1);

	goto endwhile1;

endwhile1:
	push(globals[0]);
	push(iconst(10));
	pop(r1);
	pop(r2);
	ilt(r1,r2,r1);
	push(r1);
	pop(r1);
	if(asbool(r1)) goto while1;

	return 0;
 }
