/* replaced by your json data from database */
var olddata = {
    "old1": 1,
    "old2": 2
};
var newdata = ["new1", "new2"];


function createDiv(content) {
    var createDiv = document.createElement("div");
    createDiv.className = "list";
    createDiv.draggable = "true";
    createDiv.contentEditable = "true";
    createDiv.innerHTML = content;
    return createDiv;
}

function constructTimetable(olddata, newdata) {
    for (var key in olddata) {
        var timeSlot = document.getElementById('week' + olddata[key]);
        var entity = createDiv(key);
        timeSlot.appendChild(entity);
    }

    for (var key in newdata) {
        var timeSlot = document.getElementById('week13');
        var entity = createDiv(newdata[key]);
        timeSlot.appendChild(entity);
    }

    /* blank for add */
    for (var i = 1; i <= 13; i++) {
        var timeSlot = document.getElementById('week' + i);
        var entity = createDiv("");
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
            this.style.backgroundColor = '#f8f8f8';
        }, false);

        source[i].addEventListener('dragend', function (ev) {
            ev.target.style.backgroundColor = '#fff';
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
}