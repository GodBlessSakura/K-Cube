/* replaced by your json data from database */
var olddata = {
    "old1": 1,
    "old2": 2
};
var newdata = ["new1", "new2"];

function assignWeekValue(triples, activities, courseCode) {
    let firstHop =
        triples.filter(triple => triple.h_name == courseCode || triple.t_name == courseCode)
        .map(triple => {
            let theOther = [triple.h_name, triple.t_name].filter(e => e != courseCode)[0]
            return theOther
        })
    let newData = {}
    let oldData = {
        courseCode: {
            uri: courseCode,
            week: -1,
            desc: courseCode
        }
    }
    activities.forEach(activity => {
        oldData[activity.name] = {
            uri: activity.name,
            week: activity.week,
            desc: activity.desc
        }
    });
    let visited = [courseCode, ...firstHop]

    function depthFirst(entity) {
        let children = []
        triples.map(triple => {
            let involved = [triple.h_name, triple.t_name]
            if (involved.includes(entity)) {
                let theOther = [triple.h_name, triple.t_name]
                    .filter(e => e != entity)[0]
                if (!visited.includes(theOther)) {
                    children.push(theOther)
                    visited.push(theOther)
                }
            }
        })
        let result = [entity]
        for (child of children) {
            result = [...result, ...depthFirst(child)]
        }
        return result
    }
    for (firstHopEntity of firstHop) {
        newData[firstHopEntity] = depthFirst(firstHopEntity).filter(e => e != firstHopEntity)
    }
    for (firstHopEntity of firstHop) {
        newData[firstHopEntity] = newData[firstHopEntity].filter(entity => {
            let candidate = activities.filter(a => a.name == entity)
            if (candidate.length == 0) {
                return true
            } else {
                let activity = candidate[0]
                oldData[candidate[0].name] = {
                    uri: candidate[0].name,
                    week: candidate[0].week,
                    desc: candidate[0].desc
                }
                return false
            }
        })
    }
    return [newData, oldData]
}

function createDiv(content, uri) {
    var createDiv = document.createElement("div");
    createDiv.className = "list";
    createDiv.draggable = "true";
    createDiv.contentEditable = "true";
    createDiv.innerHTML = content;
    createDiv.dataset.uri = uri;
    return createDiv;
}

function constructTimetable(triples, activities, courseCode) {
    let [newdata,
        olddata
    ] = assignWeekValue(triples, activities, courseCode)
    console.log(newdata)
    console.log(olddata)
    let timeslots = {}
    for (let i = 1; i < 14; i++) {
        timeslots[i + ''] = document.getElementById('week' + i);
    }
    for (var i = 0; i <= 12; i++) {

        timeslots[i + '.5'] = document.getElementById('week' + i + '.5');
    }
    for (id in timeslots) {
        timeslots[id].innerHTML = id % 1 != 0 ? '' : '<div class="time" draggable="false">Week ' + id + '</div>'
    }
    for (uri in olddata) {
        if (olddata[uri].week < 0) continue;
        let timeSlot = document.getElementById('week' + olddata[uri].week);
        let entity = createDiv(olddata[uri]["desc"], uri);
        timeSlot.appendChild(entity);
    }
    // add new data
    let totalItem = 0
    for (firstHopEntity in newdata) {
        totalItem = totalItem + (newdata[firstHopEntity].length < 1 ? 1 : newdata[firstHopEntity].length)
    }

    let counter = 0
    for (firstHopEntity in newdata) {
        if (Object.keys(olddata).includes(firstHopEntity)) {

        } else if (newdata[firstHopEntity].length > 0) {
            let slot_cursor = Math.floor(counter / (totalItem / 13))
            let index_of_first_item = counter
            for (depthFirstEntity of newdata[firstHopEntity]) {
                let uri = depthFirstEntity,
                    content = depthFirstEntity;
                let slot = Math.min(
                    Math.floor(counter / (totalItem / 13)),
                    Math.floor(
                        (slot_cursoindex_of_first_itemr + newdata[firstHopEntity].length) /
                        (totalItem / 13)) - 1
                )
                let timeSlot = timeslots[slot + 1];
                entity = createDiv(content, uri);
                timeSlot.appendChild(entity);
                counter++
            }
            let uri = firstHopEntity,
                content = firstHopEntity;
            let timeSlot = timeslots[slot_cursor + '.5'];
            entity = createDiv(content, uri);
            timeSlot.appendChild(entity);
        } else {}
    }
    for (firstHopEntity in newdata) {
        if (Object.keys(olddata).includes(firstHopEntity)) {

        } else if (newdata[firstHopEntity].length > 0) {} else {
            let uri = firstHopEntity,
                content = firstHopEntity;
            let slot = Math.floor(counter / (totalItem / 13))
            let timeSlot = timeslots[slot + 1];
            entity = createDiv(content, uri);
            timeSlot.appendChild(entity);
            counter++
        }
    }

    /* blank for add */
    for (var i = 1; i <= 13; i++) {
        timeSlot = document.getElementById('week' + i);
        entity = createDiv("", "");
        entity.draggable = false
        timeSlot.appendChild(entity);
    }
    for (var i = 0; i <= 12; i++) {
        timeSlot = document.getElementById('week' + i + '.5');
        entity = createDiv("", "");
        entity.draggable = false
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
                if (lock && (this == this.parentNode.lastElementchildren || this == this.parentNode.lastchildren)) {
                    this.parentNode.appendChild(dragElement);
                    lock = false;
                } else {
                    lock = true;
                }
            }
        }, false)
    };
    recycle.addEventListener('drop', function (ev) {
        dragElement.parentNode.removechildren(dragElement);
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
    let timeslots = {}
    for (let i = 1; i < 14; i++) {

        timeslots[i] = document.getElementById('week' + i);
    }
    for (var i = 0; i <= 12; i++) {

        timeslots[i + '.5'] = document.getElementById('week' + i + '.5');
    }
    console.log(timeslots)
    for (day in timeslots) {
        var weeklyDivlist = timeslots[day].querySelectorAll('.list');
        var item = null;
        for (let i = 0; i < weeklyDivlist.length; i++) {
            if (weeklyDivlist[i].innerHTML) {
                item = createItem(weeklyDivlist[i], day);
                updateItem(item);
            }

        }
    }
}