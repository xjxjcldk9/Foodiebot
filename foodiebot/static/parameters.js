const advancedsearch_button = document.getElementById("advancedButton");
const advancedsearch = document.getElementById("advancedsearch");

const otherparams_button = document.getElementById("otherparamsButton");
const otherparams = document.getElementById("otherparams");


advancedsearch.style.display = "none";

otherparams.style.display = "none";


if (!login) {
    otherparams_button.style.display = "none";
    advancedsearch_button.style.display = "none";
}



advancedsearch_button.addEventListener("click", () => {
    button_show(advancedsearch, advancedsearch_button)
}
)


otherparams_button.addEventListener("click", () => {
    button_show(otherparams, otherparams_button)
}
)

function button_show(x, button) {
    if (x.style.display === "none") {
        x.style.display = "block";
        button.classList.add("pure-button-active");
    } else {
        x.style.display = "none";
        button.classList.remove("pure-button-active");
    }
}



const money_cheap = document.getElementById("money_cheap");
const money_expensive = document.getElementById("money_expensive");

const people_single = document.getElementById("people_single");
const people_multiple = document.getElementById("people_multiple");


const store_open = document.getElementById("store_open");
const store_either = document.getElementById("store_either");

const rating_bar = document.getElementById("rating_bar");
const rating = document.getElementById("rating");

const manual = document.getElementById("manual");

money_cheap.addEventListener("click", () => {
    if (!money_cheap.checked && !money_expensive.checked) {
        money_expensive.checked = true;
    }
});


money_expensive.addEventListener("click", () => {
    if (!money_cheap.checked && !money_expensive.checked) {
        money_cheap.checked = true;
    }
});

people_single.addEventListener("click", () => {
    if (!people_single.checked && !people_multiple.checked) {
        people_multiple.checked = true;
    }
});


people_multiple.addEventListener("click", () => {
    if (!people_single.checked && !people_multiple.checked) {
        people_single.checked = true;
    }
});



store_either.addEventListener("click", () => {
    store_open.checked = !(store_open.checked);
});

store_open.addEventListener("click", () => {
    store_either.checked = !(store_either.checked);
});



rating.textContent = rating_bar.value;
rating_bar.addEventListener("input", (event) => {
    rating.textContent = event.target.value;
});





//Send POST

const postButton = document.getElementById('postButton');
postButton.addEventListener('click', () => {

    const loader = document.createElement('div')
    loader.className = 'Loader'
    postButton.parentElement.appendChild(loader);

    if (myLocation == null) {
        alert("請標註地點");
    }
    else {
        let data = new FormData;
        data.append("location", JSON.stringify(myLocation));
        data.append("radius", radius);
        data.append("money_cheap", money_cheap.checked);
        data.append("money_expensive", money_expensive.checked);
        data.append("people_single", people_single.checked);
        data.append("people_multiple", people_multiple.checked);
        data.append("store_open", store_open.checked);
        data.append("store_either", store_either.checked);
        data.append("rating", rating.value);
        data.append("search", manual.value);

        fetch(url, {
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
