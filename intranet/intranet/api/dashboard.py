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




# import frappe

# @frappe.whitelist()
# def get_open_jobs_with_applicant_count(limit=10):
#     # Fetch open job openings
#     jobs = frappe.get_all("Job Opening",
#         filters={"status": "Open"},
#         fields=["name", "job_title", "designation", "department", "posted_on", "employment_type", "location", "closes_on"],
#         limit_page_length=int(limit),
#         order_by="posted_on desc"
#     )

#     # For each job, count applicants where job_title (in Job Applicant) matches job Opening's name (ID)
#     for job in jobs:
#         job['applicant_count'] = frappe.db.count("Job Applicant", {"job_title": job["name"]})

#     return jobs


import frappe
@frappe.whitelist()
def get_open_jobs_basic(limit=10):
    jobs = frappe.get_all(
        "Job Opening",
        filters={"status": "Open"},
        fields=["name", "job_title", "employment_type", "location", "route", "publish"],  # Added publish field
        limit_page_length=int(limit),
        order_by="posted_on desc"
    )

    result = []
    for job in jobs:
        parts = [job.get('job_title') or ""]
        if job.get('employment_type'):
            parts.append(f"💼 {job.get('employment_type')}")
        if job.get('location'):
            parts.append(f"📍 {job.get('location')}")
        combined = " | ".join([p for p in parts if p])

        # Ensure route starts from root `/`
        route_path = job.get("route") or f"/app/job-opening/{job.get('name')}"
        if not route_path.startswith("/"):
            route_path = "/" + route_path  # force root absolute

        # Make route/link only if 'publish' is checked
        if job.get("publish"):
            result.append({
                "info": combined,
                "route": route_path     # clickable (front end will treat as link)
            })
        else:
            result.append({
                "info": combined,
                "route": None           # not clickable (front end can render as plain text)
            })

    return {
        "count": len(result),
        "jobs": result
    }
