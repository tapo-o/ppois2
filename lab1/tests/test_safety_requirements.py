from src.SafetyRequirements import SafetyRequirements


def test_safety_recheck():
    sr = SafetyRequirements()
    assert sr.is_pass is False

    sr.recheck(True)
    assert sr.is_pass is True

    sr.recheck(False)
    assert sr.is_pass is False

    sr.recheck(1)      # должно привести к True
    assert sr.is_pass is True

    sr.recheck(0)
    assert sr.is_pass is False