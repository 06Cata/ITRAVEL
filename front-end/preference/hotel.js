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

// 住宿偏好選項
const accommodationContainer = document.querySelector('#accommodation-container');
const accommodations = ['民宿', '輕旅/背包客棧', '星級飯店'];

accommodations.forEach(accommodation => {
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.id = accommodation;
  checkbox.name = 'accommodation';
  checkbox.value = accommodation;

  const label = document.createElement('label');
  label.htmlFor = accommodation;
  label.textContent = accommodation;

  accommodationContainer.appendChild(checkbox);
  accommodationContainer.appendChild(label);
});

// 其他需求選項
const requirementsContainer = document.querySelector('#requirements-container');
const requirements = ['SPA', '泳池', '溫泉', '停車場', '附早餐'];

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
const priceRange = document.querySelector('#price-range');
const priceValue = document.querySelector('#price-value');

// 監聽價格範圍拖動條的輸入事件
priceRange.addEventListener('input', function() {
  const formattedValue = formatNumberWithCommas(priceRange.value);
  priceValue.textContent = formattedValue;
});

// 格式化數字，加入逗號分隔
function formatNumberWithCommas(number) {
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// 監聽表單提交事件
form.addEventListener('submit', function(event) {
  event.preventDefault();

  const ratingValue = document.querySelector('input[name="rating"]:checked').value;
  const accommodationValues = Array.from(document.querySelectorAll('input[name="accommodation"]:checked')).map(input => input.value);
  const requirementValues = Array.from(document.querySelectorAll('input[name="requirement"]:checked')).map(input => input.value);
  const priceValue = priceRange.value;

  console.log('在意住宿的程度:', ratingValue);
  console.log('你有偏好哪一種嗎:', accommodationValues);
  console.log('其他需求:', requirementValues);
  console.log('最高可接受一晚的價錢:', priceValue);
});
