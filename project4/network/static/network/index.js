
loadPosts(); 


function triggerHeartReactions(event, post_id) {
    const classList = event.target.classList; 
    if ( classList[3] === 'liked' ) {
        event.target.classList.add('disliked');
        event.target.classList.remove('liked'); 
        // update like count 
        console.log(event.currentTarget.parentNode); 
        var like_count_component = event.currentTarget.parentNode.querySelector(".like-count")
        var curr_likes = parseInt(like_count_component.innerHTML); 
        like_count_component.innerHTML = curr_likes - 1;  
        // send PUT request to update like status -> false    
        axios.put(`/api/post/${post_id}/liked`, {}, {  // send a blank put request, so it'll do the opposite of what it currently has in it's state
            headers: {'X-CSRFToken': csrf_token}
        })
    }
    else { 
        event.target.classList.add('liked');
        event.target.classList.remove('disliked'); 
        // update like count 
        var like_count_component = event.currentTarget.parentNode.querySelector(".like-count"); 
        var curr_likes = parseInt(like_count_component.innerHTML); 
        like_count_component.innerHTML = curr_likes + 1;  
        // send PUT request to update like status -> true
        axios.put(`/api/post/${post_id}/liked`, {}, {  // send a blank put request, so it'll do the opposite of what it currently has in it's state
            headers: {'X-CSRFToken': csrf_token}
        })
    }
}

async function showProfileInfo(user_id) { 
    // hide header section 
    document.querySelector(".create-post-wrapper").style.display = "none"; 
    document.querySelector(".page-title").style.display = "none"; 
    // hide post section 
    document.querySelector(".posts-wrapper").style.display = "none";
    // hide pagination 
    document.querySelector(".pagination-posts").style.display = "none"; 
    // show profile info section 
    document.querySelector(".profile-info-wrapper").style.display = "flex"; 

    // render post componets
    let user_data = await fetch(`/api/user/${user_id}`).then(response => response.json());
    let account_data = await user_data["creator"];  
    let account_post_data = await user_data["posts"];
    // render components 
    document.getElementById("profile-info-username").innerHTML = account_data["username"];
    for(const post in account_post_data) {

        // fetch for like status  
        var liked = false; 
        let likeStatus = await fetch(`/api/post/${account_post_data[post]["post_id"]}/liked`).then(response => response.json()); 
        if ( likeStatus["status"] === true ) { 
            liked = true;
        }
        else { 
            liked = false; 
        }

        document.querySelector(".posts-container").innerHTML += `
            <div class="post" style="width: 50vw">
                <div class="column-1" style="justify-content: flex-end;">
                    <h5>${account_data["username"]}</h5> 
                    <span id="pencil-icon">
                        <i class="fa-sharp fa-solid fa-pen" id="edit-icon" style="color: rgba(6, 130, 6, 0.401); margin: 0.3rem;"></i>
                    </span>
                </div>
                <div class="column-2">
                    <h4>
                        ${account_post_data[post]["content"]}
                    </h4>
                </div>
                <div class="column-3">
                    <p>
                        ${account_post_data[post]["posted_time"]}
                    </p>
                    <div class="react-btns">   
                        ${liked ? `<i class="fa-sharp fa-solid fa-heart liked" onclick="triggerHeartReactions(event, ${account_post_data[post]["post_id"]})"></i>` : `<i class="fa-sharp fa-solid fa-heart disliked" onclick="triggerHeartReactions(event, ${account_post_data[post]["post_id"]})"></i>`}
                        <span class="like-count">${account_post_data[post]["n_likes"]}</span>
                    </div>
                </div>
            </div>
        `; 
    }
}


function createPost() { 
    const new_post_content = document.getElementById("newPostContent").value; 
    axios.post("/api/post", { "content": new_post_content }, { 
        headers: {'X-CSRFToken': csrf_token}
    }).then(response => {
        document.getElementById("newPostContent").value = "";
        window.location.reload(); 
    })
}

async function loadPosts() { 
    let postRes = await fetch('/api/posts'); 
    let posts = await postRes.json(); 
    // render components
    for(const post in posts) { 
        var liked = false; 
        let likeStatus = await fetch(`/api/post/${posts[post]["post_id"]}/liked`).then(response => response.json()); 
        if ( likeStatus["status"] === true ) { 
            liked = true;
        }
        else { 
            liked = false; 
        }
        document.querySelector(".posts-wrapper").innerHTML += `
            <div class="post">
                <div class="column-1">
                    <h5 onclick="showProfileInfo(${posts[post]["creator"]["id"]})">${posts[post]["creator"]["username"]}</h5> 
                    <span id="pencil-icon" onclick="triggerPostEditPanel(event)">
                        <i class="fa-sharp fa-solid fa-pen" id="edit-icon" style="color: rgba(6, 130, 6, 0.401); margin: 0.3rem;"></i>
                    </span>
                </div>
                <div class="column-2">
                    <h4 class="post-content-text" >
                        ${posts[post]["content"]}
                    </h4>
                    <div class="form-group editPanel">
                        <input type="text" class="form-control newPostContent">
                        <small id="editHelp" class="form-text text-muted">click on <b>update</b> to change post content</small>
                        <button type="submit" class="btn btn-dark" style="margin-top: 1rem" onclick="updateContent(event, ${posts[post]["post_id"]})">Update</button>
                </div> 
                </div>
                <div class="column-3">
                    <p>
                        ${posts[post]["posted_time"]}
                    </p>
                    <div class="react-btns">   
                        ${liked ? `<i class="fa-sharp fa-solid fa-heart liked" onclick="triggerHeartReactions(event, ${posts[post]["post_id"]})"></i>` : `<i class="fa-sharp fa-solid fa-heart disliked" onclick="triggerHeartReactions(event, ${posts[post]["post_id"]})"></i>`}
                        <span class="like-count">${posts[post]["n_likes"]}</span>
                    </div>
                </div>
            </div>
        `
    }
}

function triggerPostEditPanel(event) { 
    event.currentTarget.parentNode.parentNode.querySelector(".post-content-text").style.display = "none";
    event.currentTarget.parentNode.parentNode.querySelector(".editPanel").style.display = "block";
    event.currentTarget.parentNode.parentNode.querySelector(".newPostContent").value = event.currentTarget.parentNode.parentNode.querySelector(".post-content-text").innerHTML.trim();
}

function handleFollowing() {
    let current_btn_state = document.querySelector(".follow-btn").innerHTML; 
    if( current_btn_state === "Follow") {
        document.querySelector(".follow-btn").innerHTML = "Unfollow"; 
        document.querySelector(".follow-btn").classList.remove("btn-secondary"); 
        document.querySelector(".follow-btn").classList.add("btn-danger"); 
    }
    else { 
        document.querySelector(".follow-btn").innerHTML = "Follow"; 
        document.querySelector(".follow-btn").classList.remove("btn-danger"); 
        document.querySelector(".follow-btn").classList.add("btn-secondary"); 
    }
}

function updateContent(event, post_id) { 
    var new_content = event.currentTarget.parentNode.parentNode.querySelector(".newPostContent").value; 
    var content_elem = event.currentTarget.parentNode.parentNode.querySelector(".post-content-text"); 
    var editPanel = event.currentTarget.parentNode.parentNode.parentNode.querySelector(".editPanel");

    event.currentTarget.parentNode.parentNode.querySelector(".newPostContent").value = event.currentTarget.parentNode.parentNode.querySelector(".post-content-text").innerHTML.trim();

    // fetch an PUT
    axios.put(`/api/post/${post_id}`, { "content": new_content }, { 
        headers: {'X-CSRFToken': csrf_token}
    }).then(response => {
        // backup view
        content_elem.innerHTML = new_content; 
        content_elem.style.display = "block";
        editPanel.style.display = "none";
    })
}