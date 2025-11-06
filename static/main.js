console.log("Hello, world");

let show_pwd_box = document.querySelector("#show_pwd_box");
if (show_pwd_box) {
    show_pwd_box.addEventListener("click", (e) => {
        let form = show_pwd_box.closest("form");
        let pwd_input = form.querySelector("input[name=pass]");
        if (show_pwd_box.checked) {
            pwd_input.type = "text";
        } else {
            pwd_input.type = "password";
        }
    });
}

function update_results(cat_search_div) {
    let cat_input = cat_search_div.querySelector("#cat_search");
    let search_query = cat_input.value;

    let cat_results = cat_search_div.querySelector("#cat_results");
    let cats = document.querySelectorAll(".cat");
    let new_results = [];
    for (let cat of cats) {
        let cat_name = cat.dataset.catName;
        if (cat_name.indexOf(search_query) !== -1) {
            let li = document.createElement("li");
            li.append(cat_name)
            new_results.push(li);
        }
    }
    cat_results.replaceChildren(... new_results);
}

let cat_search = document.querySelector("#cat_search");
if (cat_search) {
    cat_search.addEventListener("focus", (e) => {
        cat_search.closest("div").classList.add("selected");
        update_results(cat_search.closest("div"));
    });
    cat_search.addEventListener("input", (e) => {
        update_results(cat_search.closest("div"));
    });
    cat_search.addEventListener("blur", (e) => {
        cat_search.closest("div").classList.remove("selected");
    });
}
