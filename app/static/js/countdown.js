
var wedding = new Date('July 3, 2016 15:00:00');

var toSeconds = 1000;
var toMinutes = toSeconds*60;
var toHours = toMinutes*60;
var toDays = toHours*24;

days = $('#days')
hrs = $('#hrs');
min = $('#min');
sec = $('#sec');

function getDifference(wedding) {
  var current = new Date();
  var difference = wedding - current;
  var seconds = Math.floor(difference/toSeconds)%60;
  var minutes = Math.floor(difference/toMinutes)%60;
  var hours = Math.floor(difference/toHours)%24;
  var days = Math.floor(difference/toDays);
  return {
    days: days,
    hours: hours,
    minutes: minutes,
    seconds: seconds
  }
}

function showTime() {
  time = getDifference(wedding);
  days.text(time.days);
  hrs.text(time.hours);
  min.text(time.minutes);
  sec.text(time.seconds);
  requestAnimationFrame(showTime);
}

requestAnimationFrame(showTime);