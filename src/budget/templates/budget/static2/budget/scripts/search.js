$(document).ready(function() {
    $("#filter_settings").submit(function(e)
    {
        var getData = $(this).serializeArray();
        var formURL = $(this).attr("action");
        $.ajax(
                {
                    url: formURL,
                    type: "GET",
                    data: getData,
                    success: function(data, textStatus, jqXHR)
                    {
                        $('#fuck_off').html(data);
                        //data: return data from server
                    },
                    error: function(jqXHR, textStatus, errorThrown)
                    {
                        //if fails     
                    }
                });
        e.preventDefault(); //STOP default action
        e.unbind(); //unbind. to stop multiple form submit.
    });
});