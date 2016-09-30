/* Agent helloWorld in project helloWorld.aslpy */

/* Initial beliefs and rules */
hello(world).
~hello(world).

/* Initial goals */

!start.

/* Plans */

+!start : true <- aloha; .print("Formas de imprimir a base de conhecimento:"); .print(); .print("").