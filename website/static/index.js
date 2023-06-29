function like(postId) {
    // Get the like count element and like button element based on the postId
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
  
    // Send a POST request to the server to like the post
    fetch(`/like-post/${postId}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) => {
        // Update the like count with the updated value from the server
        likeCount.innerHTML = data["likes"];
        // Change the like button icon based on whether the post is liked or not
        if (data["liked"] === true) {
          likeButton.className = "fas fa-thumbs-up"; // Liked icon
        } else {
          likeButton.className = "far fa-thumbs-up";// Not Liked icon
        }
      })
      .catch((e) => alert("Could not like post.")); // Display an alert if liking the post fails
  }