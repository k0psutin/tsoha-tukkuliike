$(document).ready(function () {
  var csrf_token = $('#csrf_token').val()
  $.post('/inventory_report', { csrf_token: csrf_token }, function (data) {
    if (!data['supply'] && !data['sale']) {
      $('#chartDiv').text('No data')
      return
    }

    if (data['supply']) {
      var trace1 = {
        x: data['supply_x'],
        y: data['supply_y'],
        name: 'Inventory',
        type: 'bar',
      }
    }

    if (data['sale']) {
      var trace2 = {
        x: data['sale_x'],
        y: data['sale_y'],
        name: 'Sales',
        type: 'bar',
        marker: {
          color: 'rgb(158,202,225)',
          line: {
            color: 'rgb(8,48,107)',
          },
        },
      }
    }

    var data = [trace1, trace2]

    var layout = {
      barmode: 'stack',
      title: 'Inventory status (Supply orders, batches and sales)',
    }

    Plotly.newPlot('chartDiv', data, layout)
  })
})
