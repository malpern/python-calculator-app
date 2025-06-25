let display = document.getElementById('display');
let history = document.getElementById('history');
let currentExpression = '0';
let lastResult = '';

function updateDisplay() {
    display.textContent = currentExpression;
    display.classList.add('update-animation');
    setTimeout(() => display.classList.remove('update-animation'), 300);
}

function clearDisplay() {
    currentExpression = '0';
    history.textContent = '';
    updateDisplay();
    animateButton(event.target);
}

function appendToDisplay(value) {
    if (currentExpression === '0' && value !== '.') {
        currentExpression = value;
    } else {
        currentExpression += value;
    }
    updateDisplay();
    animateButton(event.target);
}

function animateButton(button) {
    if (button) {
        button.classList.add('pressed');
        setTimeout(() => button.classList.remove('pressed'), 200);
    }
}

async function calculate() {
    try {
        history.textContent = currentExpression + ' =';
        
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression: currentExpression })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentExpression = data.result;
            lastResult = data.result;
            updateDisplay();
            display.classList.add('result-animation');
            setTimeout(() => display.classList.remove('result-animation'), 500);
        } else {
            display.textContent = data.error || 'Error';
            display.classList.add('error-animation');
            setTimeout(() => {
                display.classList.remove('error-animation');
                currentExpression = '0';
                updateDisplay();
            }, 2000);
        }
    } catch (error) {
        display.textContent = 'Error';
        display.classList.add('error-animation');
        setTimeout(() => {
            display.classList.remove('error-animation');
            currentExpression = '0';
            updateDisplay();
        }, 2000);
    }
    animateButton(event.target);
}

// Keyboard support
document.addEventListener('keydown', (event) => {
    if (event.key >= '0' && event.key <= '9') {
        appendToDisplay(event.key);
    } else if (event.key === '.') {
        appendToDisplay('.');
    } else if (event.key === '+' || event.key === '-' || event.key === '*' || event.key === '/') {
        appendToDisplay(event.key);
    } else if (event.key === 'Enter' || event.key === '=') {
        calculate();
    } else if (event.key === 'Escape' || event.key === 'c' || event.key === 'C') {
        clearDisplay();
    } else if (event.key === '(' || event.key === ')') {
        appendToDisplay(event.key);
    } else if (event.key === 'Backspace') {
        if (currentExpression.length > 1) {
            currentExpression = currentExpression.slice(0, -1);
        } else {
            currentExpression = '0';
        }
        updateDisplay();
    }
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    .update-animation {
        animation: fadeIn 0.3s ease-out;
    }
    
    .result-animation {
        animation: pulse 0.5s ease-out;
    }
    
    .error-animation {
        animation: shake 0.5s ease-out;
        color: #ff4444 !important;
    }
    
    .pressed {
        animation: press 0.2s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0.5; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    @keyframes press {
        0% { transform: scale(1); }
        50% { transform: scale(0.95); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);