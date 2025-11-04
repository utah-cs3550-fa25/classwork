console.log("Hello, world");

function make_p_clickable(p) {
    p.addEventListener("click", (e) => {
        console.log("You clicked on:", p);
        e.preventDefault();
    });
}

let i = document.querySelector("input");
i.addEventListener("keydown", (e) => {
    e.preventDefault();
})

let ps = document.querySelectorAll("p");
for (let p of ps) {
    make_p_clickable(p);
}
