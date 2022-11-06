
loadPosts(); 


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

function showProfileInfo(user_id) { 
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
    fetch(`/api/user/${user_id}`)
        .then(response => response.json())
        .then( user_data => {
            let account_data = user_data["creator"];  
            let account_post_data = user_data["posts"];
            // render components 
            document.getElementById("profile-info-username").innerHTML = account_data["username"];
            for(const post in account_post_data) {
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
                                <i class="fa-sharp fa-solid fa-heart" onclick="triggerHeartReactions(event)" ></i>
                                <i class="fa-sharp fa-solid fa-comment"></i>
                            </div>
                        </div>
                    </div>
                `; 
            }
        })
}

function createPost() { 
    const new_post_content = document.getElementById("newPostContent").value; 
    axios.post("/api/post", { "content": new_post_content }, { 
        headers: {'X-CSRFToken': csrf_token}
    }).then(response => {
        document.getElementById("newPostContent").value = "";
    })
}

function loadPosts() { 
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            // render components
            for(const post in posts) { 
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
                                <input type="text" class="form-control" id="newPostContent" value=${posts[post]["content"]}>
                                <small id="editHelp" class="form-text text-muted">click on <b>update</b> to change post content</small>
                                <button type="submit" class="btn btn-dark" style="margin-top: 1rem" >Update</button>
                          </div> 
                        </div>
                        <div class="column-3">
                            <p>
                                ${posts[post]["posted_time"]}
                            </p>
                            <div class="react-btns">   
                                <i class="fa-sharp fa-solid fa-heart" onclick="triggerHeartReactions(event)" ></i>
                                <i class="fa-sharp fa-solid fa-comment"></i>
                            </div>
                        </div>
                    </div>
                `
            }
        })
}

function triggerPostEditPanel(event) { 
    console.log(event); 
    document.querySelector(".post-content-text").style.display = "none";
    document.querySelector(".editPanel").style.display = "block";
}