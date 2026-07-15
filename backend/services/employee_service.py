# Mock employee data — mirrors mock-database.md
# Will be replaced with real DB queries in Step 17

EMPLOYEES = {
    "EMP001": {"employee_id": "EMP001", "name": "Raj Sharma", "department": "Engineering", "email": "raj.sharma@techcorp.com", "manager": "EMP010", "location": "Mumbai"},
    "EMP002": {"employee_id": "EMP002", "name": "Priya Patel", "department": "Human Resources", "email": "priya.patel@techcorp.com", "manager": "EMP011", "location": "Bangalore"},
    "EMP003": {"employee_id": "EMP003", "name": "Amit Verma", "department": "Finance", "email": "amit.verma@techcorp.com", "manager": "EMP012", "location": "Delhi"},
    "EMP004": {"employee_id": "EMP004", "name": "Sneha Iyer", "department": "Marketing", "email": "sneha.iyer@techcorp.com", "manager": "EMP010", "location": "Mumbai"},
    "EMP005": {"employee_id": "EMP005", "name": "Rohan Mehta", "department": "Engineering", "email": "rohan.mehta@techcorp.com", "manager": "EMP010", "location": "Pune"},
    "EMP006": {"employee_id": "EMP006", "name": "Kavya Nair", "department": "Marketing", "email": "kavya.nair@techcorp.com", "manager": "EMP010", "location": "Mumbai"},
    "EMP007": {"employee_id": "EMP007", "name": "Arjun Das", "department": "Finance", "email": "arjun.das@techcorp.com", "manager": "EMP012", "location": "Delhi"},
    "EMP008": {"employee_id": "EMP008", "name": "Meera Joshi", "department": "Human Resources", "email": "meera.joshi@techcorp.com", "manager": "EMP011", "location": "Bangalore"},
    "EMP009": {"employee_id": "EMP009", "name": "Siddharth Rao", "department": "Engineering", "email": "siddharth.rao@techcorp.com", "manager": "EMP010", "location": "Pune"},
    "EMP010": {"employee_id": "EMP010", "name": "Vikram Nair", "department": "Engineering", "email": "vikram.nair@techcorp.com", "manager": "EMP020", "location": "Mumbai"},
    "EMP011": {"employee_id": "EMP011", "name": "Deepa Rao", "department": "HR Lead", "email": "deepa.rao@techcorp.com", "manager": "EMP020", "location": "Bangalore"},
    "EMP012": {"employee_id": "EMP012", "name": "Suresh Kumar", "department": "Finance Lead", "email": "suresh.k@techcorp.com", "manager": "EMP020", "location": "Delhi"},
    "EMP020": {"employee_id": "EMP020", "name": "Anita Desai", "department": "CTO", "email": "anita.desai@techcorp.com", "manager": None, "location": "Mumbai"},
}


def get_employee_info(employee_id: str) -> dict:
    """Look up an employee by ID."""
    employee = EMPLOYEES.get(employee_id.upper())
    if not employee:
        return {"error": f"Employee {employee_id} not found. Please verify the ID."}
    return employee