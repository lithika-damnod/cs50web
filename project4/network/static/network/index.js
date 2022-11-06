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
    // hide pagination 
    document.querySelector(".pagination-posts").style.display = "none"; 
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

function loadPosts() { 
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            // render components
            for(const post in posts) { 
                document.querySelector(".posts-wrapper").innerHTML += `
                    <div class="post">
                        <div class="column-1">
                            <h5 onclick="showProfileInfo()">${posts[post]["creator"]}</h5> 
                            <span id="pencil-icon">
                                <i class="fa-sharp fa-solid fa-pen" id="edit-icon" style="color: rgba(6, 130, 6, 0.401); margin: 0.3rem;"></i>
                            </span>
                        </div>
                        <div class="column-2">
                            <h4>
                                ${posts[post]["content"]}
                            </h4>
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
loadPosts(); 