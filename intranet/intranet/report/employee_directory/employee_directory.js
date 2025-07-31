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
  ],
  onload: function(report) {
    if (!$('.custom-breadcrumb').length) {
      $('.page-head').prepend(`
        <div class="custom-breadcrumb" style="margin-bottom:10px; float: right; margin-right: 15px; white-space: nowrap;">
          <a href="/app/home">Home</a> / <span>Employee Directory</span>
        </div>
      `);
    }
  }
};




