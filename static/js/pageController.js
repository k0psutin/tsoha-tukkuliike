function changePage(page_number, page, page_count_type) {
  $.post('/change_page', { page_count_type: page_count_type, page_number: page_number, page: page }, function () {
    location.reload()
  })
}

function nextPage(page, page_count_type) {
  $.post('/next_page', { page: page, page_count_type:page_count_type }, function () {
    location.reload()
  })
}

function prevPage(page, page_count_type) {
  $.post('/prev_page', { page: page, page_count_type:page_count_type }, function () {
    location.reload()
  })
}
