let dragged;

//卡片庫
const source = document.getElementById('foodSource');
//卡片池
const pool = document.getElementById('foodPool');

//編輯區
const editpanel = document.getElementById('editpanel');


const template = document.getElementById('template');
template.style.display = "none";




function clear_edit() {
    const edit_blocks = document.querySelectorAll(".edit");

    edit_blocks.forEach((edit_block) => {
        edit_block.style.display = "none";
    });
}

//把每個編輯區塊都藏起來
clear_edit()



//將在編輯區塊中的卡片新增至相對應處
const edit_blocks = document.querySelectorAll(".edit .draggable_block");
edit_blocks.forEach((edit_block) => {
    const block = edit_block.cloneNode(true);
    block.draggable = true;

    if (block.classList[1] === 'on_board') {
        pool.appendChild(block);
    } else {
        source.appendChild(block);
    }

});



//讓掉落區中的卡片可以拖曳、顯示編輯區

const blocks = document.querySelectorAll(".dropzone .draggable_block");
blocks.forEach((block) => make_block_listen(block));


function make_block_listen(block) {
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


    block.addEventListener("click", () => {
        clear_edit();
        const target = document.getElementById(block.textContent);
        console.log(target);
        target.style.display = 'block';
    });
}




//新增卡片


const addButton = document.getElementById("add_food");
addButton.addEventListener("click", () => {
    clear_edit();
    const food_edit = document.createElement('div');
    food_edit.className = 'edit';

    editpanel.appendChild(food_edit);

    const describe_box = document.createElement('div');
    describe_box.classList.add("draggable_block", "reserve");

    describe_box.setAttribute('contenteditable', true);


    food_edit.appendChild(describe_box);

    describe_box.focus();


    const edit_template = template.cloneNode(true);
    edit_template.style.display = 'block';


    food_edit.appendChild(edit_template);


    const confirmButton = document.createElement("button");

    confirmButton.textContent = "新增食物";
    food_edit.appendChild(confirmButton);

    confirmButton.addEventListener("click", () => {
        const name = describe_box.textContent
        if (name != null) {
            food_edit.setAttribute('id', name);
            const food_block = document.createElement('div');
            food_block.textContent = name;
            food_block.className = "draggable_block";
            food_block.draggable = true;
            make_block_listen(food_block);
            source.appendChild(food_block);
            clear_edit();
            confirmButton.style.display = 'none';
            describe_box.setAttribute('contenteditable', false);
        }
    });
});



/* events fired on the drop targets */
const targets = document.querySelectorAll(".dropzone");

targets.forEach((target) => {

    target.addEventListener(
        "dragover",
        (event) => {
            // prevent default to allow drop
            event.preventDefault();
        },
        false,
    );

    target.addEventListener("dragenter", (event) => {
        // highlight potential drop target when the draggable element enters it
        if (event.target.classList.contains("dropzone")) {
            event.target.classList.add("dragover");
        }
    });

    target.addEventListener("dragleave", (event) => {
        // reset background of potential drop target when the draggable element leaves it
        if (event.target.classList.contains("dropzone")) {
            event.target.classList.remove("dragover");
        }
    });

    target.addEventListener("drop", (event) => {
        // prevent default action (open as link for some elements)
        event.preventDefault();
        // move dragged element to the selected drop target
        if (event.target.classList.contains("dropzone")) {
            event.target.classList.remove("dragover");
            event.target.appendChild(dragged);

            if (event.target.id === 'foodPool') {
                const edit_block = document.getElementById(dragged.textContent).getElementsByClassName('draggable_block')[0];
                edit_block.classList.add('on_board');
                edit_block.classList.remove('reserve');

            } else {
                const edit_block = document.getElementById(dragged.textContent).getElementsByClassName('draggable_block')[0];
                edit_block.classList.add('reserve');
                edit_block.classList.remove('on_board');
            }
        }
    });

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

        const trashEdit = document.getElementById(dragged.textContent);
        trashEdit.remove();
        dragged.remove();
    }
});



const saveBtn = document.getElementById('save');

saveBtn.addEventListener("click", () => {
    const foods = document.querySelectorAll(".edit");
    let data = new FormData;

    //Turn into binary then send I suppose:)


    foods.forEach((food) => {

        const checking = [];

        const name = food.getElementsByClassName('draggable_block')[0].textContent;
        const from_where = food.getElementsByClassName('draggable_block')[0].classList[1];
        const infs = food.getElementsByClassName('information');

        checking.push(from_where);

        for (const inf of infs) {
            checking.push(inf.checked);
        }

        data.append(name, checking);
    });



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


