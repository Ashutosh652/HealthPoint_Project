function commentReplyToggle(parent_id){
	const row = document.getElementById(parent_id);
	if(row.classList.contains('d-none')){
		row.classList.remove('d-none');
	}
	else{
		row.classList.add('d-none');
	}
}

// function likeToggle(post_id){
// 	const like = document.getElementById(post_id)
// 	if(post.classList.contains('far fa-thumbs-up')){
// 		post.classList.remove('far fa-thumbs-up');
// 		post.classList.add('fas fa-thumbs-up');
// 	}
// 	else{
// 		post.classList.remove('fas fa-thumbs-up');
// 		post.classList.add('far fa-thumbs-up');
// 	}
// }