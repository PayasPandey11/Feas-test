$(document).ready(function() {

  $("#is_following").click(function(e){
    var follow_status = $(this).attr('value');
    var username = $(this).prev().attr('value');
    var data = {"username":username,"follow_status":follow_status};
    var p = e.currentTarget;
    console.log(e)
    $.ajax({
      url: "follow",
      type: "post", // or "get"
      data: data,
      success: function(data) {
        console.log(p)
        if (data == "following"){
            console.log("f",p);
            $(p).val('not_following');
            $(p).html('follow');

        }
        if (data == "not_following"){
            console.log("nf",p);
            $(p).val('following');
            $(p).html('unfollow');
        }

    }})

  });
});
