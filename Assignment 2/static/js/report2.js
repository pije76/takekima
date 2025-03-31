$(document).ready(function()
{
    const now = new Date();
    var globalcode = "";
    var url_code = "";
    var globalstart_date = "";
    var globalend_date = "";
    var url_itemdetail = "";
    // var url = "{% url 'books:view_report_detail' code=1 start_date=2 end_date=3 %}";
    // var url_report = "/report/" + globalcode + "/?start_date=" + globalstart_date + "/?end_date=" + globalend_date;
    var url_report = "/report/items/";

    const csr = $("input[name=csrfmiddlewaretoken]").val();

    // var form = document.getElementById("itemForm");
    var form = $('form[name="itemForm"]');

    // let code = JSON.parse(document.getElementById('code').textContent);
    console.log("form", form);

    $(document).on('change', 'select#selectItem', function(e)
    {
        e.preventDefault();

        var code = $(this).val();
        globalcode = code;
        console.log("globalcode", globalcode);

        $.ajax(
        {
            type: 'GET',
            // url: "url_itemdetail",
            url: "http://127.0.0.1:8000/report/",
            dataType: 'html',
            data:
            {
                "code": globalcode,
            },
            success: function(data)
            {
                console.log("success");
                // console.log("data", data);
            },
            error: function(xhr, textStatus, error)
            {
                console.log("error");
                // console.log("xhr.responseText", xhr.responseText);
                console.log("xhr.statusText", xhr.statusText);
                console.log("textStatus", textStatus);
                console.log("error", error);
            },
        });

    });


    $('#start_date').on('change', function(e)
    {
        e.preventDefault();

        console.log("globalstart_date");

        var start_date = $(this).val();
        globalstart_date = start_date;
        console.log("globalstart_date", globalstart_date);

        $.ajax(
        {
            type: 'GET',
            // url: "url_itemdetail",
            url: "http://127.0.0.1:8000/report/",
            dataType: 'html',
            data:
            {
                "start_date": globalstart_date,
            },
            success: function(data)
            {
                console.log("success");
                // console.log("data", data);
                console.log("globalstart_date", globalstart_date);
            },
            error: function(xhr, textStatus, error)
            {
                console.log("error");
                // console.log("xhr.responseText", xhr.responseText);
                console.log("xhr.statusText", xhr.statusText);
                console.log("textStatus", textStatus);
                console.log("error", error);
            },
        });
    });

    $('#end_date').on('change', function(e)
    {
        e.preventDefault();

        var end_date = $(this).val();
        globalend_date = end_date;
        console.log("globalend_date", globalend_date);

        // var optionSelected = $("option:selected", this);
        // var place = this.value;
        // console.log( $('#selectCountry').val());
        // console.log(place);
        // var date_start = $(this).find("[name=start_date]").val();

        $.ajax(
        {
            type: 'GET',
            // url: "url_itemdetail",
            url: "http://127.0.0.1:8000/report/",
            dataType: 'html',
            data:
            {
                "end_date": globalend_date,
            },
            success: function(data)
            {
                console.log("success");
                // console.log("data", data);
            },
            error: function(xhr, textStatus, error)
            {
                console.log("error");
                // console.log("xhr.responseText", xhr.responseText);
                console.log("xhr.statusText", xhr.statusText);
                console.log("textStatus", textStatus);
                console.log("error", error);
            },
        });

    });

    $("#btnSubmit").click(function()
    {
        // url_itemdetail = url_code + "?start_date=" + globalstart_date + "&end_date=" + globalend_date;
        // url_itemdetail = url.replace('1', globalcode) + "?start_date=" + url.replace('2', globalstart_date) + "&end_date=" + url.replace('3', globalend_date);
        // url_itemdetail = url_code + "?start_date=" + globalstart_date + "&end_date=" + globalend_date;
        url_itemdetail = url_report + globalcode + "/" + globalstart_date + "/" + globalend_date + "/";
        console.log("globalcode_submit", globalcode);
        console.log("globalstart_date_submit", globalstart_date);
        console.log("globalend_date_submit", globalend_date);
        // var field1value = $( "#field1" ).val()
        // alert( "Modal submitted with text: " + field1value);

        // var url_send = url_report + "/items/" + globalcode + "/" + globalstart_date + "/" + globalend_date;

        $(form).attr('action', url_itemdetail);

        $.ajax(
        {
            method: 'POST',
            type: 'POST',
            // url: "url_itemdetail",
            url: "http://127.0.0.1:8000/report/",
            dataType: 'json',
            // dataType: 'text',
            // dataType: 'json',
            data:
            {
                "code": globalcode,
                // "response" url_send;
                "start_date": globalstart_date,
                "end_date": globalend_date,
                csrfmiddlewaretoken: csr,
            },
            success: function(data)
            {
                console.log("success");
                // console.log("data", data);
            },
            error: function(xhr, textStatus, error)
            {
                console.log("error");
                // console.log("xhr.responseText", xhr.responseText);
                console.log("xhr.statusText", xhr.statusText);
                console.log("textStatus", textStatus);
                console.log("error", error);
            },
        });
    });
});
