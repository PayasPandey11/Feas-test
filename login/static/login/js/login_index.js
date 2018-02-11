$(document).ready(function() {

  $("#signup-button").click(function(){
    var username = $("#signup-username").val()
    var email = $("#signup-email").val()
    var password = $("#signup-password").val()
    console.log(username,email,password)
    var data = {"username":username,"email":email,"password":password}

    console.log(data)
    $.ajax({
      url: "signup",
      type: "post", // or "get"
      data: data,
      success: function(data) {
        if (data =="Username_taken"){
            console.log(data)
            $('#signup-error').text('Username_taken')
        }
        if (data =="email_taken"){
            $('#signup-error').text('Email_taken')
        }
        if (data =="Success"){
          window.location.replace("/home");

        }

    }})

  });
});
