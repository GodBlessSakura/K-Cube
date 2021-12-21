var iosDragDropShim = {
    enableEnterLeave: true
}
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