function showConfirm(order_id) {
  var conf = confirm('Remove order ' + order_id + '?')
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
