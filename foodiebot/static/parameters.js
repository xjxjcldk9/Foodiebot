const directSearch = document.getElementById("directSearch");

const otherParams = document.getElementById("otherParams");


const cheap = document.getElementById("cheap");
const expensive = document.getElementById("expensive");

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
        parameters.location = { "lat": myLocation.lat(), "lng": myLocation.lng() };
        //這邊是公尺
        parameters.radius = radius / 1000;
        parameters.cheap = checkedToNum(cheap);
        parameters.expensive = checkedToNum(expensive);
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
