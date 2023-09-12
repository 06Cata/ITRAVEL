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

// 這裡面你有特別愛吃的嗎選項
const cuisineContainer = document.querySelector('#cuisine-container');
const cuisines = ['火鍋', '燒烤', '中式', '義式', '泰式', '日式', '韓式', '越南菜', '墨西哥菜', '其他'];

cuisines.forEach(cuisine => {
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.id = cuisine;
  checkbox.name = 'cuisine';
  checkbox.value = cuisine;

  const label = document.createElement('label');
  label.htmlFor = cuisine;
  label.textContent = cuisine;

  cuisineContainer.appendChild(checkbox);
  cuisineContainer.appendChild(label);
});

// 你可以接受的價位選項
const priceContainer = document.querySelector('.price-container');
const prices = [
  { label: '低價位(1-200)', value: '1-200' },
  { label: '中價位(200-400)', value: '200-400' },
  { label: '高價位(400up)', value: '400up' }
];

prices.forEach(price => {
  const radio = document.createElement('input');
  radio.type = 'radio';
  radio.id = `price-${price.value}`;
  radio.name = 'price';
  radio.value = price.value;

  const label = document.createElement('label');
  label.htmlFor = `price-${price.value}`;
  label.textContent = price.label;

  priceContainer.appendChild(radio);
  priceContainer.appendChild(label);
});

// 你追求熱門美食嗎

const hotFoodContainer = document.getElementById('hot-food-container');

const hotFoodOptions = [
  { label: '是', value: 'yes' },
  { label: '否', value: 'no' }
];

hotFoodOptions.forEach(option => {
  const radio = document.createElement('input');
  radio.type = 'radio';
  radio.id = `hot-food-${option.value}`;
  radio.name = 'hot-food';
  radio.value = option.value;

  const label = document.createElement('label');
  label.htmlFor = `hot-food-${option.value}`;
  label.textContent = option.label;

  hotFoodContainer.appendChild(radio);
  hotFoodContainer.appendChild(label);
});

// 其他需求選項
const requirementsContainer = document.querySelector('#requirements-container');
const requirements = ['親子餐廳', '寵物友善'];

requirements.forEach(requirement => {
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.id = requirement;
  checkbox.name = 'requirement';
  checkbox.value = requirement;

  const label = document.createElement('label');
  label.htmlFor = requirement;
  label.textContent = requirement;

  requirementsContainer.appendChild(checkbox);
  requirementsContainer.appendChild(label);
});

// 表單提交處理
const form = document.querySelector('#form');
const finishButton = document.querySelector('#finish-button');

form.addEventListener('submit', function(event) {
  event.preventDefault();

  const ratingValue = document.querySelector('input[name="rating"]:checked').value;
  const cuisineValues = Array.from(document.querySelectorAll('input[name="cuisine"]:checked')).map(input => input.value);
  const priceValue = document.querySelector('input[name="price"]:checked').value;
  const popularFoodValue = document.querySelector('#popularFood').checked;
  const requirementValues = Array.from(document.querySelectorAll('input[name="requirement"]:checked')).map(input => input.value);
  const whateverValue = document.querySelector('#whatever').checked;

  // 執行相應的處理或導向下一頁
  // ...

  console.log('在意住宿的程度:', ratingValue);
  console.log('這裡面你有特別愛吃的嗎:', cuisineValues);
  console.log('你可以接受的價位:', priceValue);
  console.log('你追求熱門美食嗎:', popularFoodValue);
  console.log('其他需求:', requirementValues);
  console.log('隨便啦:', whateverValue);
});