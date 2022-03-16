function showPass() {
  var x = document.getElementById("password");
  var y = document.getElementById("repassword");
  if (x.type === "password") {
    x.type = "text";
    y.type = "text";
  } else {
    x.type = "password";
    y.type = "password";
  }
}
