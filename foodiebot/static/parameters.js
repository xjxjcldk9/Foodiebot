const directSearchBtn = document.getElementById("directSearchBtn");
const directSearch = document.getElementById("directSearch");

const otherParamsBtn = document.getElementById("otherParamsBtn");
const otherParams = document.getElementById("otherParams");

const people = document.getElementById('people');

//先隱藏參數
directSearch.style.display = "none";
otherParams.style.display = "none";

//若無登入則不顯示按鈕
if (!login) {
    otherParamsBtn.style.display = "none";
    directSearchBtn.style.display = "none";
}


directSearchBtn.addEventListener("click", () => {
    if (directSearch.style.display === "none") {
        directSearch.style.display = "block";
        directSearchBtn.classList.add("pure-button-active");
        people.style.display = "none";
    } else {
        directSearch.style.display = "none";
        directSearchBtn.classList.remove("pure-button-active");
        people.style.display = "block";
    }
})

otherParamsBtn.addEventListener("click", () => {
    if (otherParams.style.display === "none") {
        otherParams.style.display = "block";
        otherParamsBtn.classList.add("pure-button-active");
    } else {
        otherParams.style.display = "none";
        otherParamsBtn.classList.remove("pure-button-active");
    }
})



const cheap = document.getElementById("cheap");
const expensive = document.getElementById("expensive");

const singlepeople = document.getElementById("singlepeople");
const manypeople = document.getElementById("manypeople");

const open = document.getElementById("open");

const star = document.getElementById("star");
const starOutput = document.getElementById("starOutput");

const manual = document.getElementById("manual");

//確保不會都沒勾到
cheap.addEventListener("click", () => {
    if (!cheap.checked && !expensive.checked) {
        expensive.checked = true;
    }
});

expensive.addEventListener("click", () => {
    if (!cheap.checked && !expensive.checked) {
        cheap.checked = true;
    }
});

singlepeople.addEventListener("click", () => {
    if (!singlepeople.checked && !manypeople.checked) {
        manypeople.checked = true;
    }
});


manypeople.addEventListener("click", () => {
    if (!singlepeople.checked && !manypeople.checked) {
        singlepeople.checked = true;
    }
});



starOutput.textContent = star.value;
star.addEventListener("input", (event) => {
    starOutput.textContent = event.target.value;
});





//Send POST

const postButton = document.getElementById('postButton');
postButton.addEventListener('click', () => {

    if (myLocation == null) {
        alert("請標註地點");
    }
    else {
        const loader = document.createElement('div')
        loader.className = 'Loader'
        postButton.parentElement.appendChild(loader);



        let data = new FormData;
        let parameters = {};
        parameters.location = { 'lat': myLocation.lat(), 'lng': myLocation.lng() };
        //這邊是公尺
        parameters.radius = radius / 1000;
        parameters.cheap = checkedToNum(cheap);
        parameters.expensive = checkedToNum(expensive);
        parameters.singlepeople = checkedToNum(singlepeople);
        parameters.manypeople = checkedToNum(manypeople);
        parameters.open = checkedToNum(open);
        parameters.star = Number(star.value);
        parameters.manual = manual.value;

        data.append('parameters', JSON.stringify(parameters));


        fetch(user_input_url, {
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
        );
    };
});


function checkedToNum(checkbox) {
    if (checkbox.checked) {
        return 1;
    }
    return 0;
}
