function graph_traversal(triples, activities, courseCode) {
    let firstHop =
        triples.filter(triple => triple.h_name == courseCode || triple.t_name == courseCode)
        .map(triple => {
            let theOther = [triple.h_name, triple.t_name].filter(e => e != courseCode)[0]
            return theOther
        })
    let newData = {}
    let oldData = {}
    oldData[courseCode] = {
        uri: courseCode,
        week: -1,
        desc: courseCode
    }

    activities.forEach(activity => {
        // only reflect activity if it is shown on course graph
        for (triple of triples) {
            let involved = [triple.h_name, triple.t_name]
            if (involved.includes(activity.name)) {
                oldData[activity.name] = createItem(activity.desc, activity.name, activity.week)
                break
            }
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
                return false
            }
        })
    }
    return [newData, oldData]
}


function assign_timeslot(triples, activities, courseCode) {
    let [newdata,
        olddata
    ] = graph_traversal(triples, activities, courseCode)
    console.log(newdata)
    console.log(olddata)
    let timeslots = {}
    for (let i = 1; i < 14; i++) {
        timeslots[i - .5] = [];
        timeslots[i + ''] = [];
    }
    for (uri in olddata) {
        if (olddata[uri].week < 0) continue;
        let timeSlot = timeslots[olddata[uri].week];
        if (timeSlot) timeSlot.push(olddata[uri]);
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
                        (index_of_first_item + newdata[firstHopEntity].length) /
                        (totalItem / 13)) - 1,
                )
                slot = slot < 0 ? 0 : slot
                slot++
                let timeSlot = timeslots[slot];
                entity = createItem(content, uri, undefined);
                timeSlot.push(entity);
                counter++
            }
            let uri = firstHopEntity,
                content = firstHopEntity;
            let slot = slot_cursor + '.5'
            let timeSlot = timeslots[slot];
            entity = createItem(content, uri, undefined);
            timeSlot.push(entity);
        } else {}
    }
    for (firstHopEntity in newdata) {
        if (Object.keys(olddata).includes(firstHopEntity)) {

        } else if (newdata[firstHopEntity].length > 0) {} else {
            let uri = firstHopEntity,
                content = firstHopEntity;
            let slot = Math.floor(counter / (totalItem / 13)) + 1
            let timeSlot = timeslots[slot];
            entity = createItem(content, uri, undefined);
            timeSlot.push(entity);
            counter++
        }
    }
    return timeslots
}


function createItem(content, uri, week) {
    var item = {
        "name": uri,
        "desc": content,
        "week": week
    };
    return item;
}