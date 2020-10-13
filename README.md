# Discovery of Relations by Analogy

## Overview

DORA (Discovery of Relations by Analogy) is a cognitive model of relational learning. DORA is capable of representing multi-place relationships f(a,b,c..) where a,b,c.. are the arguments. Such a multiplace relationship containing n arguments can be represented as embedded binary relationships

For example, consider the proposition - "Karthikeya works at the MPI". Relationally, "Karthikeya" and "the MPI" are connected by the predicate "works at". Therefore, we can represent the proposition as works(Karthikeya, MPI), with the implicit assumption that the predicate "works" takes as its first argument the worker, and second argument, the place of work. Clearly, this is a multiplace relationship (n>1), and can be decomposed into two binary relationships with a way to connect them : worker(Karthikeya), place(MPI) represent the binary relationships (Of course this alone is insufficient to define works(Karthikeya, MPI)). What we now need is a way to combine these binary relationships - bind(worker(Karthikeya), place(MPI)) == works(Karthikeya, MPI). How DORA does this will be explained shortly. The important point however, is that all propositions rest on the structural relationships between their elements to derive "meaning". Maintaining these relationships as binary predicate-argument pairs becomes necessary if one assumes that "meaning" emerges from the interaction of the atomic elements. Therefore every binary predicate-argument pair has a limited, but essential value. We now see what architectural features DORA possesses to preserve this value.

## Features and Architecture

Propositions in DORA are represented across four layers, termed the P, RB, PO, and semantic units. We first look at how each proposition in DORA is encoded (ie., the microarchitecture), and then understand how the encoding of individual propositions relates to how an entire knowledge base is represented in DORA (ie., the macro-architecture).




The bottom-most layer is the semantic layer and it acts as the perceptual layer connecting the real world to DORA. This is done via representing entities as distributed features, which are commonly accessible to all the units in the layer above it.


## Flow of control


## Dataset and representation

## Results

