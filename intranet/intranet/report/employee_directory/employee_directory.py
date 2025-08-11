# employee_directory.py

import frappe

def execute(filters=None):
    columns = [
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 160},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 150},
        {"label": "Date of Joining", "fieldname": "date_of_joining", "fieldtype": "Date", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
        {"label": "Mobile Number", "fieldname": "cell_number", "fieldtype": "Data", "width": 120},
        {"label": "Company Email", "fieldname": "company_email", "fieldtype": "Data", "width": 180},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Data", "width": 110},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 150},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 150},
    ]

    filters_dict = {"status": ["!=", "Left"]}

    if filters and filters.get("employee_name"):
        filters_dict["employee_name"] = ["like", f"%{filters['employee_name']}%"]

    data = frappe.get_all(
        "Employee",
        fields=[
            "employee_name", "company", "department", "designation", "branch",
            "bio", "date_of_joining", "status", "cell_number",
            "personal_email", "company_email"
        ],
        filters=filters_dict,
        order_by="employee_name"
    )

    return columns, data
