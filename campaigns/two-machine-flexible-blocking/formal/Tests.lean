import Challenge
open TwoMachineFlexibleBlocking
example : targetWitness ([⟨2,[],1⟩,⟨1,[],2⟩],4) ([0,1],[0,0]) = false := by native_decide
example : targetWitness ([⟨2,[],1⟩,⟨1,[],2⟩],4) ([1,0],[0,0]) = true := by native_decide
