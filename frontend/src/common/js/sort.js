function JsonSort (json, key) {
    // console.log(json);
      var groupId2index = {}
      json.sort(function (commentA, commentB) {
        var createdA = commentA.id
        var createdB = commentB.id
        // console.log(createdA, createdB)
        return createdA - createdB
      })
      for (var j = 0, jl = json.length; j < jl; j++) {
        var temp = json[j]
        groupId2index[temp.id] = j
      }
      // console.log(json);
      return groupId2index
    }