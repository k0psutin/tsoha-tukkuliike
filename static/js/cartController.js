function addToCart(sales = false) {
  resetHelpers()
  var csrf_token = $('#csrf').val()
  var item_name = $('select#items option:checked').text()
  var item_id = $('select#items option:checked').val()
  var company_id = $('select#company_id option:checked').val()
  var price = $('#price').val()
  var qty = $('#qty').val()
  console.log(company_id)

  var error = false

  if (item_id == '') {
    $('#itemHelp').text('Select an item')
    error = true
  }
  if (!sales) {
    if (company_id == '') {
      $('#companyHelp').text('Select a company')
      error = true
    }
  }
  if (Number(qty) === qty || qty % 1 !== 0) {
    $('#qtyHelp').text('Quantity must be an integer')
    error = true
  }
  if (qty == '' || qty < 1) {
    $('#qtyHelp').text('Quantity must be non-empty and higher than zero')
    error = true
  }
  if (price == '' || price <= 0) {
    $('#priceHelp').text('Price must be non-empty and higher than zero')
    error = true
  }

  if (price.includes('e')) {
    $('#priceHelp').text('Not a valid price.')
    error = true
  }

  if (qty.includes('e')) {
    $('#qtyHelp').text('Not a valid quantity.')
    error = true
  }

  if (typeof Number(qty) != 'number') {
    $('#qtyHelp').text('Invalid quantity type')
    error = true
  }

  if (error) return

  $('#qty').val('')
  $('#price').val('')

  var addItem = {
    company_id: company_id,
    item_name: item_name,
    item_id: item_id,
    qty: qty,
    price: price,
    csrf_token: csrf_token,
  }

  company_id = ''
  item_name = ''
  item_id = ''
  qty = ''
  price = ''
  csrf_token = ''

  $.post('/add_item_to_cart', addItem, function (count) {
    $('#showCart').text('Show cart (' + count + ')')
  })
  $('#showCart').prop('disabled', false)
}
$(document).ready(function () {
  $.get('/cart_count', function (count) {
    if (count == 0) {
      $('#showCart').prop('disabled', true)
      $('#showCart').text('Show cart')
    } else {
      $('#showCart').prop('disabled', false)
      $('#showCart').text('Show cart (' + count + ')')
    }
  })
})

function clearCart() {
  var csrf_token = $('#csrf').val()
  $.post('/clear_cart', { csrf_token: csrf_token })
  csrf_token = ''
  $('#showCart').prop('disabled', true)
  $('#showCart').text('Show cart')
  $('#closeCart').click()
}

function getCart() {
  $('#cartTable').empty()
  $('#modalBody').append(
    '<table id="cartTable" class="table table-striped"></table>'
  )
  $('#cartTable').append(
    '<thead class="thead">' +
      '<th scope="col">Item name</th>' +
      '<th scope="col">Quantity</th>' +
      '<th scope="col">Price</th>' +
      '<th scope="col"></th>' +
      '</thead>'
  )
  $.get('/get_cart', function (cart) {
    if (cart.length == 0) {
      $('#closeCart').click()
      return
    }
    var total = 0
    if (cart.length > 0) {
      cart.forEach((item) => {
        slot1 = uuidv4()
        slot2 = uuidv4()
        slot3 = uuidv4()
        slot4 = uuidv4()
        slot5 = uuidv4()

        button = $(
          '<button class="btn btn-light" type="button">Remove</button>'
        )
        button.click(function () {
          removeItemFromCart(
            item.item_id,
            item.item_name,
            item.qty,
            item.price,
            slot2
          )
        })

        qty = $(
          '<a id="' +
            slot3 +
            '" style="cursor: pointer;" type="button">' +
            item.qty +
            '</a>'
        )

        qty.click(function () {
          updateItemQty(item.item_id, item.qty, item.price, slot3, slot4)
        })
        price = item.price * item.qty
        total += price
        $('#cartTable').append(
          '<tr id=' +
            slot2 +
            '><td>' +
            item.item_name +
            '</td>' +
            '<td id="' +
            slot1 +
            '"></td>' +
            '<td id="' +
            slot4 +
            '">' +
            Number(price).toFixed(2) +
            '</td><td id="' +
            slot5 +
            '"></td></tr>'
        )
        $('#' + slot1).append(qty)
        $('#' + slot5).append(button)
      })
      $('#cartTable').append(
        '<tr><td></td><td>Total: </td>' +
          '<td id="total">' +
          Number(total).toFixed(2) +
          '</td></tr>'
      )
    }
  })
}

function removeItemFromCart(item_id, item_name, qty, price, slot) {
  var csrf_token = $('#csrf').val()
  var remove = confirm('Remove ' + item_name + '?')

  if (remove) {
    $.post(
      '/remove_item_from_cart',
      {
        item_id: item_id,
        csrf_token: csrf_token,
      },
      function () {
        $('#' + slot).remove()
        var total = $('#total').text()
        total -= parseFloat(price * qty).toFixed(2)
        $('#total').text(parseFloat(total).toFixed(2))
        $.get('/cart_count', function (count) {
          if (count == 0) {
            $('#showCart').prop('disabled', true)
            $('#showCart').text('Show cart')
            $('#closeCart').click()
          } else {
            $('#showCart').prop('disabled', false)
            $('#showCart').text('Show cart (' + count + ')')
          }
        })
      }
    )
  } else return
}

function updateItemQty(item_id, old_qty, price, slot3, slot4) {
  var csrf_token = $('#csrf').val()
  var qty = prompt('Change item quantity', '')

  if (qty == null || qty == '0' || qty == 0) return
  var total = $('#total').text()
  var new_price = qty * price
  total -= old_qty * price
  total += new_price

  $('#' + slot3).text(qty)
  $('#' + slot4).text(Number(new_price).toFixed(2))
  $('#total').text(total)

  $.post('update_cart_item_qty', {
    csrf_token: csrf_token,
    item_id: item_id,
    qty: qty,
  })
}

function makeOrder(sales = false, company = false) {
  var company_id = $('#company_id').val()
  if (sales) {
    if (company_id == '') {
      $('#companyHelp').text('Select a company')
      $('#confirmOrder').modal('hide')
      return
    }
  }
  var csrf_token = $('#csrf').val()
  var item
  if (sales) {
    item = { csrf_token: csrf_token, company_id: company_id }
  } else {
    item = { csrf_token: csrf_token }
  }
  $.post('/finalize_order', item, function (order_id) {
    if (sales || company) {
      var url = location.origin + '/order_summary/' + order_id
      window.location.replace(url)
    } else {
      $('#closeCart').click()
      location.reload()
    }
  })
}

function resetHelpers() {
  $('#priceHelp').text('')
  $('#qtyHelp').text('')
  $('#itemHelp').text('')
  $('#companyHelp').text('')
}

$(document).ready(function () {
  $('#items').change(function () {
    var form = $('#items').val()
    var price = $('#' + form * 10).val()

    $('#price').val(price)
  })
})

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = (Math.random() * 16) | 0,
      v = c == 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}
