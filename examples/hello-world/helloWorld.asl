/* Agent helloWorld in project helloWorld.aslpy */

/* Initial beliefs and rules */
p(c).
p1(c).
p2(c).
~p(c).
~p1(c).
~p2(c).

localizacao(lixeira, b).
~localizacao(lixeira, b).

hello(world).
~hello(world).

/* Initial goals */

!start.

/* Plans */

+!start : true <- aloha; .print("Formas de imprimir a base de conhecimento:"); .print(); .print("").