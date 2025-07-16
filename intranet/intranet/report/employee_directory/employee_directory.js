// Copyright (c) 2025, hopeson and contributors
// For license information, please see license.txt

// employee_directory.js

frappe.query_reports["Employee Directory"] = {
  filters: [
    {
      fieldname: "employee_name",
      label: "Employee Name",
      fieldtype: "Data",
      reqd: 0,
    }
  ]
};
