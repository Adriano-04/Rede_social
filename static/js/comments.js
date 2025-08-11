document.querySelectorAll(".button_comments").forEach(btn => {
    btn.addEventListener('click', function() {
        let postId = this.dataset.postId

        document.getElementById('commentForm').action = `/posts/${postId}/add/`

        fetch(`/posts/${postId}/comments/`)
            .then(response => response.json())
            .then(data => {

                let list = document.getElementById('commentsList')
                list.innerHTML = "";

                data.forEach(c => {
                    list.innerHTML += `<p><b>${c.user__name}:</b> ${c.text}</p>`
                })

                document.getElementById('modalComments').style.display = 'block'
            })
    })
})

document.getElementById("closeModal").onclick = function() {
    document.getElementById("modalComments").style.display = "none";
}