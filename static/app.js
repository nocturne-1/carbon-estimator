// Accessing form elements and labels
let activity = document.getElementById("activity");

let electricity_activity_label = document.getElementById("elecactivity");
let electricity_activity = document.getElementById("electricity_activity");
let duration_label = document.geetElementById("timing");
let duration = document.getElementById("duration");

let passengers_flight_label = document.getElementById("people_flight");
let passengers_flight =  document.getElementById("passengers");
let departure_label = document.getElementById("leaving");
let departure = document.getElementById("departure");
let arrival_label = document.getElementById("returning");
let arrival = document.getElementById("arrival");

let transport_type_label = document.getElementById("moving_type");
let transport_type = document.getElementById("transport_type");
let passengers_ground_label = document.getElementById("people-ground");
let passengers_ground = document.getElementById("passengers_ground");
let distance_transport_label = document.getElementById("distance_ground");
let distance_transport = document.getElementById("distance_transport");

let rating_label = document.getElementById("stars");
let rating = document.getElementById("rating");
let nights_label = document.getElementById("days");
let nights = document.getElementById("nights");

let restaurant_type_label = document.getElementById("eating_type");
let restaurant_type = document.getElementById("restaurant_type");
let spent_label = document.getElementById("money");
let spent = document.getElementById("spent");

let electricity_question_list = [
    [electricity_activity_label, electricity_activity], 
    [duration_label, duration]
];
let flight_question_list = [
    [passengers_flight_label, passengers_flight], 
    [departure_label, departure], 
    [arrival_label, arrival]
];
let transportation_question_list = [
    [transport_type_label, transport_type],
    [passengers_ground_label, passengers_ground],
    [distance_transport_label, distance_transport]
];

let accommodation_question_list = [
    [rating_label, rating],
    [nights_label, nights]
];

let restaurant_question_list = [
    [restaurant_type_label, restaurant_type],
    [spent_label, spent]
];

const makeVisible = (label, element) => {
    label.classList.add("make_visible");
    element.classlist.add("make_visible");
}

activity.addEventListener("change", () => {
    if (activity.value == "electricity") {
        for (let i = 0; i < electricity_question_list.length; i++) {
            makeVisible(i[0], i[1]);
        }
    }

    else if (activity.value == "flight") {
        for (let i = 0; i < flight_question_list.length; i++) {
            makeVisible(i[0], i[1]);
        }
    }

    else if (activity.value == "transportation") {
        for (let i = 0; i < transportation_question_list.length; i++) {
            makeVisible(i[0], i[1]);
        }
    }

else if (activity.value == "accommodation") {
    for (let i = 0; i < accommodation_question_list.length; i++) {
        makeVisible(i[0], i[1]);
        }
    }

else if (activity.value == "restaurant") {
    for (let i = 0; i < restaurant_question_list.length; i++) {
        makeVisible(i[0], i[1]);
    }
    }
})
