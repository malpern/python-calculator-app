let display = document.getElementById('display');
let history = document.getElementById('history');
let currentExpression = '0';
let lastResult = '';
let isTyping = false;

function typewriterEffect(element, text, speed = 50) {
    return new Promise((resolve) => {
        element.textContent = '';
        let i = 0;
        isTyping = true;
        element.classList.add('typing');
        
        const timer = setInterval(() => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                // Add subtle vibration effect
                element.style.transform = `translateX(${Math.random() * 2 - 1}px)`;
            } else {
                clearInterval(timer);
                element.style.transform = 'translateX(0)';
                element.classList.remove('typing');
                isTyping = false;
                resolve();
            }
        }, speed);
    });
}

async function updateDisplay(useTypewriter = false) {
    if (useTypewriter && currentExpression.length > 0) {
        await typewriterEffect(display, currentExpression, 30);
    } else {
        display.textContent = currentExpression;
        display.classList.add('typing');
        setTimeout(() => display.classList.remove('typing'), 300);
    }
}

function clearDisplay() {
    currentExpression = '0';
    history.textContent = '';
    display.classList.remove('result', 'error');
    updateDisplay();
    animateButton(event.target);
    
    // Add clearing animation
    display.style.animation = 'fadeOut 0.2s ease-out, fadeIn 0.3s ease-out 0.2s';
    setTimeout(() => {
        display.style.animation = '';
    }, 500);
}

function appendToDisplay(value) {
    if (isTyping) return; // Prevent input during typing animation
    
    if (currentExpression === '0' && value !== '.') {
        currentExpression = value;
    } else {
        currentExpression += value;
    }
    updateDisplay();
    animateButton(event.target);
    
    // Add subtle glow effect
    display.style.filter = 'brightness(1.2)';
    setTimeout(() => {
        display.style.filter = '';
    }, 200);
}

function animateButton(button) {
    if (button) {
        button.classList.add('pressed');
        
        // Create ripple effect
        const ripple = document.createElement('div');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;
        
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = (rect.width / 2 - size / 2) + 'px';
        ripple.style.top = (rect.height / 2 - size / 2) + 'px';
        
        button.appendChild(ripple);
        
        setTimeout(() => {
            button.classList.remove('pressed');
            ripple.remove();
        }, 600);
    }
}

// Safe evaluation function
function safeEval(expression) {
    try {
        // Replace display symbols with JavaScript operators
        let jsExpression = expression
            .replace(/×/g, '*')
            .replace(/÷/g, '/')
            .replace(/−/g, '-')
            .replace(/\^/g, '**');
        
        // Security: Only allow mathematical expressions
        const allowedChars = /^[0-9+\-*/.() Math.sqrt()Math.sin()Math.cos()Math.tan()Math.log()Math.PI]*$/;
        if (!allowedChars.test(jsExpression.replace(/\s/g, ''))) {
            throw new Error('Invalid characters');
        }
        
        // Replace Math functions properly
        jsExpression = jsExpression
            .replace(/Math\.sqrt\(/g, 'Math.sqrt(')
            .replace(/Math\.sin\(/g, 'Math.sin(')
            .replace(/Math\.cos\(/g, 'Math.cos(')
            .replace(/Math\.tan\(/g, 'Math.tan(')
            .replace(/Math\.log\(/g, 'Math.log(');
        
        // Evaluate using Function constructor for safety
        const result = new Function('Math', `"use strict"; return (${jsExpression})`)(Math);
        
        if (typeof result !== 'number' || !isFinite(result)) {
            throw new Error('Invalid result');
        }
        
        return result;
    } catch (error) {
        throw new Error('Invalid expression');
    }
}

async function calculate() {
    if (isTyping) return; // Prevent calculation during typing
    
    try {
        // Add loading state
        display.classList.add('calculating');
        history.textContent = currentExpression + ' =';
        
        // Add calculating animation
        const originalText = display.textContent;
        let dots = '';
        const loadingInterval = setInterval(() => {
            dots = dots.length >= 3 ? '' : dots + '.';
            display.textContent = 'calculating' + dots;
        }, 200);
        
        // Simulate network delay for better UX
        await new Promise(resolve => setTimeout(resolve, 800));
        
        const result = safeEval(currentExpression);
        
        clearInterval(loadingInterval);
        display.classList.remove('calculating');
        
        // Format result
        let formattedResult = result.toString();
        if (result % 1 !== 0 && result.toString().length > 10) {
            formattedResult = result.toPrecision(10);
        }
        
        currentExpression = formattedResult;
        lastResult = formattedResult;
        
        // Animate result with typewriter effect
        display.classList.add('result');
        await typewriterEffect(display, currentExpression, 80);
        
        // Add success glow
        display.style.filter = 'drop-shadow(0 0 20px rgba(76, 175, 80, 0.8))';
        setTimeout(() => {
            display.style.filter = '';
            display.classList.remove('result');
        }, 2000);
        
    } catch (error) {
        clearInterval(loadingInterval);
        display.classList.remove('calculating');
        display.classList.add('error');
        
        const errorMessage = error.message === 'Invalid expression' ? 'Error' : 'Math Error';
        await typewriterEffect(display, errorMessage, 60);
        
        // Add error glow
        display.style.filter = 'drop-shadow(0 0 20px rgba(244, 67, 54, 0.8))';
        
        setTimeout(async () => {
            display.style.filter = '';
            display.classList.remove('error');
            currentExpression = '0';
            await updateDisplay(true);
        }, 2500);
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
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .calculating {
        animation: calculating 1s ease-in-out infinite;
        color: var(--accent-color) !important;
    }
    
    @keyframes calculating {
        0%, 100% { 
            text-shadow: 
                0 0 20px currentColor,
                0 0 40px rgba(187, 134, 252, 0.5);
        }
        50% { 
            text-shadow: 
                0 0 30px currentColor,
                0 0 60px rgba(187, 134, 252, 0.8),
                0 0 80px rgba(187, 134, 252, 0.6);
            transform: scale(1.02);
        }
    }
    
    .pressed {
        animation: buttonPress 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes buttonPress {
        0% { transform: scale(1); }
        50% { transform: scale(0.95); filter: brightness(1.3); }
        100% { transform: scale(1); }
    }
    
    /* Particle effects for result */
    .result::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 4px;
        height: 4px;
        background: var(--success-color);
        border-radius: 50%;
        animation: particle 2s ease-out infinite;
        pointer-events: none;
    }
    
    @keyframes particle {
        0% {
            transform: translate(-50%, -50%) scale(0);
            opacity: 1;
        }
        50% {
            transform: translate(-150%, -150%) scale(1);
            opacity: 0.8;
        }
        100% {
            transform: translate(-300%, -300%) scale(0);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Add sound effects (optional, requires user interaction first)
function playSound(type) {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        switch(type) {
            case 'click':
                oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
                break;
            case 'result':
                oscillator.frequency.setValueAtTime(1200, audioContext.currentTime);
                break;
            case 'error':
                oscillator.frequency.setValueAtTime(300, audioContext.currentTime);
                break;
        }
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
        // Sound not supported, ignore
    }
}