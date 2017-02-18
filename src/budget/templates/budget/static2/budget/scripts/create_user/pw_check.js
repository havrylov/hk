/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

$(document).ready(function() {
    $.passMeter({
        // Config local
        'id_password': '#password',
        'id_result': '#password-result',
        // Msg level pass
        'msg_bad': 'Extremly Weak <a href="#">Info</a>',
        'msg_low': 'Weak <a href="#">Info</a>',
        'msg_good': 'Middle strength',
        'msg_strong': 'Strong'});
    $("#retypepassword").focusout(function() {
        pw = $("#password").val();
        rtpw = $("#retypepassword").val();
        if (pw != rtpw) {
            $("#password-confirmed").html("<span class='failure'>X</span>");
        } else {
            $("#password-confirmed").html("<span class='success'>V</span>");
        }
    });
    $("#showpassword").select(function() {
        $("#password").type("text");
    });
    $('#user_form').on('submit', function(e) {
        e.preventDefault();
        if ($("#password").val() != $("#retypepassword").val()) {
            alert("Password does not match. \nPlease retype password.");
            $("#password").select();
        } else {
            this.submit();
        }
    });
});