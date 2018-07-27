
///////////////////////////////////////////////////////////////////////////////////////////////////
// API :: payments
///////////////////////////////////////////////////////////////////////////////////////////////////

function fetchData() {
    $.getJSON('/api/payments', function(payments) {

        // hacky function
        function periodStart(period) {
            let start = period.split(' - ')[0].split('/');
            return Date.UTC(start[2], start[1], start[0]);
        }

        function paymentToHTML(payment, index, self) {

            let rowspan = self.filter(p => p.employee_id === payment.employee_id).length;

            let previous = self[index - 1] ? self[index - 1].employee_id : -1;

            let firstCol = previous !== payment.employee_id ? `<td rowspan="${rowspan}"><strong>${payment.employee_id}</strong></td>` : '';

            return `${firstCol}
                    <td>${payment.period}</td>
                    <td>${payment.amount}</td>`
        }

        let html = '<tr>' + payments.map(p => Object.assign(p, { amount: '$' + p.amount + '.00' }))
                                    .sort((a, b) => periodStart(a.period) > periodStart(b.period))
                                    .sort((a, b) => a.employee_id > b.employee_id)
                                    .map(paymentToHTML)
                                    .join('</tr><tr>') + '</tr>';

        $('#data').html(html);

    });
}


///////////////////////////////////////////////////////////////////////////////////////////////////
// AJAX file upload
///////////////////////////////////////////////////////////////////////////////////////////////////

$('input[type=file]').on('change', function(event) {

    event.stopPropagation();
    event.preventDefault();

    let data = new FormData();

    data.append('file', event.target.files[0]);

    $('#loader').addClass('active');
    $('#loading-icon').show();
    $('#loading-body').show();
    $('#success-icon').hide();
    $('#success-body').hide();
    $('#warning-icon').hide();
    $('#warning-body').hide();

    $.ajax({
        url: '/upload',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data, status, jqXHR) {
            console.log('HERE!');
            if(typeof data.error === 'undefined') {
                fetchData();
                $('#success-icon').show();
                $('#success-body').show();
            }
            else {
                $('#warning-icon').show();
                $('#warning-body').show();
            }
        },
        error: function(jqXHR, status, error) {
            $('#warning-icon').show();
            $('#warning-body').show();
        },
        complete: function() {
            $('#loader').removeClass('active');
            $('#loading-icon').hide();
            $('#loading-body').hide();
        }
    });

});


///////////////////////////////////////////////////////////////////////////////////////////////////
// On startup
///////////////////////////////////////////////////////////////////////////////////////////////////

fetchData();

