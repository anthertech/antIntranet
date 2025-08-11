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
};


  function handleBreadcrumb() {
  const current_route = frappe.get_route().join('/');

  // Check your actual route via console.log() to match exactly
  if (current_route === 'query-report/Employee Directory') {
    if (!$('.custom-breadcrumb').length) {
      setTimeout(() => {
        $('<div class="custom-breadcrumb" style="padding: 5px 15px; font-size: 14px; white-space: nowrap;">' + 
          '<a href="/app/home">Home</a> / <span>Employee Directory</span>' + 
          '</div>').insertAfter('.navbar-brand');
      }, 200); // small delay ensures navbar already rendered
    }
  } else {
    $('.custom-breadcrumb').remove();
  }
}

// Listen to route changes
frappe.router.on('change', () => {
  handleBreadcrumb();
});

// Run once on initial load (refresh)
$(document).ready(function() {
  handleBreadcrumb();
});
