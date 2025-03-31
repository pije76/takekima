$(document).ready(function()
{
    var data_url = "{{ title }}";
    console.log("data_url", data_url);

    const now = new Date();
    // $('.input-group.date').find("input").data("DateTimePicker").defaultDate(now);

    var globalcode = "";
    var url_code = "";
    var globalstart_date = "";
    var globalend_date = "";
    var url_itemdetail = "";
    // var url = "{% url 'books:view_report_detail' code=1 start_date=2 end_date=3 %}";
    var url = "/report/" + globalcode + "/?start_date=" + globalstart_date + "/?end_date=" + globalend_date;

    const csr = $("input[name=csrfmiddlewaretoken]").val();

    // let code = JSON.parse(document.getElementById('code').textContent);
    console.log("url", url);

    $(document).on('change', 'select#selectItem', function(e)
    {
        e.preventDefault();

        var code = $(this).val();
        globalcode = code;

        // url_code = url.replace('1', globalcode);

        // url_itemdetail = url.replace('1', globalcode) + "?start_date=" + url.replace('2', globalstart_date) + "&end_date=" + url.replace('3', globalend_date);
        console.log("globalcode", globalcode);

        $.ajax(
        {
            type: 'GET',
            // url: url_itemdetail,
            url: "",
            dataType: 'text',
            // dataType: 'json',
            data:
            {
                'item_code': globalcode,
                // "url_itemdetail": url_itemdetail,
                // csrfmiddlewaretoken: csr,
            },
            // success: function(data)
            // {
            //  console.log("data", data);
            //  // $('#itemForm').attr('action', url_itemdetail);
            // },
            // error: function(error)
            // {
            //  console.log("error");
            //  // console.log(error);
            // }
            // error: function(xhr, textStatus, error, errorThrown)
            // {
            //  console.log(xhr.responseText)
            //  console.log(xhr.statusText);
            //  console.log(textStatus);
            //  console.log(error);
            //  console.log(errorThrown);
            // },
        });
    });

    // $(document).on('change', 'select#selectItem', function(e)
    // {
    //  alert($(this).find("[name=start_date]").val());
    // });

    // $(document).on('change', 'input#start_date', function()
    // $(document).on('change', '#start_date', function(e)
    // $(document).on('change', 'input[name=start_date]', function()
    // $('input[name=start_date]').on('click', function()
    $('#start_date').on('change', function(e)
    {
        e.preventDefault();

        // var date_start = $(this).find("[name=start_date]").val();
        var start_date = $(this).val();
        globalstart_date = start_date;
        // var start_date = $(this).val();
        console.log("start_date", start_date);

        $.ajax(
        {
            type: 'GET',
            // url: url_itemdetail,
            // dataType: 'html',
            url: "",
            dataType: 'text',
            data:
            {
                "get_start_date": globalstart_date,
                // "url_itemdetail": url_itemdetail,
                // csrfmiddlewaretoken: csr,
            },
            success: function(data)
            {
                console.log(data.globalstart_date);
                $('#itemForm').attr('action', url_itemdetail);
            },
            error: function(error)
            {
                // console.log(error);
            }
        });
    });

    $('#end_date').on('change', function(e)
    {
        e.preventDefault();

        var optionSelected = $("option:selected", this);
        var place = this.value;
        console.log( $('#selectCountry').val());
        console.log(place);
        // var date_start = $(this).find("[name=start_date]").val();
        var end_date = $(this).val();
        globalend_date = end_date;
        // var date_start = $(this).val();
        console.log("end_date", end_date);

        $.ajax(
        {
            type: 'GET',
            // url: url_itemdetail,
            // dataType: 'html',
            url: "",
            dataType: 'text',
            data:
            {
                "get_end_date": globalend_date,
                // "url_itemdetail": url_itemdetail,
                // csrfmiddlewaretoken: csr,
            },
            success: function(data)
            {
                console.log(data.globalstart_date);
                $('#itemForm').attr('action', url_itemdetail);
            },
            error: function(error)
            {
                // console.log(error);
            }
        });
    });

    $( "#btnSubmit" ).click(function()
    {
        // url_itemdetail = url_code + "?start_date=" + globalstart_date + "&end_date=" + globalend_date;
        url_itemdetail = url.replace('1', globalcode) + "?start_date=" + url.replace('2', globalstart_date) + "&end_date=" + url.replace('3', globalend_date);
        console.log("url_itemdetail", url_itemdetail);
        // var field1value = $( "#field1" ).val()
        // alert( "Modal submitted with text: " + field1value);

        $.ajax(
        {
            type: 'GET',
            url: url_itemdetail,
            dataType: 'html',
            data:
            {
                // "data_item": code,
                "url_itemdetail": url_itemdetail,
                csrfmiddlewaretoken: csr,
            },
            success: function(data)
            {
                $('#itemForm').attr('action', url_itemdetail);
            },
            error: function(error)
            {
                console.log(error);
            }
        });
    });
});
