class BlackCard {
    constructor(name) {
        this.name = name;
    }
}

const container = [];


//先把資料庫中的物件變成卡片丟上去
async function populate() {
    const request = new Request(get_black_url);
    const response = await fetch(request);
    const blacks = await response.json();

    addToContainer(blacks);
    showContainer();
}





function addToContainer(blacks) {
    for (const black of blacks) {
        const blackCard = new BlackCard(black.name);
        container.push(blackCard);
    }
}

function showContainer() {
    const containerH = document.getElementById('container');
    for (const blackCard of container) {
        const card = document.createElement('div');
        card.className = 'card';

        const name = document.createElement('h2');
        name.textContent = blackCard.name;

        card.appendChild(name);


        const delBtn = document.createElement('button');
        delBtn.textContent = '刪除詞彙';
        delBtn.addEventListener("click", () => {
            const result = confirm(`確定刪除「${blackCard.name}」？`);
            if (result) {
                container.splice(container.indexOf(blackCard), 1);
                clearShow();
                showContainer();
            }
        })
        card.appendChild(delBtn);




        containerH.appendChild(card);
    }
}


function clearShow() {
    const containerH = document.getElementById('container');
    containerH.innerHTML = '';
}

const addBtn = document.getElementById('add');
addBtn.addEventListener("click", () => {
    const newName = prompt('黑名單');

    if (newName !== null) {
        if (newName === '') {
            alert('不能為空');
        } else if (checkIfRepeat(newName)) {
            const blackCard = new BlackCard(newName);
            container.unshift(blackCard);
            clearShow();
            showContainer();
        }
        else {
            alert(`「${newName}」已經存在`);
        }

    }
})


function checkIfRepeat(name) {
    for (const blackCard of container) {
        if (name === blackCard.name) {
            return false;
        }
    }
    return true;
}


const saveBtn = document.getElementById('save');
saveBtn.addEventListener("click", () => {
    let data = new FormData;
    data.append("blackCards", JSON.stringify(container));


    fetch(save_black_url, {
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