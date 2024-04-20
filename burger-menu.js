function toggleMenu() {
    var menuPopup = document.querySelector('#menuPopup');
    menuPopup.classList.toggle('visible');
}
let attractions=[];

document.addEventListener('DOMContentLoaded', function(){
    fetch('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1')
    .then(function(response){
        return response.json();
    })
    .then(data =>{
        attractions = data.data.results;
        let promoContainer = document.querySelector('.promotion')
        let bigBoxContainer = document.querySelector('.bigbox-container')

        //在這裡清空容器，避免重複內容
        while (promoContainer.firstChild) {
            promoContainer.removeChild(promoContainer.firstChild);
        }
        while (bigBoxContainer.firstChild) {
            bigBoxContainer.removeChild(bigBoxContainer.firstChild);
        }
        

        for (let i=0; i<3; i++){
            let spot = attractions[i];
            let element = createSpotElement(spot, 'promo-item');   //function後面設置
            promoContainer.appendChild(element);
        }

        for (let i=3; i<13; i++){
            let spot = attractions[i];
            let element = createSpotElement(spot, 'bigframe');   //function後面設置
            bigBoxContainer.appendChild(element);
        }
    })
    .then(() => {
        // 確保數據已經加載完成後才添加事件監聽器
        document.querySelector('.learn_more_button').addEventListener('click', function() {
            let bigBoxContainer = document.querySelector('.bigbox-container');
            let currentContentCount = bigBoxContainer.children.length;
            let maxContent = attractions.length;
        
            for (let i = currentContentCount; i < currentContentCount + 10 && i < maxContent; i++) {
                let spot = attractions[i];
                let element = createSpotElement(spot, 'bigframe');
                bigBoxContainer.appendChild(element);
            }
            updateBigFrames();
        });
    });
});

function updateBigFrames() {
    let frames = document.querySelectorAll('.bigbox-container .bigframe');
    const screenWidth = window.innerWidth;

    // 先重置所有元素的 gridColumn 设置
    frames.forEach(frame => frame.style.gridColumn = "");

    if (screenWidth <= 600) {
        // 0-600px: 每个元素占满一整行
        frames.forEach(frame => frame.style.gridColumn = "1fr");
    } else if (screenWidth > 600 && screenWidth <= 1200) {
        // 601-1200px: 每四个元素一行，均匀分布，不跨列
        frames.forEach(frame => frame.style.gridColumn = "auto");
    } else {
        // 1201px 及以上: 每6个元素一行，第1个和每隔5个后的第1个元素跨两列
        frames.forEach((frame, index) => {
            if (index % 5 === 0) {
                frame.style.gridColumn = "span 2";
            }
        });
    }
}




function createSpotElement(spot, className){
    let spotDiv = document.createElement('div');
    spotDiv.className = className

    let img = document.createElement('img');
    let imageUrls = spot.filelist.split('https');
    if (imageUrls.length > 1) {
        // 轉換所有URL為小寫再處理，並找到第一個.jpg出現的位置
        let imageUrl = 'https' + imageUrls[1];
        imageUrl = imageUrl.toLowerCase(); 
        let jpgIndex = imageUrl.indexOf('.jpg'); 
        if (jpgIndex !== -1) {
            img.src = imageUrl.substring(0, jpgIndex + 4); // 包含.jpg四個字
        }
    }
    img.alt = '這是景點';
    img.className = className === 'promo-item' ? 'promo-img' : 'bigboximg';

    // 只有smallbox 裡面才用到span
    if (className === 'promo-item'){
        let promoText = document.createElement('span')
        promoText.textContent = spot.stitle;
        promoText.className = 'promo-text';
        spotDiv.appendChild(promoText);
    }

    // 只有當類別是 'bigframe' 時才加button
    if (className === 'bigframe') {
        let button = document.createElement('button');
        button.textContent = spot.stitle;
        button.className = 'text-block';
        spotDiv.appendChild(button);
    }

    spotDiv.appendChild(img);
    
    
    if (className === 'bigframe') {
        let starIcon = document.createElement('img');
        starIcon.src = 'star.png';
        starIcon.alt = 'image';
        starIcon.className = 'star-icon';
        spotDiv.appendChild(starIcon);
    }

    return spotDiv;
    
}