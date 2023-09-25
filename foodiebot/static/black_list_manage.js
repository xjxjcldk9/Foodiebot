let dragged;

const pool = document.getElementById('pool');


//讓掉落區中的卡片可以拖曳、顯示編輯區

const blocks = document.querySelectorAll(".draggable_block");
blocks.forEach((block) => make_block_listen(block));


function make_block_listen(block) {
    block.draggable = true;

    block.addEventListener("drag", (event) => {
        //console.log("dragging");
    });

    block.addEventListener("dragstart", (event) => {
        // store a ref. on the dragged elem
        dragged = event.target;
        // make it half transparent
        event.target.classList.add("dragging");
    });

    block.addEventListener("dragend", (event) => {
        // reset the transparency
        event.target.classList.remove("dragging");
    });

}




//新增卡片


const addButton = document.getElementById("add_food");
addButton.addEventListener("click", () => {

    const describe_box = document.createElement('div');
    describe_box.classList.add("draggable_block");

    describe_box.setAttribute('contenteditable', true);

    pool.appendChild(describe_box);
    make_block_listen(describe_box);



    describe_box.focus();



});


const trash = document.querySelector(".trash");


trash.addEventListener(
    "dragover",
    (event) => {
        // prevent default to allow drop
        event.preventDefault();
    },
    false,
);

trash.addEventListener("dragenter", (event) => {
    // highlight potential drop target when the draggable element enters it
    if (event.target.classList.contains("trash")) {
        event.target.classList.add("dragover");
    }
});

trash.addEventListener("dragleave", (event) => {
    // reset background of potential drop target when the draggable element leaves it
    if (event.target.classList.contains("trash")) {
        event.target.classList.remove("dragover");
    }
});

trash.addEventListener("drop", (event) => {
    // prevent default action (open as link for some elements)
    event.preventDefault();
    // move dragged element to the selected drop target
    if (event.target.classList.contains("trash")) {
        event.target.classList.remove("dragover");
        //移除dragged
        dragged.remove();
    }
});



const saveBtn = document.getElementById('save');

saveBtn.addEventListener("click", () => {
    const foods = document.querySelectorAll(".draggable_block");
    let data = new FormData;

    //Turn into binary then send I suppose:)
    const name = [];


    foods.forEach((food) => {
        name.push(food.textContent);

    });

    data.append('black', name);

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
});

