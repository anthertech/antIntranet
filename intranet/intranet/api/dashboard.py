import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)  # or remove `allow_guest` if only logged-in users should see it
def get_public_attendance():
    today = frappe.utils.today()
    thirty_days_later = frappe.utils.add_days(today, 30)

    records = frappe.get_all("Attendance",
        filters={
            "status": ["in", ["On Leave", "Work From Home"]],
            "attendance_date": [">=", today],
        },
        fields=["employee_name", "attendance_date", "status"],
        order_by="attendance_date asc",
        limit_page_length=100
    )

    return records



import frappe

@frappe.whitelist(allow_guest=False)  # only for logged-in users, safer than guests!
def get_public_tasks():
    task_statuses = ["Open", "Overdue", "Pending Review", "Working"]
    fields = ["name", "subject", "status", "project", "priority"]
    filters = {"status": ["in", task_statuses]}

    user = frappe.session.user
    roles = frappe.get_roles(user)

    # If the user has Employee role, override permissions and show all tasks
    if "Employee" in roles:
        tasks = frappe.db.get_list(
            "Task",
            filters=filters,
            fields=fields,
            order_by="priority desc",
            limit=100,
            ignore_permissions=True   # <-- THIS LINE OVERRIDES STANDARD PERMISSIONS
        )
    else:
        # For safety, restrict or fallback to normal permissions
        tasks = frappe.db.get_list(
            "Task",
            filters=filters,
            fields=fields,
            order_by="priority desc",
            limit=100
        )

    return tasks
import frappe

@frappe.whitelist(allow_guest=False)
def get_employee_events(start, end):
    user = frappe.session.user
    roles = frappe.get_roles(user)

    filters = {
        "starts_on": ["between", [start, end]]
    }
    fields = ["subject", "starts_on"]

    if "Employee" in roles:
        events = frappe.db.get_list(
            "Event",
            filters=filters,
            fields=fields,
            order_by="starts_on asc",
            limit_page_length=50,
            ignore_permissions=True
        )
    else:
        events = frappe.db.get_list(
            "Event",
            filters=filters,
            fields=fields,
            order_by="starts_on asc",
            limit_page_length=50
        )

    return events



import frappe

@frappe.whitelist(allow_guest=False)
def get_energy_point_logs(start_date=None, end_date=None):
    user = frappe.session.user
    roles = frappe.get_roles(user)

    filters = {}
    if start_date and end_date:
        filters["creation"] = ["between", [start_date, end_date]]

    fields = ["user", "points", "creation"]

    if "Employee" in roles:
        logs = frappe.db.get_list(
            "Energy Point Log",
            filters=filters,
            fields=fields,
            order_by="creation asc",
            limit_page_length=1000,
            ignore_permissions=True
        )
    else:
        logs = frappe.db.get_list(
            "Energy Point Log",
            filters=filters,
            fields=fields,
            order_by="creation asc",
            limit_page_length=1000
        )

    return logs




import frappe

@frappe.whitelist(allow_guest=False)  # Only logged-in users
def get_all_employee_details():
    user = frappe.session.user
    roles = frappe.get_roles(user)

    fields = [
        "name",
        "employee_name",
        "image",
        "date_of_birth",
        "date_of_joining",
        "designation",
        "company"
    ]

    if "Employee" in roles:
        # Employees see all Employee records, ignoring permission checks
        employees = frappe.db.get_list(
            "Employee",
            fields=fields,
            order_by="employee_name asc",
            limit_page_length=1000,
            ignore_permissions=True
        )
    else:
        # Other roles: default permission behavior applies
        employees = frappe.get_list(
            "Employee",
            fields=fields,
            order_by="employee_name asc",
            limit_page_length=1000
        )

    return employees




