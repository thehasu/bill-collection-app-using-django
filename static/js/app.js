$('#id_city').change(function () {
    const url = $('#update-form').attr('data-areas-url');
    const cityid = $(this).val();

    $.ajax({
      url: url,
      data: {
        city_id: cityid
      },
      success: function (data) {
        $('#id_area').html(data);
      },
    });
  });

  console.log("Hello World")