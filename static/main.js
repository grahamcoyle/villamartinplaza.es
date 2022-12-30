// Ajax (extras.html)
function extras(extra)
 {
    // Deal with situation where nothing is chosen
    if (extra == "")
        return;
    // create new AJAX object
    var ajax = new XMLHttpRequest();
    // When page loaded have callback function pre-fill <div>
    ajax.onreadystatechange = function() {
        if (ajax.readyState == 4 && ajax.status == 200) {
            // JQuery way to do it
            $("#extrasdiv").html(ajax.responseText);
        }
    };
    // Open requested file and transmit data
    ajax.open("GET", extra, true);
    ajax.send();
}

// Phone number verification (book.html)
// Code from https://www.twilio.com/blog/validate-phone-number-input
// Detect Country IP to set country dialing code (flag)
function getIp(callback) {
  fetch('https://ipinfo.io/json?token=7806d8fb6e24eb', { headers: { 'Accept': 'application/json' }})
    .then((resp) => resp.json())
    .catch(() => {
      return {
        country: 'es',
      };
    })
    .then((resp) => callback(resp.country));
 }

// intl-tel-input initialization
const phoneInputField = document.querySelector("#phone");
const phoneInput = window.intlTelInput(phoneInputField, {
    initialCountry: "auto",
    geoIpLookup: getIp,
    preferredCountries: ["gb", "es", "fr", "ie", "no", "se", "de", "nl"],
    utilsScript:
    "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.19/js/utils.js",
});

function verify(event)
{
    event.preventDefault();
    const phoneNumber = phoneInput.getNumber();
    const data = new URLSearchParams();
    data.append("phone", phoneNumber);

    // My Twilio function URL
    fetch("https://intl-tel-input-4911.twil.io/lookup", {
      method: "POST",
      body: data,
    })
      // .then handles response
      .then((response) => response.json())
      .then((json) => {
        if (json.success)
        {
          document.querySelector("#verified").value = "verified";
          document.querySelector("#phone").value = phoneNumber
          document.querySelector("#book").submit();
        }
        else
        {
          document.querySelector("#verified").value = "";
          console.log(json.error);
          document.querySelector("#book").submit();
        }
      })
      // .catch handles error
      .catch((err) => {
        if (err != null)
        {
          document.querySelector("#verified").value = err.message;
          console.log(err.message);
          document.querySelector("#book").submit();
        }
      });
}