const goodBtn = document.getElementById('good');
const badBtn = document.getElementById('bad');
const fireBtn = document.getElementById('fire');

let data = new FormData;




goodBtn.addEventListener("click", () => {
    goodBtn.classList.add("pure-button-active");
    badBtn.classList.remove("pure-button-active");

});


badBtn.addEventListener("click", () => {
    badBtn.classList.add("pure-button-active");
    goodBtn.classList.remove("pure-button-active");
});




fireBtn.addEventListener("click", () => {
    const activeBtn = document.getElementsByClassName('pure-button-active');
    if (activeBtn.length == 0) {
        alert('選一個表情才能送出');
    } else {
        data.append('response', activeBtn[0].id);
        fetch(url, {
            "method": "POST",
            "body": data,
        }).then(response => {
            if (response.redirected) {
                window.location = response.url
            } else {
                alert("一些錯誤提示")
            }
        });
    }
});





