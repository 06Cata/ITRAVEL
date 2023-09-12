const taiwanCities = [
    '基隆市', '新北市', '台北市', '桃園市', '新竹市', '新竹縣', '苗栗縣',
    '台中市', '彰化縣', '南投縣', '雲林縣', '嘉義市', '嘉義縣', '台南市',
    '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣', '金門縣', '連江縣'
];

const citiesContainer = document.querySelector('#cities-container');

taiwanCities.forEach(city => {
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = city;
    checkbox.name = 'location';
    checkbox.value = city;

    const label = document.createElement('label');
    label.htmlFor = city;
    label.classList.add('checkbox-label');
    label.textContent = city;

    citiesContainer.appendChild(checkbox);
    citiesContainer.appendChild(label);
});

