from check import legal_target,solve_target,valid_target


def test_hand_cases():
    one = {"jobs":[{"first":2,"middle":[],"last":3}],"deadline":5}
    assert valid_target(one,{"order":[0],"splits":[0]})
    assert solve_target({**one,"deadline":4}) == {"status":"NO-SOLUTION"}
    flexible = {"jobs":[{"first":1,"middle":[[1,5]],"last":1}],"deadline":3}
    assert valid_target(flexible,{"order":[0],"splits":[1]})
    assert not valid_target(flexible,{"order":[0],"splits":[0]})
    assert not legal_target({"jobs":[{"first":0,"middle":[],"last":1}],"deadline":1})


if __name__ == "__main__":
    test_hand_cases()
