module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace TwoMachineFlexibleBlocking

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

/-- Relational version for witnesses with quantified real or optimality conditions. -/
def relationalOutput {I W : Type} (legal : I → Bool) (witness : I → W → Prop)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w
  | none => legal x = true ∧ ¬ ∃ w, witness x w

def legalSource (x : List Nat) : Bool := x.all (fun w => w > 0)

def sourceWitness (x : List Nat) (subset : List Nat) : Bool :=
  decide subset.Nodup && subset.all (fun i => i < x.length) &&
  2 * (subset.map (fun i => x[i]?.getD 0)).sum == x.sum

def encodeSource := encodeList encodeNat

def validSourceOutput := searchOutput legalSource sourceWitness

structure Job where
  first : Nat
  middle : List (Nat × Nat)
  last : Nat
  deriving Repr
abbrev Instance := List Job × Nat
def legalTarget (x : Instance) : Bool := x.1.all (fun j =>
  j.first > 0 && j.last > 0 && j.middle.all (fun p => p.1 > 0 && p.2 > 0))
def durations (j : Job) (split : Nat) :=
  (j.first + ((j.middle.take split).map Prod.fst).sum,
   j.last + ((j.middle.drop split).map Prod.snd).sum)
def completion (times : List (Nat × Nat)) : Nat :=
  (times.foldl (fun prior p =>
    let secondStart := max (prior.1+p.1) prior.2
    (secondStart,secondStart+p.2)) (0,0)).2
def targetWitness (x : Instance) (w : List Nat × List Nat) : Bool :=
  decide (w.1.Perm (List.range x.1.length)) && w.2.length == x.1.length &&
  (x.1.zip w.2).all (fun (j,s) => s ≤ j.middle.length) &&
  completion (w.1.map (fun i => durations (x.1[i]?.getD ⟨0,[],0⟩) (w.2[i]?.getD 0))) ≤ x.2
def encodeTarget (x : Instance) :=
  encodeList (fun j => encodeNat j.first ++ encodeList (fun p => encodeNat p.1 ++ encodeNat p.2) j.middle ++ encodeNat j.last) x.1 ++ encodeNat x.2
def encodeWitness (w : List Nat × List Nat) := encodeList encodeNat w.1 ++ encodeList encodeNat w.2
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : (List Nat) → Instance)
    (recover : (List Nat) × Option (List Nat × List Nat) → Option (List Nat)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption encodeWitness) input.2)
    (encodeOption (encodeList encodeNat)) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList encodeNat)) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption encodeWitness) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))


def Goal : Prop :=
  ∃ (forward : (List Nat) → Instance)
    (recover : (List Nat) × Option (List Nat × List Nat) → Option (List Nat)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end TwoMachineFlexibleBlocking
