function getMostLiked(){
    $.ajax(
      {
        type:"GET",
        url: "/most_liked/",
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response)
        {
          var post_objects = JSON.parse(response.posts);
          for (post of post_objects){
            var post_id = post['pk'];
            $('#mostLikedPosts').append('<div class=row><a href="/post/' + post_id + '/">' + post['fields']['post_caption'] + '</a></div>');
          }
        },
        error: function (response) {
            alert(response["error"]);
        }
      })
}

$(window).on('load',getMostLiked);
