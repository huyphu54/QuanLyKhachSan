
function formatDate() {
  var inputDate = document.getElementById("checkin_date").value;
  var formattedDate = new Date(inputDate).toISOString().split('T')[0].replace(/-/g, '/');
  document.getElementById("checkin_date").value = formattedDate;

