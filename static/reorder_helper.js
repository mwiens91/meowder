// Find select boxes
var pic1box = document.getElementById('pic1select')
var boxes = [pic1box]

if (document.getElementById('pic2select')) {
  var pic2box = document.getElementById('pic2select')
  boxes.push(pic2box)
}

if (document.getElementById('pic3select')) {
  var pic3box = document.getElementById('pic3select')
  boxes.push(pic3box)
}

// Automatically reorder select boxes when a change is made
document.body.addEventListener('change', function (event) {
  // Check if the change came from the rating pictures
  var reorderbox = event.target.closest('div.reorderbox')

  // Get out if the change didn't come from the reorderbox
  if (!reorderbox) {
    return
  }

  // Make sure all pictures aren't being deleted
  var allDeleted = true

  boxes.forEach(function (item) {
    if (item.value !== 'delete') {
      allDeleted = false
    }
  })

  if (allDeleted) {
    // Cannot delete all images! Send an alert and reset the select box
    // '1'
    event.target.value = '1'
    window.alert('You must have at least one rating picture!')
    return
  }

  // Find all boxes that don't have a delete option
  var notDeleteSelections = boxes.filter(box => box.value !== 'delete')

  // If the event value just changed has another box with the same
  // value, promote or demote other boxes as necessary
  var oldDuplicateBox = notDeleteSelections.filter(function (box) {
    return box !== event.target && box.value === event.target.value
  })

  if (oldDuplicateBox.length) {
    // Reassign remaining values
    var remainingBoxes = notDeleteSelections.filter(box => box !== event.target)
    var remainingVals = Array.from({length: notDeleteSelections.length},
                                   (x, i) => i + 1)
                              .filter(x => x !== parseInt(event.target.value))
    remainingBoxes.sort((x, y) => parseInt(x.value) - parseInt(y.value))
    remainingBoxes.forEach(function (item, index) {
      item.value = String(remainingVals[index])
    })
  }

  // Sort the values
  notDeleteSelections.sort((x, y) => parseInt(x.value) - parseInt(y.value))

  // Re-assign (possibly again)
  notDeleteSelections.forEach(function (item, index) {
    item.value = String(index + 1)
  })
})
