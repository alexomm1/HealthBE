async function loadTest()
{
    const params = new URlSearchParams(window.location.search);
    const testId = params.get('id');
    const token = localStorage.getItem('jwtAccess');

    const response = fetch('http://127.0.0.1/test/${testId}', {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer: ${token}`
        }
    });

    if(response.ok)
    {
        const test = await response.json();
        renderTest(test);
    }
}

function renderTest(test)
{
    document.getElementById('test-title').textContent = test.title;
    document.getElementById('test-description').textContent = test.description;

    const container = document.getElementById('question-container');
    container.innerHTML = test.questions.map(q => `
        <div class = 'question'>
            <h4>${q.Text}</h4>
            <div class = 'answers'>
                ${q.answers.map(a => `
                    <label>
                        <input type='radio' name='question_${q.id}' value = '${a.id}'>
                        ${a.text}
                    </label>
                `)}.join();
            </div>
        </div>
    `).join();
}

window.onload = loadTest;