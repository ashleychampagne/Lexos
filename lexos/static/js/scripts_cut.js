import * as utility from './utility.js'

function toggle_option() {
  const selectedValue = $("#cut-method option:selected").val()
  if (selectedValue === "segments") {
    $("#cutting-option-for-general").hide()
    $("#cutting-option-for-segments").show()
    $("#cutting-option-for-milestone").hide()
  } else if (selectedValue === "milestone") {
    $("#cutting-option-for-general").hide()
    $("#cutting-option-for-segments").hide()
    $("#cutting-option-for-milestone").show()
  } else {
    $("#cutting-option-for-general").show()
    $("#cutting-option-for-segments").hide()
    $("#cutting-option-for-milestone").hide()
  }
}


function get_checked_file_id() {
    // Get all the checked files.
    const checkedFiles = $('.each-file :checked')
    // Set a variable to store checked file ids.
    let activeFileIds = ''
    // Store checked file ids by putting a blank between each id.
    checkedFiles.each(function () {
      activeFileIds += `${$(this).val()} `
    })
    // Store the variable to input field.
    $('#active_file_ids').val(activeFileIds)
}

/**
 * Display the result of the box plot on web page.
 * @return {string}: formatted file report.
 */
function applyCut () {
  // convert form into an object map string to string
  const form = utility.jsonifyForm()

  // send the ajax request
  utility.sendAjaxRequest('/apply_cut', form)
    .done(
      function (response) {
        console.log(response)
      })
    .fail(
      function (jqXHR, textStatus, errorThrown) {
        console.log('textStatus: ' + textStatus)
        console.log('errorThrown: ' + errorThrown)
        utility.runModal('Error encountered while cutting the files.')
      })
}


/**
 * Document ready function.
 */
$(function () {
  // New functions start here.
  $('#cut-method').change(function () { toggle_option() })
  get_checked_file_id()
  $('#apply-cut').click(function () {
    applyCut()
  })

})
