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
 * Performs the ajax request.
 * @param {string} action - the action type being requested.
 * @returns {void}
 */
function doAjax (action) {
  /* It's not really efficient to create a FormData and a json object,
     but the former is easier to pass to lexos.py functions, and the
     latter is easier for the ajax response to use. */
  const numActiveFiles = $('#numActiveFiles').val()
  const formData = new FormData($('form')[0])
  formData.append('action', action)
  const form = utility.jsonifyForm()
  const jsonForm = jsonifyForm()
  $.extend(jsonForm, {'action': action})
  // Initiate a timer to allow user to cancel if processing takes too long
  const loadingTimeout = window.setTimeout(function () {
    $('#needsWarning').val('true')
    const timeWarning = `Lexos seems to be taking a long time.  \
    This may be because you are cutting a large number of documents. 
    If not, we suggest that you cancel, reload the page, and try again.`
    const footerButtons = `<button type="button" class="btn btn-default" data-dismiss="modal">Continue Anyway</button>
    <button type="button" class="btn btn-default" id="timerCancel" >Cancel</button>`
    $('#warning-modal-footer').html(footerButtons)
    $('#warning-modal-message').html(timeWarning)
    $('#warning-modal').modal()
  }, 10000) // 10 seconds
  $.ajax({
    url: '/doCutting',
    type: 'POST',
    contentType: 'application/json; charset=utf-8',
    data: form,
    error: function (jqXHR, textStatus, errorThrown) {
      $('#status-prepare').css({'visibility': 'hidden'})
      // Show an error if the user has not cancelled the action
      if (errorThrown !== 'abort') {
        const notApplyMsg = 'Lexos could not apply the cutting actions.'
        $('#error-modal-message').html(notApplyMsg)
        $('#error-modal').modal()
      }
      console.log(`bad: ${textStatus}: ${errorThrown}`)
    }
  }).done(function (response) {
    clearTimeout(loadingTimeout)
    $('#warning-modal').modal('hide') // Hide the warning if it is displayed
    response = JSON.parse(response)
    $('#preview-body').empty() // Correct
    $.each(response['data'], function () {
      const fileID = $(this)[0]
      const fileName = $(this)[1]
      const fileLabel = fileName
      const fileContents = $(this)[3]
      const indivCutButtons = `<a id="indivcutbuttons_${fileID}" onclick="toggleIndivCutOptions(${fileID});" class="bttn indivcutbuttons" role="button">Individual Options</a></legend>`
      // CSS truncates the document label
      const fieldSet = $(`<fieldset class="individualpreviewwrapper"><legend class="individualpreviewlegend has-tooltip" style="color:#999; width:90%;margin: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${fileLabel} ${indivCutButtons}</fieldset>`)
      const indCutOptsWrap = `<div id="indcutoptswrap_${fileID}" class="cuttingoptionswrapper ind hidden">\
      <fieldset class="cuttingoptionsfieldset">\
      <legend class="individualcuttingoptionstitle">Individual Cutting Options</legend>\
      <div class="cuttingdiv individcut">\
      <div class="row">\
      <div class="col-md-5">\
      <label class="radio sizeradio">\
      <input type="radio" name="cutType_${fileID}" id="cutTypeIndLetters_${fileID}" value="letters"/>\
      Characters/Segment</label>\
      </div>\
      <div class="col-md-7">\
      <label class="radio sizeradio">\
      <input type="radio" name="cutType_${fileID}" id="cutTypeIndWords_${fileID}" value="words"/>\
      Tokens/Segment</label>\
      </div>\
      </div>\
      <div class="row cutting-radio">\
      <div class="col-md-5">\
      <label class="radio sizeradio">\
      <input type="radio" name="cutType_${fileID}" id="cutTypeIndLines_${fileID}" value="lines"/>\
      Lines/Segment</label>\
      </div>\
      <div class="col-md-7">\
      <label class="radio numberradio">\
      <input type="radio" name="cutType_${fileID}" id="cutTypeIndNumber_${fileID}" value="number"/>\
      Segments/Document</label>\
      </div>\
      </div>\
      </div>\
      <div class="row">\
      <div class="col-md-6 pull-right" style="padding-left:2px;padding-right:3%;">\
      <label>\
      <span id="numOf${fileID}" class="cut-label-text">Number of Segments:</span>\
      <input type="number" min="1" step="1" name="cutValue_${fileID}" class="cut-text-input" id="individualCutValue" value=""/>\
      </label>\
      </div>\
      </div>\
      <div class="row overlap-div">\
      <div class="col-md-6 pull-right" style="padding-left:2px;padding-right:3%;">\
      <label>Overlap: \
      <input type="number" min="0" name="cutOverlap_${fileID}" class="cut-text-input overlap-input" id="individualOverlap" value="0"/>\
      </label>\
      </div>\
      </div>\
      <div id="lastprop-div_${fileID}" class="row lastprop-div">\
      <div class="col-md-6 pull-right" style="padding-left:2px;padding-right:1%;">\
      <label>Last Proportion Threshold: \
      <input type="number" min="0" id="cutLastProp_${fileID}" name="cutLastProp_${fileID}" class="cut-text-input lastprop-input" value="50" style="width:54px;margin-right:3px;"/>\
      %</label>\
      </div>\
      </div>\
      <div class="row">\
      <div class="col-md-6 pull-right" style="padding-left:2px;padding-right:1%;">\
      <label>Cutset Label: \
      <input type="text" name="cutsetnaming_${fileID}" class="cutsetnaming" value="${fileName}" style="width:155px;display:inline; margin: auto; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"/>\
      </label>\
      </div>\
      </div>\
      <div class="row cuttingdiv" id="cutByMSdiv">\
      <div class="col-sm-4">\
      <label>\
      <input type="checkbox" class="indivMS" name="cutByMS_${fileID}" id="cutByMS_${fileID}"/>\
      Cut by Milestone</label>\
      </div>\
      <div class="col-sm-8 pull-right" id="MSoptspan" style="display:none;">\
      <span>Cut document on this term \
      <input type="text" class="indivMSinput" name="MScutWord_${fileID}" id="MScutWord${fileID}" value="" style="margin-left:3px;width:130px;"/>\
      </span>\
      </div>\
      </div>\
      </fieldset>\
      </div>`
      fieldSet.append(indCutOptsWrap)
      if ($.type(fileContents) === 'string') {
        fieldSet.append(`<div class="filecontents">${fileContents}</div>`) // Keep this with no whitespace!
      } else {
        $.each(fileContents, function (i, segment) {
          const segmentLabel = segment[0]
          const segmentString = segment[1]
          fieldSet.append(`<div class="filechunk"><span class="filechunklabel">${segmentLabel}</span><div>${segmentString}</div></div>`)
        })
      }
      $('#preview-body').append(fieldSet)
      // Hide the individual cutting wrapper if the form doesn't contain values for it
      if (!(`cutType_${fileID}` in formData) && formData[`cutType_${fileID}`] !== '') {
        $(`#indcutoptswrap_${fileID}`).addClass('hidden')
      }
      // Check the cut type boxes
      if (formData['cutTypeInd'] === 'letters') {
        $(`#cutTypeIndLetters_${fileID}`).prop('checked', true)
      }
      if (formData['cutTypeInd'] === 'words') {
        $(`#cutTypeIndWords_${fileID}`).prop('checked', true)
      }
      if (formData['cutTypeInd'] === 'lines') {
        $(`#cutTypeIndLines_${fileID}`).prop('checked', true)
      }
      if (formData['cutTypeInd'] === 'number') {
        $(`#cutTypeIndNumber_${fileID}`).prop('checked', true)
        $(`#numOf_${fileID}`).html('Number of Segments')
        $('#lastprop-div').addClass('transparent')
        $(`#cutLastProp_${fileID}`).prop('disabled', true)
      }
      if (formData['Overlap']) { $(`#cutOverlap_${fileID}`).val(formData['Overlap']) } else { $(`#cutOverlap_${fileID}`).val(0) }
      if (formData[`cutLastProp_${fileID}`]) {
        $(`#lastprop-div_${fileID}`).val(formData[`#cutLastProp_${fileID}`])
      }
      if (formData['cutType'] === 'milestone') {
        $(`#cutTypeIndNumber_${fileID}`).prop('checked', true)
      }
      if (formData[`MScutWord_${fileID}`] === 'milestone') {
        $(`#MScutWord${fileID}`).val(formData['cuttingoptions']['cutValue'])
      }
    })
    $('.fa-folder-open-o').attr('data-original-title', `You have ${numActiveFiles} active document(s).`)
    $('#status-prepare').css({'visibility': 'hidden'})
  })
}

/**
 * Checks the form data for errors and warnings.
 * @param {string} action - the action type being requested.
 * @returns {void}
 */
function process (action) { // eslint-disable-line no-unused-vars
  $('#status-prepare').css({'visibility': 'visible', 'z-index': '400000'})
  doAjax(action)

}

// Handle the Continue button in the warning modal
$(document).on('click', '#warningContinue', function () {
  $('#needsWarning').val('false')
  const action = $('#formAction').val()
  $('#warning-modal').modal('hide')
  doAjax(action)
  $('#status-prepare').css({'visibility': 'visible', 'z-index': '400000'})
})

// Handle the Timer Cancel button in the warning modal
$(document).on('click', '#timerCancel', function () {
  $('#needsWarning').val('false')
  $('#hasErrors').val('false')
  $('#warning-modal-footer').append('<button>Moo</button>')
  $('#warning-modal').modal('hide')
  $('#status-prepare').css('visibility', 'hidden')
})

/**
 * Convert the form data into a JSON object.
 * @returns {array} - returns the form data as a json object.
 */
function jsonifyForm () {
  const form = {}
  $.each($('form').serializeArray(), function (i, field) {
    form[field.name] = field.value || ''
  })
  return form
}


/**
 * Document ready function.
 */
$(function () {
  // New functions start here.
  $('#cut-method').change(function () { toggle_option() })
  get_checked_file_id()

  $('#actions').addClass('actions-cut')

  // Toggle cutting options when radio buttons with different classes are clicked
  const timeToToggle = 150
  $('.sizeradio').click(function () {
    const cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text')
    cuttingValueLabel.text('Segment Size:')

    $(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
      .animate({opacity: 1}, timeToToggle)
      .find('.lastprop-input').prop('disabled', false)

    $(this).parents('.cuttingoptionswrapper').find('.overlap-div')
      .animate({opacity: 1}, timeToToggle)
      .find('.overlap-input').prop('disabled', false)
  })

  $('.numberradio').click(function () {
    const cuttingValueLabel = $(this).parents('.cuttingoptionswrapper').find('.cut-label-text')
    cuttingValueLabel.text('Number of Segments:')

    $(this).parents('.cuttingoptionswrapper').find('.lastprop-div')
      .animate({opacity: 0.2}, timeToToggle)
      .find('.lastprop-input').prop('disabled', true)

    $(this).parents('.cuttingoptionswrapper').find('.overlap-div')
      .animate({opacity: 0.2}, timeToToggle)
      .find('.overlap-input').prop('disabled', true)
  })

  // Toggle individual cut option on load.
  $('.indivcutbuttons').click(function () {
    const toggleDiv = $(this).closest('.individualpreviewwrapper').find('.cuttingoptionswrapper')
    toggleDiv.toggleClass('hidden')
  })

  $("#apply-btn").click(function () {
    process("apply")
  })


  $(document).on('click', '.indivMS', function () {
    if ($(this).is(':checked')) {
      $(this).parents('#cutByMSdiv').filter(':first').children('#MSoptspan').show()
      $(this).parents('#cutByMSdiv').filter(':first')
        .parents('.cuttingoptionswrapper').find('.individcut').hide()
    } else {
      $(this).parents('#cutByMSdiv').filter(':first').children('#MSoptspan').hide()
      $(this).parents('#cutByMSdiv').filter(':first')
        .parents('.cuttingoptionswrapper').find('.individcut').show()
    }
  })
})
