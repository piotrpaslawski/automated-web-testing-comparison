function buttonFunction1() {
    var x = document.getElementById("Button");
    var y = document.getElementById("pText");
    var z = document.getElementById("readOnlyText");

    if (x.style.color != "black") {
        x.style.color = "black";
        y.textContent = "#000000";
        y.style.color = "black";
        z.value = "#000000";
        z.style.color = "black";
    } else {
        x.style.color = "red";
        y.textContent = "#ff0000";
        y.style.color = "red";
        z.value = "#ff0000";
        z.style.color = "red";
    }
}

function sliderFunction1() {
    var s = document.getElementById("Slider");
    var p = document.getElementById("progressBar");
    var pl = document.getElementById("progressLabel");

    p.value = s.value;
    pl.textContent = "Progress bar: (" + p.value + "%)";
}

function selectFunction1() {
    var d = document.getElementById("Select").value;
    var m = document.getElementById("meterBar");
    var ml = document.getElementById("meterLabel");

    if (d == "1%") {
        m.value = "0.01";
        ml.textContent = "Percentage indicator: (1%)";
    }
    if (d == "50%") {
        m.value = "0.5";
        ml.textContent = "Percentage indicator: (50%)";
    }
    if (d == "100%") {
        m.value = "1.0";
        ml.textContent = "Percentage indicator: (100%)";
    }
}

function clickDropdownFunction() {
    var the_h3 = document.querySelector("h3");
    the_h3.textContent = "Default text";
    var overlay = document.querySelector(".dropdown-content");
    overlay.style.pointerEvents = "auto";
}

function clickOption1() {
    var the_h3 = document.querySelector("h3");
    the_h3.textContent = "Text 1";
    var overlay = document.querySelector(".dropdown-content");
    overlay.style.pointerEvents = "auto";
}

function clickOption2() {
    var the_h3 = document.querySelector("h3");
    the_h3.textContent = "Text 2";
    var overlay = document.querySelector(".dropdown-content");
    overlay.style.pointerEvents = "auto";
}

function clickOption3() {
    var the_h3 = document.querySelector("h3");
    the_h3.textContent = "Text 3";
    var overlay = document.querySelector(".dropdown-content");
    overlay.style.pointerEvents = "auto";
}
