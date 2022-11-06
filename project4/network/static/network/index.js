function triggerHeartReactions(event) {
    const classList = event.target.classList; 
    if ( classList[3] === 'liked' ) {
        event.target.classList.add('disliked');
        event.target.classList.remove('liked'); 
    }
    else { 
        event.target.classList.add('liked');
        event.target.classList.remove('disliked'); 
    }
}

function showProfileInfo() { 
    // hide header section 
    document.querySelector(".create-post-wrapper").style.display = "none"; 
    document.querySelector(".page-title").style.display = "none"; 
    // hide post section 
    document.querySelector(".posts-wrapper").style.display = "none";
    // show profile info section 
    document.querySelector(".profile-info-wrapper").style.display = "flex"; 
}

function createPost() { 
    const new_post_content = document.getElementById("newPostContent").value; 
    fetch('/api/post', {
        method: 'POST',
        body: {
            "content": new_post_content
        }
    }).then(() => { 
        document.getElementById("newPostContent").value = "";
    })
}