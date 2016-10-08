/* Agent helloWorld in project helloWorld.aslpy */

/* Initial beliefs and rules */

p(c).
p1(c).
p2(c).
~p(c).
~p1(c).
~p2(c).

localizacao(lixeira, b).

hello(world).
~hello(world).

/* Initial goals */


!start.
!start1.
!start2.
!g(t).
!g1(t).
!g2(t).
!~g(t).
!~g1(t).
!~g2(t).

/* Plans */

+!start : true <- .print("hello world.").
+!start : true <- .print().

+locked(door) : true
  <- .send(porter,achieve,~locked(door)). // ask porter to unlock the door
 
//-locked(door) : true
//  <- .print("Thanks for unlocking the door!").

+!locked(door) //[source(paranoid)]
  : ~locked(door)
  <- lock.

+!locked(door)
  : ~locked(door)
  <- lock.
  
+!~locked(door) //[source(claustrophobe)]
  : locked(door)
  <- unlock.
  
+!~locked(door)
  : locked(door)
  <- unlock.
  
+~locked(door) : true
  <- .send(porter,achieve,locked(door)). // ask porter to lock the door

//+locked(door) : true
//  <- .print("Thanks for locking the door!").

+p(a) : true <- act; .print("Noticed p(a).").

+~p(a) : true <- act; .print("Noticed ~p(a).").

+p(b) : p(a) & ~p(a) <- act; .print("Noticed p(b) and contradiction.").

+p(b) : not p(a) & not ~p(a) <- act; .print("Noticed p(b) and lack of information.").

+p(b) : true <- act; .print("Noticed p(b) and nothing else special.").

+~p(b) : p(a) & ~p(a) <- act; .print("Noticed ~p(b) and contradiction.").

+~p(b) : not p(a) & not ~p(a) <- act; .print("Noticed ~p(b) and lack of information.").

+~p(b) : true <- act; .print("Noticed ~p(b) and nothing else special.").

