
import frappe

def is_hrms_app_installed():
    """Check if HRMS app is installed on the current site."""
    installed_apps = frappe.get_installed_apps()
    return "hrms" in installed_apps  # match your HRMS app name exactly

def before_app_install(app_name):
    """Runs before installing an app — stops if HRMS is missing."""
    if app_name == "intranet":
        if not is_hrms_app_installed():
            raise Exception("Installation aborted: HRMS app must be installed first.")
    return