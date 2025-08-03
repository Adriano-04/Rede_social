document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form_login')

    form.addEventListener('submit', async (e) => {
        e.preventDefault()

        const email = document.getElementById('useremail').value
        const password = document.getElementById('password').value
        const csrftoken = document.querySelector('[name=csrf-token]').content

        try {
            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({email , password})
            })
            
            const data = await response.json()

            if(response.ok) {
                window.location.href = "/feed/";
                alert('login efetuado')
                form.reset()
            } else {
                alert(data.erro || data.error || 'Erro no login')
            }
        } catch (error) {
            console.error(error)
            alert('erro no login')
        }
    })
})