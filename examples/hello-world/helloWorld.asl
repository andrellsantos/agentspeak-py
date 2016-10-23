/* Agent helloWorld in project helloWorld.aslpy */

/* Initial beliefs and rules */

/* Initial goals */
!start_function.

/* Plans */
+!start_function : true <- aloha; ?start_print(true); !start_print.
+!start_print : true <- .print("Formas de imprimir a base de conhecimento:"); .print(); .print(""); !start_variable(andre).
+!start_variable(A) : true <- mahalo(A).