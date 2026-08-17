from core.Result import Result

def test_result_success():
    res = Result.success("test_data")
    assert res.is_success is True
    assert res.value == "test_data"
    assert res.error is None

def test_result_failure():
    res = Result.failure("Something went wrong")
    assert res.is_success is False
    assert res.value is None
    assert res.error == "Something went wrong"
