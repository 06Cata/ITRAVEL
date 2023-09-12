// 在意程度選項
const ratingContainer = document.querySelector('.rating-container');
const ratings = [1, 2, 3, 4, 5];

ratings.forEach(rating => {
  const radio = document.createElement('input');
  radio.type = 'radio';
  radio.id = `rating-${rating}`;
  radio.name = 'rating';
  radio.value = rating;

  const label = document.createElement('label');
  label.htmlFor = `rating-${rating}`;
  label.textContent = rating;

  ratingContainer.appendChild(radio);
  ratingContainer.appendChild(label);
});

// 室內或室外選項
const indoorOutdoorContainer = document.querySelector('#indoor-outdoor-container');
const indoorOutdoorOptions = [
  { label: '室內', value: 'indoor' },
  { label: '室外', value: 'outdoor' }
];

indoorOutdoorOptions.forEach(option => {
  const radio = document.createElement('input');
  radio.type = 'radio';
  radio.id = `indoor-outdoor-${option.value}`;
  radio.name = 'indoor-outdoor';
  radio.value = option.value;

  const label = document.createElement('label');
  label.htmlFor = `indoor-outdoor-${option.value}`;
  label.textContent = option.label;

  indoorOutdoorContainer.appendChild(radio);
  indoorOutdoorContainer.appendChild(label);
});

// 表單提交處理
const form = document.querySelector('#form');
const finishButton = document.querySelector('#finish-button');

form.addEventListener('submit', function(event) {
  event.preventDefault();

  const ratingValue = document.querySelector('input[name="rating"]:checked').value;
  const indoorOutdoorValue = document.querySelector('input[name="indoor-outdoor"]:checked').value;

  console.log('在意程度:', ratingValue);
  console.log('偏好室內或室外:', indoorOutdoorValue);
});
