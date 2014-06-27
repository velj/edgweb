var scoreinput = document.getElementById("scoreinput");
//validate the client side if the value is 1-15
//alert(scoreinput);
scoreinput.addEventListener("blur", function (event) {
  if(scoreinput.validity.patternMismatch) {
    scoreinput.setCustomValidity("");
  } else {
    scoreinput.setCustomValidity("");

  }
});


