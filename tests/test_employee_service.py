from backend.services.employee_service import get_employee_info


def test_get_existing_employee():
    result = get_employee_info("EMP001")
    assert result["name"] == "Raj Sharma"
    assert result["department"] == "Engineering"
    assert result["email"] == "raj.sharma@techcorp.com"
    assert result["location"] == "Mumbai"


def test_get_employee_case_insensitive():
    result = get_employee_info("emp001")
    assert result["name"] == "Raj Sharma"


def test_get_nonexistent_employee_returns_error():
    result = get_employee_info("EMP999")
    assert "error" in result


def test_all_employees_have_required_fields():
    from backend.services.employee_service import EMPLOYEES
    required = {"employee_id", "name", "department", "email", "location"}
    for emp_id, emp in EMPLOYEES.items():
        for field in required:
            assert field in emp, f"{emp_id} missing field: {field}"
