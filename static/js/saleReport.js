$(document).ready(function () {
  var currentYear = new Date().getFullYear()

  for (var i = currentYear; i >= 2000; i--) {
    if (i != currentYear) {
      $('#yearlist').append(
        '<option value=' + i + ' id=' + i + '>' + i + '</option>'
      )
    } else {
      $('#yearlist').append(
        '<option value=' + i + ' id=' + i + '>' + i + '</option>'
      )
    }
  }
})

$('#yearlist').change(function () {
  $('#chartDiv').text('')
  $('#statistics').text('')
  var year = $('#yearlist').val()

  if (year == 'None') return

  var csrf_token = $('#csrf_token').val()

  $.post('/sales_by_year', { year: year, csrf_token: csrf_token }, function (
    data
  ) {
    //console.log(data)

    if (data['empty']) {
      $('#chartDiv').text('No data')
      return
    }

    var average = data['average']
    var total = data['total']

    var xValue = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ]

    var yValue = data['x']

    var trace1 = {
      x: xValue,
      y: yValue,
      type: 'bar',
      text: yValue.map(String),
      textposition: 'auto',
      hoverinfo: 'none',
    }

    var data = [trace1]

    var layout = {
      title: 'Summary of ' + year,
    }

    $('#statistics').append(
      '<p> Total sales: ' +
        total +
        '<p><p> Average sale per month: ' +
        average +
        '<p>'
    )
    Plotly.newPlot('chartDiv', data, layout)
  })
})
