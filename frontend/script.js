const form = document.getElementById("expense-form");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    console.log("Form submitted!");
});