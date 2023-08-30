$(document).ready(function () {
  $('#id_city').change(function () {
    const url = $('#update-form').attr('data-areas-url');
    const cityid = $(this).val();

    $.ajax({
      url: url,
      data: {
        city_id: cityid,
      },
      success: function (data) {
        $('#id_area').html(data);
      },
    });
  });

  $('#id_billDate').datepicker({
    todayHighlight: true,
    format: 'yyyy-mm-dd',
  });

  console.log('Hello World');
});
