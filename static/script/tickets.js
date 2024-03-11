submitButton = document.getElementById("submit");
submitButton.addEventListener("click", updateUrl);
function updateUrl() {
  //Go back yo page one
  window.history.pushState({}, "", "/search/tickets?page=1");
}
