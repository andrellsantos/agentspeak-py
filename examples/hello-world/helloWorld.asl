/* Agent helloWorld in project helloWorld.aslpy */

/* Initial beliefs and rules */

/* Initial goals */
!start.
//!start2(andre).

/* Plans */

+!start : true <- aloha; .print("Formas de imprimir a base de conhecimento:"); .print(); .print("").

+!start2(A) : true <- mahalo(A).