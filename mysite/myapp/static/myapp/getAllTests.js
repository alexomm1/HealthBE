async function getAllTests()
{
    const token = localStorage.getItem('jwtAccess');

    const response = await fetch ('/api/tests', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    });

    if(response.ok)
    {
        const tests = await response.json();
        console.log('Список тестов:', tests);

        renderTests(tests);
    }
}

function renderTests(tests)
{
    const container = document.getElementById('tests-container');
    container.innerHTML = tests.map(test => `
        <div class = "test-container">
            <div class = 'test-card' onclick = "startTest(${test.id})" style = "cursor: pointer;">
                <h3 class = "test-title">${test.title}</h4>
                <p class = "test-description">${test.description || 'Нет описания'}</p>
            </div>
        </div>
    `).join('');
}


function startTest(testId)
{
    alert("Вы выбрали тест с ID: " + testId);
}


window.onload = getAllTests;
