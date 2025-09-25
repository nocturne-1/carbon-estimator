//Set variables
const submitBtn = document.getElementById("submitForm");
const user = document.getElementById("name");
var activity = document.getElementById("activity");
var actvalue = activity.value;
var acttext = activity.options[activity.selectedIndex].text;

var elecActivity = document.getElementById("electricity_activity");
var eavalue = elecActivity.value; 
var eatext = elecActivity.options[elecActivity.selectedIndex].text;
const duration = document.getElementById("duration");
const coutry = document.getElementById("country");
const state = document.getElementById("state");

const departure = document.getElementById("departure");
const destination = document.getElementById("destination");
const cabinClass = document.getElementById("cabin_class");
const parcelWeight = document.getElementById("parcel_weight");
var shippingZone = document.getElementById("shipping_zone")
var shipValue = shippingZone.value;
var shipText = shippingZone.options[shippingZone.selectedIndex].text;

const shippedFrom = document.getElementById("warehouse_loc")
const shippedTo = document.getElementById("current_loc")

const vehicleMake = document.getElementById("vehicle_make")
const vehicleModel = document.getElementById("vehicle_model")
const distanceTraveled = document.getElementById("distance")

// Set dict for energy used by common appliances
const electricActivities = {
    "Portable Heater": 1.5, 
    "A/C (Window/Wall)": 1.2, 
    "AC (Central)": 3, 
    "Ceiling Fan": 0.075, 
    "Oven": 2.3,
    "Dishwasher": 2, 
    "Refrigerator": 2, 
    "TV": 0.14, 
    "Desktop PC": 0.15, 
    "Laptop": 0.05,
    "Monitor": 0.06,
}

//Calculate energy used total in kWh

// Use GeoCode API to geocode places & get coordinates
// Calculate distance between places with Leaflet

// Send Carbon Interface API Request with parameters from Above

// For Vehicle, send Vehicle Make and Model API Requests
// Then send Carbon Interface API Request using vehicle_id

//Store User Data in Firebase