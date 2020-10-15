function showConfirm(order_id) {
  var conf = confirm('Remove order ' + order_id + '?')
  return conf
}

function confirmAddItem() {
  var conf = confirm('Add item to order?')
  return conf
}

function confirmShipment(order_id) {
  var conf = confirm('Close and mark order ' + order_id + ' as collected?')
  return conf
}

function confirmDeleteItem(item_name) {
  var conf = confirm('Remove item ' + item_name + ' from order?')
  return conf
}

function updateOrderItemQty(item_id) {
  var csrf_token = $('#csrf_token').val()
  var company_id = $('#company_id').val()
  var order_id = $('#order_id').val()
  var qty = prompt('Change item quantity', '')

  console.log('csrf_token: ' + csrf_token)

  if (qty == null || qty == '0' || qty == 0) return

  $.post(
    '/update_sale_order',
    {
      csrf_token: csrf_token,
      item_id: item_id,
      qty: qty,
      order_id: order_id,
      company_id: company_id,
    },
    function () {
      location.reload()
    }
  )
}
