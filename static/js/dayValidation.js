
console.log("date is working {{ order.status }}");
if("{{ order.status }}" == "pending"){

   
      // e.g., "2024-07-28"
    var djangoDate = new Date(djangoDateString);
    var differenceInMillis =djangoDate - currentDate;

    // Convert milliseconds to days
    var differenceInDays = differenceInMillis / (1000 * 60 * 60 * 24);

    remainDate=Math.round(differenceInDays);

    // Compare the dates
    if (currentDate.toDateString() === djangoDate.toDateString()) {
        days.innerText="today";
    } else if (currentDate > djangoDate) {
        days.innerText="over";
    } else {
        days.innerText=remainDate+"days left";
    }
    if(remainDate>0)
    {
        document.getElementById("updateStatus").addEventListener("submit", function(event) {
            // Display the confirmation dialog
            var userConfirmed = confirm("Are you sure you want to delivery today?\nstill "+remainDate+"days left");

            // If the user clicks "Cancel", prevent form submission
            if (!userConfirmed) {
                event.preventDefault();  // Prevents the form from being submitted
            }
        });
    }
}