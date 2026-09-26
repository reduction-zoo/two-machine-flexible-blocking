# Prepared contract

Source input is `{"weights":[positive_integer,...]}`. A positive output `{"subset":[index,...]}` names distinct indices whose weights sum to half the total. Otherwise output `{"status":"NO-SOLUTION"}`.

Target input is `{"jobs":[{"first":p1,"middle":[[p_M1,p_M2],...],"last":p2},...],"deadline":D}` with positive integer processing times and nonnegative integer deadline. Each job has a mandatory first operation on machine 1, zero or more flexible middle operations in order, and a mandatory last operation on machine 2. A split `s_j` assigns the first `s_j` middle operations to machine 1 and the rest to machine 2. A positive output `{"order":[job,...],"splits":[s_by_job,...]}` chooses a common order on both machines and splits whose earliest two-machine no-wait/blocking makespan is at most `D`. `NO-SOLUTION` means no order and splits meet the deadline.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.
