document.addEventListener('DOMContentLoaded', function () {
    const like_buttons = document.querySelectorAll('.like_button');

    like_buttons.forEach(button => {
        button.addEventListener('click', function () {
            console.log('Botão clicado:', this.dataset.postId);

            const post_id = this.dataset.postId
            const csrftoken = document.querySelector('[name=csrf-token]').content

            fetch(`/like/${post_id}/`, {
                method: 'POST',
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    'X-CSRFToken': csrftoken
                }
            })
            .then(response => response.json())
            .then(data => {
                this.innerHTML = data.liked
                    ? `Descurtir (<span class="like-count">${data.likes_count}</span>)`
                    : `Curtir (<span class="like-count">${data.likes_count}</span>)`
            })
        })
    })
})
