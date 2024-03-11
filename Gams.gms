sets
j vessel /v1*v6/
i berth /1*3/
alias(j,jp)
;

parameter
a(j) /v1 0,v2 0,v3 0,v4 0,v5 0,v6 0/
w(j) /v1 4,v2 1,v3 4,v4 4,v5 8,v6 2/
p(j) /v1 6,v2 9,v3 7,v4 6,v5 8,v6 13/
M /9999/
H(j) /v1 1,v2 2,v3 2,v4 3,v5 2,v6 1/
L(j) /v1 1,v2 3,v3 3,v4 3,v5 3,v6 1/
T /12/
;

variable z;

binary variables x(i,j),II(i,j,jp);
positive variable s(j);

equations
obj
eq1
eq2
eq3
eq4
eq5
eq6
eq7
;

obj .. z=e=sum(j,w(j)*(s(j)+p(j)-a(j)));

eq1(j) .. sum(i,x(i,j))=e=1;

eq2(j) .. s(j)=g=a(j);

eq3(i,j,jp)$(ord(j)<>ord(jp)) .. s(jp)=g=s(j)+p(j)-m*(1-II(i,j,jp));

eq4(i,j,jp)$(ord(j)<ord(jp)) .. II(i,j,jp)+II(i,jp,j)=l=.5*(x(i,j)+x(i,jp));

eq5(i,j,jp)$(ord(j)<ord(jp)) .. II(i,j,jp)+II(i,jp,j)=g=x(i,j)+x(i,jp)-1;

eq6(i,j)$(ord(i)<=H(j)-1) .. x(i,j)=e=0;

eq7(i,j)$(ord(i)<=L(j)-1) .. s(j)=g=T*x(i,j);

model B1 /all/;

option mip=cplex,optca=0,optcr=0;

solve B1 using mip min z;

display z.l,x.l,II.l,s.l;