#include "base.h"
#include <stdio.h>
int main() {

	init(8192, 0, 8192);
	globals[0] = iconst(10);
	
	goto functend_blob;

funct_blob:

	push(globals[0]);
	push(bp[3]);
	pop(r1);
	pop(r2);
	iadd(r1,r2,r1);
	push(r1);;
	globals[0]=r1;
	push(r1);

	pop(r1);
	debug_reg(r1);

	pop(r1);
	drop(0);
	ret(r1);
functend_blob:
	push(iconst(1));
	call(funct_blob);

	pop(r1);
	drop(0);
	debug_reg(r1);

	push(iconst(2));
	call(funct_blob);

	pop(r1);
	drop(0);
	debug_reg(r1);


	return 0; 
 }
