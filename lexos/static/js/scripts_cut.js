import * as utility from './utility.js'

function toggle_option () {
  const selectedValue = $('#method option:selected').val()
  if (selectedValue === 'segments') {
    $('#cutting-option-for-general').hide()
    $('#cutting-option-for-segments').show('slide')
    $('#cutting-option-for-milestone').hide()
  } else if (selectedValue === 'milestone') {
    $('#cutting-option-for-general').hide()
    $('#cutting-option-for-segments').hide()
    $('#cutting-option-for-milestone').show('slide')
  } else {
    $('#cutting-option-for-general').show('slide')
    $('#cutting-option-for-segments').hide()
    $('#cutting-option-for-milestone').hide()
  }
}

function toggle_file_preview (clickedFileId) {
  $(`#${clickedFileId}`).toggle('drop')
}

function get_checked_file_id () {
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
      function () {
        utility.runModal('Error encountered while cutting the files.')
      })
}

/**
 * Document ready function.
 */
$(function () {
  // New functions start here.
  $('#method').change(function () {
    toggle_option()
  })
  $('.file-select').click(function () {
    toggle_file_preview($(this).val())
  })
  $('#apply-cut').click(function () {
    get_checked_file_id()
    applyCut()
  })
})
