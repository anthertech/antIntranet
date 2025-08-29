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

@frappe.whitelist(allow_guest=False)
def get_employee_events(start, end):
    user = frappe.session.user
    roles = frappe.get_roles(user)

    filters = {
        "starts_on": ["between", [start, end]]
    }
    # Add status field here!
    fields = ["subject", "starts_on", "status"]

    events = frappe.db.get_list(
        "Event",
        filters=filters,
        fields=fields,
        order_by="starts_on asc",
        limit_page_length=50,
        ignore_permissions=True if "Employee" in roles else False
    )
    return events


from frappe.utils import getdate

@frappe.whitelist(allow_guest=False)
def get_employee_holidays(start, end):
    user = frappe.session.user
    roles = frappe.get_roles(user)

    # Allow access if user has Employee or HR role
    if not ("Employee" in roles or "HR" in roles):
        return []

    employee = frappe.db.get_value("Employee", {"user_id": user}, ["company"], as_dict=True)
    if not employee:
        return []

    company_doc = frappe.get_doc("Company", employee["company"])
    holiday_list_name = company_doc.default_holiday_list
    if not holiday_list_name:
        return []

    holiday_list = frappe.get_doc("Holiday List", holiday_list_name, ignore_permissions=True)

    start_date = getdate(start)
    end_date = getdate(end)

    holidays = []
    for h in holiday_list.holidays:
        holiday_date = getdate(h.holiday_date)
        if start_date <= holiday_date <= end_date:
            holidays.append({
                "holiday_date": holiday_date,
                "description": h.description
            })

    return holidays


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
        "company",
        "status"  # ✅ Include status so frontend can also see it if needed
    ]

    filters = {"status": "Active"}  # ✅ Only Active employees

    if "Employee" in roles:
        employees = frappe.db.get_list(
            "Employee",
            fields=fields,
            filters=filters,
            order_by="employee_name asc",
            limit_page_length=1000,
            ignore_permissions=True
        )
    else:
        employees = frappe.get_list(
            "Employee",
            fields=fields,
            filters=filters,
            order_by="employee_name asc",
            limit_page_length=1000
        )

    return employees



@frappe.whitelist()
def get_open_jobs_basic(limit=10):
    location_img = '<img src="/assets/intranet/images/loc.png" width="19" height="20" style="vertical-align:middle; border-radius:50%; object-fit:cover;" />'
    jobs = frappe.get_all(
        "Job Opening",
        filters={"status": "Open"},
        fields=["name", "job_title", "employment_type", "location", "route", "publish"],
        limit_page_length=int(limit),
        order_by="posted_on desc"
    )
    result = []
    for job in jobs:
        parts = [job.get('job_title') or ""]
        if job.get('employment_type'):
            parts.append(
                f'<span style="display:inline-block; background:#e4f5e9; color:#16794c; border-radius:4px; padding:2px 8px; font-size:12px; margin-left:8px;">{job.get("employment_type")}</span>'
            )
        if job.get('location'):
            parts.append(
                f'<span style="display:inline-flex;  margin-left:8px;">'
                f'<span style="vertical-align:middle;">{location_img}</span>'
                f'<span style="background:#fff1e7; color:#bd3e0c; border-radius:4px; padding:2px 8px; font-size:12px; margin-left:4px;">{job.get("location")}</span>'
                f'</span>'
            )
        combined = " ".join([p for p in parts if p])
        route_path = job.get("route") or f"/app/job-opening/{job.get('name')}"
        if not route_path.startswith("/"):
            route_path = "/" + route_path
        if job.get("publish"):
            result.append({
                "info": combined,
                "route": route_path
            })
        else:
            result.append({
                "info": combined,
                "route": None
            })
    return {
        "count": len(result),
        "jobs": result
    }

