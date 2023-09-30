class FoodCard {
    constructor(category, singlepeople, manypeople, cheap, expensive, breakfast, lunch, dinner, night, hot, cold, activate) {
        this.category = category;
        this.singlepeople = singlepeople;
        this.manypeople = manypeople;
        this.cheap = cheap;
        this.expensive = expensive;
        this.breakfast = breakfast;
        this.lunch = lunch;
        this.dinner = dinner;
        this.night = night;
        this.hot = hot;
        this.cold = cold;
        this.activate = activate;
    }
}


const container = [];


function showContainer() {
    const containerH = document.getElementById('container');
    for (const foodCard of container) {
        const card = document.createElement('div');
        card.className = 'card';

        const category = document.createElement('h2');
        category.textContent = foodCard.category;


        //狂加Checkbox以及Event
        const peopleField = document.createElement('div');

        createCheckBox('一人', peopleField, 'singlepeople', foodCard);
        createCheckBox('多人', peopleField, 'manypeople', foodCard);

        const moneyField = document.createElement('div');

        createCheckBox('便宜', moneyField, 'cheap', foodCard);
        createCheckBox('昂貴', moneyField, 'expensive', foodCard);

        const mealField = document.createElement('div');

        createCheckBox('早', mealField, 'breakfast', foodCard);
        createCheckBox('午', mealField, 'lunch', foodCard);
        createCheckBox('晚', mealField, 'dinner', foodCard);
        createCheckBox('宵', mealField, 'night', foodCard);

        const seasonField = document.createElement('div');

        createCheckBox('只能夏', seasonField, 'hot', foodCard);
        createCheckBox('只能冬', seasonField, 'cold', foodCard);


        card.appendChild(category);
        card.appendChild(peopleField);
        card.appendChild(moneyField);
        card.appendChild(mealField);
        card.appendChild(seasonField);



        const delBtn = document.createElement('button');
        delBtn.textContent = '刪除卡片';
        delBtn.addEventListener("click", () => {
            const result = confirm(`確定刪除「${foodCard.category}」？`);
            if (result) {
                container.splice(container.indexOf(foodCard), 1);
                clearShow();
                showContainer();
            }
        })
        card.appendChild(delBtn);


        const hideBtn = document.createElement('button');
        if (foodCard.activate === 1) {
            card.classList.remove('disabled');
            hideBtn.textContent = '隱藏';
        } else {
            card.classList.add('disabled');
            hideBtn.textContent = '啟動';
        }

        hideBtn.addEventListener("click", () => {
            if (hideBtn.textContent === '隱藏') {
                card.classList.add('disabled');
                foodCard.activate = 0;
                hideBtn.textContent = '啟動'
            } else {
                card.classList.remove('disabled');
                foodCard.activate = 1;
                hideBtn.textContent = '隱藏';
            }
        })
        card.appendChild(hideBtn);


        containerH.append(card);

    }
}


function createCheckBox(label, field, instance, foodCard) {
    const check = document.createElement('input');
    check.setAttribute('type', 'checkbox');
    if (foodCard[instance] === 1) {
        check.checked = true;
    }

    check.addEventListener("change", () => {
        foodCard[instance] = (foodCard[instance] + 1) % 2;
    })

    const checkLabel = document.createElement('label');
    checkLabel.textContent = label;

    field.appendChild(checkLabel);
    field.appendChild(check);
}


function clearShow() {
    const containerH = document.getElementById('container');
    containerH.innerHTML = '';
}


//先把資料庫中的物件變成卡片丟上去
async function populate() {
    const request = new Request(get_food_url);
    const response = await fetch(request);
    const foods = await response.json();

    addToContainer(foods);
    showContainer();
}


function addToContainer(foods) {
    for (const food of foods) {
        const foodCard = new FoodCard(
            category = food.category,
            singlepeople = food.singlepeople,
            manypeople = food.manypeople,
            cheap = food.cheap,
            expensive = food.expensive,
            breakfast = food.breakfast,
            lunch = food.lunch,
            dinner = food.dinner,
            night = food.night,
            hot = food.hot,
            cold = food.cold,
            activate = food.activate);
        container.push(foodCard);
    }
}



const addBtn = document.getElementById('add');
addBtn.addEventListener("click", () => {
    const newCategory = prompt('食物名稱');

    if (newCategory !== null) {
        if (newCategory === '') {
            alert('不能為空');
        } else if (checkIfRepeat(newCategory)) {
            const foodCard = new FoodCard(
                category = newCategory,
                singlepeople = 1,
                manypeople = 0,
                cheap = 1,
                expensive = 0,
                breakfast = 0,
                lunch = 1,
                dinner = 1,
                night = 0,
                hot = 0,
                cold = 0,
                activate = 1);
            container.unshift(foodCard);
            clearShow();
            showContainer();
        }
        else {
            alert(`「${newCategory}」已經存在`);
        }

    }
})


function checkIfRepeat(name) {
    for (const foodCard of container) {
        if (name === foodCard.category) {
            return false;
        }
    }
    return true;
}

const saveBtn = document.getElementById('save');
saveBtn.addEventListener("click", () => {
    let data = new FormData;
    data.append("foodCards", JSON.stringify(container));


    fetch(save_food_url, {
        "method": "POST",
        "body": data,
    }).then(
        response => {
            if (response.redirected) {
                window.location = response.url
            } else {
                alert("一些錯誤提示")
            }
        }
    )
})

populate();