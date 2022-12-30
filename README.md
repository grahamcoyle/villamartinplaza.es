# VILLAMARTIN PLAZA
#### Video Demo:  https://youtu.be/hZjoFgA6xVo
#### Description:
Villamartin Plaza is a booking enquiry app for holiday rentals at an apartment in Villamartín Plaza Spain. It is a responsive mobile-first python web app using Flask framework, HTML, CSS and JavaScript. It also utilizes, Bootstrap, AJAX, a sprinkling of jQuery and a Sqlite3 database.

#### **Homepage - navbar**
The homepage is the user's first experience of the site-wide bootstrap navbar that collapses to a hamburger on smaller screens. In order to employ the .active class to highlight the current page, extra coding was required for the nav-links in the Fask template layout.html to check the endpoint and determine the active page. Here is an example using 'Photos' nav-link:
```
<li class="nav-item">
    <a {% if request.endpoint == 'photos' %} class="nav-link active" aria-current="true" {% else %} class="nav-link" {% endif %}
        href="/photos"> Photos </a>
```

#### **Homepage - logo**
The apartment is located on the sunny Costa Blanca surrounded by palm trees so the palm tree and sun logo was chosen along with the pale blue 'sky' as navbar background. The logo was also used as the favicon. The logo acts as a nav-link to return the user to the homepage. Originally all the nav-links were going to be graphical buttons but after I decided to add a call to action in the form of a big red 'Book Now!' button I decided to leave the simple nav-links so as not to make the navbar too busy.

#### **Homepage - weather**
The home page is essentially an 'about' page with a few photos and some information about the Plaza, plus a google location map (implemented as an iframe). Most people visit Spain because of the sunny weather so I added the maximum temperature of the day just below the page title in red. It is retrieved using [openweathermap.org API](https://openweathermap.org/api) with it's key stored as an [environment variable](#Environment-variables).

#### **Photos - carousel**
Beyond the red 'Book Now!' button, the first nav-link is 'Photos'. This made sense because property websites rely on good photography to entice users and so this this is arguably the most important page of the app. I employed Bootstrap carousel and adjusted the CSS using viewport height and width to allow both landscape and portrait photos to be displayed in full on all size screens:
```
 img {
   margin-left: auto;
   margin-right: auto;
   width: auto;
   max-width: 90vw;
   height: auto;
   max-height: 90vh;
 }
 ```

#### **360° Tour - iframe**
The next page is a 360 degree tour taken with a panoramic camera and accessed via an iframe. Using the photgrapher's hyperlink, it was ultimately very simple to implement as an iframe, but adds significant functionality for the user by allowing them to move around the apartment and even the Plaza itself! I did add CSS so that when a mobile screen is turned to landscape the 360° tour becomes fullscreen using: `@media screen and (orientation:landscape) and (max-width:1024px)`

#### **Extras - AJAX**
The navbar next links to extras.html; a page where the user can browse through a choice of optional extras using a dropdown menu. This page employs AJAX (jQuery method) to dynamically update the page depending on the user’s selection without reloading the whole page. This page can be expanded with other optional extras easily and is a great way to upsell. At the moment the selection includes ‘Airport transfers’, ‘Chilled beer’ and ‘Romantic collection’, the content of each being a jpeg, basic explanation and a price, although the Romantic collection has a pretty animated gif – again a picture paints a thousand words!

#### **Contact - Flask Mail**
The next nav-link is to a basic Bootstrap contact form containing fields for name, email address and message (limited to 255 characters). There are no labels as placeholders suffice to direct the user, with asterisks to indicate required fields (they are all required). A simple bot captcha has been added by including a hidden ‘subject’ field. If any data is submitted in this field then the whole submission is disregarded and the ‘user’ is returned to the homepage. Beyond front–end validation there is also basic server-side validation in the app.py file. Upon validated submission of the form, the app uses Flask Mail to send me an email containing the form data, which I receive immediately so can act on in a timely manner. The user is routed to a page that tells them their message has been sent.

#### **Activities - dropdown**
The navbar itself then has an ‘activities’ dropdown menu from which the user can choose things to do in the area. Currently this is restricted to the main things like; Golf, Beach, Shopping and Karting. Again this section could be readily expanded to include many other things to do nearby. The menu links the user to the relevant HTML page containing photos and text and where appropriate, hyperlinks to 3rd party sites that open in separate browser tabs. The photos are arranged as polaroids with white border on sides and bottom, a little shadowing and the text on the bottom border. I like the way this looks particularly on mobile screens. The same poloroid format was used on the homepage photos.

#### **Book Now! - content**
The call-to-action is the big red “Book Now!” button. This links to an HTML page with a table showing the rates and then another form with name, email, phone and a daterangepicker.  Client and server-side validation is also present as per the Contact form and again there is also a hidden subject field to act a bot captcha. This booking enquiry form also has hidden fields for telephone number verification and arrival and departure dates (taken from the daterangepicker). The 'phone' field is optional whereas the others are all required. The 'phone' field includes a country code drop down menu with flags of the countries. A GeoIP JavaScript function that uses [InfoIP API](https://infoip.io/) should automatically set the country flag to the users location. If this fails the default has been set to Spain and the initial choices to those countires from where most users are likely to originate.

#### **Book Now! - telephone validation**
If a telephone number is entered then validation takes place using the [International Telephone Input](https://intl-tel-input.com/) JavaScript plugin combined with [Twilio's Lookup API](https://www.twilio.com/blog/validate-phone-number-input). It is basic (free) and not foolproof but sufficient to catch obvious user input errors without asking for more input from the user. The function returns the number in E.164 format which is then entered to the hidden verification field on the form which is then passed to the app.py when the form is submitted.

#### **Book Now! - daterangepicker**
A JavaScript [daterangepicker](https://www.daterangepicker.com/) was chosen to provide a quick and intuitive way for users to select arrival and departure dates. The python app imports the datetime library to determine the current date then converts the format to an easier to read D MMM Y (eg 5 Jun 2022) format. The minimum rental period is 3 days but unfortunately the daterangepicker does not facilitate a minimum range but at least the intial endDate is set to 3 days from today (using Python's timedelta). The maximum range (dateLimit) is 1 month and the furthest into the future (maxDate) that the user may book is 1 year. These dates are calculated and reformatted in app.py before being passed to Flask placeholders in the daterangepicker function. The picker also blocks out all past dates. The jQuery attribute parameter was added to the function so that upon load there was no date selection in the form field, but instead a placeholder telling the user to "select dates*":
```
  $('input[name="daterange"]').val("");
  $('input[name="daterange"]').attr("placeholder", "select dates*");
 ```

#### **Book Now! - availability calendar**
Finishing up this page is a responsive calendar that syncs availability from external icals (eg airbnb). Unfortunaley this is a one-way sync at the moment so any bookings taken via this app would need to be manually updated on airbnb’s availability calendar. The calendar is provided by [Availcalendar](https://www.availcalendar.com/) and their intention is to provide 2-way sync functionality in the near future. It would also be better to integrate the daterangepicker with the availability calendar to automatically prevent users from selecting unavailable dates.

#### **Database**
Functionality-wise after submitting a valid form, the data is again emailed to me immediately (and the user is again routed to a message sent page) but the booking enquiry is also saved into a sqlite3 database called bookings.db and into a table called enquiries. The data saved is name, email address, phone number (if submitted), arrival date, departure date and the date of submission as well as an autogenerated unique ID as primary key for each submission. This information could prove useful for future marketing campaigns.

#### **Environment variables**
The third-party APIs used by this app are all free and the API keys are not hugely sensitive but environment variables have been used for the mail settings in particular. If the facility to sync availability 2-ways and a payment gateway were to be added then payments could be taken securely and fully automatically without fear of double bookings.