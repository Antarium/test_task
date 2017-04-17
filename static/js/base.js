function ArticleLike(type_like){
  jQuery.ajax({
    	type: 'GET',
    	data: {'t_like': type_like, 't_content': 'article', },
		  url: document.location.pathname,
  		success: function(answer){
  			var data = JSON.parse(answer);
        $('#article_like').text(data['like']);
        $('#article_dislike').text(data['dislike']);
  		}
	});
}

function CommentLike(type_like, comment_id){
  jQuery.ajax({
    	type: 'GET',
    	data: {'t_like': type_like, 't_content': 'comment', 'comment_id': comment_id},
		  url: document.location.pathname,
  		success: function(answer){
  			var data = JSON.parse(answer);
        var like = '#comment_like_'+comment_id;
        var dislike = '#comment_dislike_'+comment_id;
        $(like).text(data['like']);
        $(dislike).text(data['dislike']);
  		}
	});
}
