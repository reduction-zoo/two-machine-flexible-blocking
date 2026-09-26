"""Independent exact oracles for Partition and fixed-order Unanimous Vote."""

import argparse
import json
import subprocess
import sys
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path


def legal_source(source):
    return (isinstance(source, dict) and isinstance(source.get("weights"), list)
            and all(type(weight) is int and weight > 0 for weight in source["weights"]))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal Partition instance")
    weights = source["weights"]
    total = sum(weights)
    if total % 2:
        return {"status": "NO-SOLUTION"}
    for mask in range(1 << len(weights)):
        subset = [index for index in range(len(weights)) if mask & (1 << index)]
        if sum(weights[index] for index in subset) * 2 == total:
            return {"subset": subset}
    return {"status": "NO-SOLUTION"}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    subset = output.get("subset")
    weights = source["weights"]
    return (set(output) == {"subset"} and isinstance(subset, list)
            and all(type(index) is int and 0 <= index < len(weights) for index in subset)
            and len(set(subset)) == len(subset)
            and 2 * sum(weights[index] for index in subset) == sum(weights))


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"jobs","deadline"}:
        return False
    jobs,deadline = target["jobs"],target["deadline"]
    return (isinstance(jobs,list) and type(deadline) is int and deadline >= 0
            and all(isinstance(job,dict) and set(job) == {"first","middle","last"}
                    and type(job["first"]) is int and job["first"] > 0
                    and type(job["last"]) is int and job["last"] > 0
                    and isinstance(job["middle"],list)
                    and all(isinstance(pair,list) and len(pair) == 2
                            and all(type(time) is int and time > 0 for time in pair)
                            for pair in job["middle"]) for job in jobs))


def processing(job,split):
    return (job["first"]+sum(pair[0] for pair in job["middle"][:split]),
            job["last"]+sum(pair[1] for pair in job["middle"][split:]))


def makespan(target,order,splits):
    if not order:
        return 0
    durations = [processing(target["jobs"][job],splits[job]) for job in order]
    return durations[0][0]+sum(max(durations[i][0],durations[i-1][1])
                               for i in range(1,len(order)))+durations[-1][1]


def direct_schedule(target,order,splits):
    departure = completion = 0
    for job in order:
        first,second = processing(target["jobs"][job],splits[job])
        start_second = max(departure+first,completion)
        completion = start_second+second
        departure = start_second
    return completion


def direct_plan(target,order,splits):
    n = len(target["jobs"])
    return (isinstance(order,list) and len(order) == n
            and all(type(job) is int for job in order)
            and sorted(order) == list(range(n))
            and isinstance(splits,list) and len(splits) == n
            and all(type(split) is int and 0 <= split <= len(target["jobs"][i]["middle"])
                    for i,split in enumerate(splits))
            and direct_schedule(target,order,splits) <= target["deadline"])


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal flexible blocking instance")
    jobs = target["jobs"]
    outputs = []
    for order in permutations(range(len(jobs))):
        for splits in product(*(range(len(job["middle"])+1) for job in jobs)):
            if makespan(target,order,splits) <= target["deadline"]:
                output = {"order":list(order),"splits":list(splits)}
                assert direct_plan(target,output["order"],output["splits"])
                outputs.append(output)
                if len(outputs) >= limit:
                    return outputs
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return (set(output) == {"order","splits"}
            and direct_plan(target,output["order"],output["splits"]))


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for weights,expected in EDGE_CASES:
        assert ("subset" in solve_source({"weights":weights})) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        reachable = {0}
        for weight in source["weights"]:
            reachable |= {value+weight for value in reachable}
        total = sum(source["weights"])
        exists = total % 2 == 0 and total//2 in reachable
        assert ("subset" in current) == exists == ("subset" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    import random
    checks = 0
    for seed in range(100):
        rng = random.Random(seed)
        jobs = [{"first":rng.randint(1,4),
                 "middle":[[rng.randint(1,4),rng.randint(1,4)] for _ in range(rng.randint(0,2))],
                 "last":rng.randint(1,4)} for _ in range(rng.randint(1,4))]
        dummy = {"jobs":jobs,"deadline":0}
        all_times = []
        for order in permutations(range(len(jobs))):
            for splits in product(*(range(len(job["middle"])+1) for job in jobs)):
                fast = makespan(dummy,order,splits)
                direct = direct_schedule(dummy,order,splits)
                assert fast == direct
                all_times.append(direct)
        for bound,expected in ((min(all_times)-1,False),(min(all_times),True)):
            dummy["deadline"] = bound
            assert ("order" in solve_target(dummy)) == expected
            checks += 1
    print(f"Self-test passed: {len(cases)} source instances and {checks} exact scheduling thresholds")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
