const searchInput = document.getElementById('search-input');
const searchResultsContainer = document.getElementById('search-results');
const selectedPlacesContainer = document.getElementById('selected-places');

const MAX_PLACES = 10;
let selectedPlaces = [];

// 監聽輸入框的輸入事件
searchInput.addEventListener('input', handleSearchInput);

// 處理輸入框的輸入事件
function handleSearchInput() {
    const searchQuery = searchInput.value.trim();
    
    // 發送非同步請求到後端，獲取搜尋結果
    // 可以使用XMLHttpRequest、fetch或其他庫（如axios）來發送請求

    // 假設後端返回一個包含搜尋結果的陣列
    const searchResults = ['老串角居酒屋','Wood Bistro 木餐酒館', '傑仕堡有氧酒店', '酒師傅體驗館', ];

      // 清空搜尋結果容器
      searchResultsContainer.innerHTML = '';

      // 遍歷搜尋結果陣列，創建搜尋結果項並添加到搜尋結果容器
      searchResults.forEach(place => {
        const resultItem = document.createElement('div');
        resultItem.textContent = place;
        resultItem.classList.add('search-result');
        resultItem.addEventListener('click', () => selectPlace(place));
        searchResultsContainer.appendChild(resultItem);
      });
    }

// 選擇地點
function selectPlace(place) {
    // 檢查是否已達到最大選擇數量
    if (selectedPlaces.length >= MAX_PLACES) {
    alert('最多只能選擇' + MAX_PLACES + '個地點');
    return;
    }

    // 檢查地點是否已被選擇
    if (selectedPlaces.includes(place)) {
    alert('該地點已被選擇');
    return;
    }

    // 添加地點到已選擇列表
    selectedPlaces.push(place);

    // 創建已選擇地點的DOM元素
    const listItem = document.createElement('li');
    listItem.innerHTML = `
    <span class="selected-place-name">${place}</span>
    <span class="remove-button" data-place="${place}">✖</span>
    `;

    // 添加移除按鈕的點擊事件
    const removeButton = listItem.querySelector('.remove-button');
    removeButton.addEventListener('click', () => removePlace(place));

    // 添加已選擇項目到已選擇列表容器
    selectedPlacesContainer.appendChild(listItem);

    // 清空搜尋框和搜尋結果
    searchInput.value = '';
    searchResultsContainer.innerHTML = '';
}

// 移除地點
function removePlace(place) {
    // 在已選擇列表中移除地點
    selectedPlaces = selectedPlaces.filter(p => p !== place);

    // 從DOM中移除地點項
    const listItem = selectedPlacesContainer.querySelector(`[data-place="${place}"]`).parentElement;
    listItem.remove();
}