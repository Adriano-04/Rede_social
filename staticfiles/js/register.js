document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-register')


    form.addEventListener('submit', async (e) => {
        e.preventDefault()

        const name = document.getElementById('username').value;
        const email = document.getElementById('useremail').value;
        const password = document.getElementById('password').value;
        const csrftoken = document.querySelector('[name=csrf-token]').content;

        try {
            const response = await fetch('/api/register/', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({name, email, password})
            })

            const data = await response.json()

            if (response.ok) {
                alert("usuario cadastrado")
                form.reset()
            } else {
                alert(`Erro no cadastrado : ${data.error}`)
            }
        } catch (error) {
            alert(`Erro no cadastrado : ${data.error}`)
            console.error(error)
        }
    })
})