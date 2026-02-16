function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



async function sendResult()
{
    const test_id = document.getElementById("test_id").value;
    const score = document.getElementById("testScore").value;
    const statusMsg = document.getElementById("status-message");

    const token = localStorage.getItem('jwtAccess');

    if(!token)
    {
        statusMsg.innerText = `Ошибка токена ${token}`;

        return;
    }

    const data = {
        test: parseInt(test_id),
        score: parseInt(score),
        answers: {}
    }

    try{
        const response = await fetch('/results/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            statusMsg.style.color = "green";
            statusMsg.innerText = "Успешно сохранено! ID записи: " + result.id;
        } else {
            const errorData = await response.json();
            statusMsg.style.color = "red";
            statusMsg.innerText = "Ошибка: " + JSON.stringify(errorData);
        }
    } catch (error) {
        statusMsg.innerText = "Ошибка сети: " + error.message;
    }
}
//git remote set-url gitlab https://gitlab.com/health5155406/health.git
