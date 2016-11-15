/* Agent poster in project poster.maspy */

/* Initial beliefs and rules */

/* Initial goals */
!start.

/* Plans */
+!start : true <- aloha; ?continue(execute); !run(agentspeak).
+!run(A) : true <- mahalo(A).