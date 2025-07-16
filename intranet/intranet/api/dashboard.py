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
