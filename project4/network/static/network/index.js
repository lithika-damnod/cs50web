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