// Listen for form submits
document.body.addEventListener('submit', function (event) {
  // Abort the form's POST
  event.preventDefault()

  // POST manually with the Fetch API
  var form = event.originalTarget

  fetch(form.action, {
    body: new FormData(form),
    credentials: 'include',
    headers: {
      'accept': 'application/json'
    },
    method: 'POST'
  }).then(function () {
    // Update the UI
    var parentBox = form.closest('div.matchbox')
    var boxesWrapper = form.closest('div.matchwrapper')
    var dateSection = form.closest('div.matchdatesection')

    // Remove the match box
    parentBox.parentNode.removeChild(parentBox)

    // If no match boxes in date section, remove the date section
    if (!boxesWrapper.children.length) {
      dateSection.parentNode.removeChild(dateSection)
    }

    // If no matches left at all, show "no matches" text
    if (!document.getElementsByClassName('matchdatesection').length) {
      document.getElementById('has-matches').style.display = 'none'
      document.getElementById('no-matches').style.display = 'block'
  }
  })
})
