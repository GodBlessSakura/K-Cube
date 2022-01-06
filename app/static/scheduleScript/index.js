/* replaced by your json data from database */
var olddata = {
    "old1": 1,
    "old2": 2
};
var newdata = ["new1", "new2"];


function createDiv(content, uri) {
    var createDiv = document.createElement("div");
    createDiv.className = "list";
    createDiv.draggable = "true";
    createDiv.contentEditable = "true";
    createDiv.innerHTML = content;
    createDiv.dataset.uri = uri;
    return createDiv;
}

function constructTimetable(olddata, newdata) {
    var timeSlot = null,
        entity = null;
    for (var uri in olddata) {
        //console.log(uri);
        for (var key in olddata[uri]) {
            if (key == "week") {
                timeSlot = document.getElementById('week' + olddata[uri][key]);
            } else {
                entity = createDiv(olddata[uri]["desc"], uri);
            }
        }
        timeSlot.appendChild(entity);
    }
    let timeslots = {}
    for (let i = 0; i < 14; i++) {

        timeslots[i] = document.getElementById('week' + i);
    }
    for (let i = 0; i < newdata.length; i++) {
        let uri = newdata[i],
            content = newdata[i];
        let slot = Math.floor(i / (newdata.length / 13))
        let timeSlot = timeslots[slot + 1];
        entity = createDiv(content, uri);
        timeSlot.appendChild(entity);
    }

    /* blank for add */
    for (var i = 1; i <= 13; i++) {
        timeSlot = document.getElementById('week' + i);
        entity = createDiv("", "");
        timeSlot.appendChild(entity);
    }

    var iosDragDropShim = {
        enableEnterLeave: true
    };
    var source = document.querySelectorAll('.list'),
        recycle = document.getElementById('recycle'),
        dragElement = null,
        lock = true;

    for (var i = 0; i < source.length; i++) {
        source[i].addEventListener('dragstart', function (ev) {
            dragElement = this;
            ev.target.style = ev.target.style ? ev.target.style : {}
            ev.target.style["back-groundColor"] = '#f8f8f8';
        }, false);

        source[i].addEventListener('dragend', function (ev) {
            ev.target.style = ev.target.style ? ev.target.style : {}
            ev.target.style["back-groundColor"] = '#fff';
            ev.preventDefault();
        }, false)

        source[i].addEventListener('dragenter', function (ev) {
            if (dragElement != this) {
                this.parentNode.insertBefore(dragElement, this);
            }
        }, false)

        source[i].addEventListener('dragleave', function (ev) {
            console.log(111);
            if (dragElement != this) {
                if (lock && (this == this.parentNode.lastElementChild || this == this.parentNode.lastChild)) {
                    this.parentNode.appendChild(dragElement);
                    lock = false;
                } else {
                    lock = true;
                }
            }
        }, false)
    };
    recycle.addEventListener('drop', function (ev) {
        dragElement.parentNode.removeChild(dragElement);
    }, false)

    document.ondragover = function (e) {
        e.preventDefault();
    }
    document.ondrop = function (e) {
        e.preventDefault();
    }


    document.querySelector('#upJS').addEventListener('click', uploadTeachplan)

}


function createItem(div, day) {
    var item = {
        "name": "",
        "desc": "",
        "week": 0,
    };
    item["name"] = div.dataset.uri;
    item["desc"] = div.innerHTML;
    item["week"] = day;
    return item;
}

function uploadTeachplan() {
    for (var day = 1; day <= 13; day++) {
        var weeklyDivlist = document.getElementById('week' + day).querySelectorAll('.list');
        var item = null;
        for (let i = 0; i < weeklyDivlist.length; i++) {
            if (weeklyDivlist[i].innerHTML) {
                item = createItem(weeklyDivlist[i], day);
                updateItem(item);
            }

        }
    }
}