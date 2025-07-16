# employee_directory.py

import frappe

def execute(filters=None):
    columns = [
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 160},
        {"label": "Company", "fieldname": "company", "fieldtype": "Data", "width": 150},
        {"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 150},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Data", "width": 150},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Data", "width": 110},
        {"label": "Bio", "fieldname": "bio", "fieldtype": "Small Text", "width": 250},
        {"label": "Date of Joining", "fieldname": "date_of_joining", "fieldtype": "Date", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 90},
        {"label": "Cell Number", "fieldname": "cell_number", "fieldtype": "Data", "width": 120},
        {"label": "Personal Email", "fieldname": "personal_email", "fieldtype": "Data", "width": 180},
        {"label": "Company Email", "fieldname": "company_email", "fieldtype": "Data", "width": 180},
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
