/**
 * Main function to classify user intent via API
 * Sends input to backend and displays structured results
 */
async function classifyIntent() {
    const userInput = document.getElementById('userInput').value.trim();
    
    // Hide previous results/errors
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    if (!userInput) {
        showError('Please enter some text to classify');
        return;
    }
    
    // Show loading state
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('classifyBtn').disabled = true;
    
    try {
        // Call the classification API
        const response = await fetch('/api/classify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Classification failed');
        }
        
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('classifyBtn').disabled = false;
    }
}

/**
 * Display classification results in the UI
 * Populates all result fields with color-coded badges and lists
 * 
 * @param {Object} data - Structured intent classification result
 */
function displayResults(data) {
    // Populate basic fields with dynamic badge styling
    document.getElementById('intentType').textContent = data.intent_type;
    document.getElementById('intentType').className = `value badge badge-${data.intent_type.toLowerCase()}`;
    
    document.getElementById('confidenceLevel').textContent = data.confidence_level;
    document.getElementById('confidenceLevel').className = `value badge badge-${data.confidence_level.toLowerCase()}`;
    
    document.getElementById('emotionalSignal').textContent = data.emotional_signal;
    document.getElementById('emotionalSignal').className = `value badge badge-${data.emotional_signal.toLowerCase()}`;
    
    document.getElementById('primaryGoal').textContent = data.primary_goal;
    
    // Populate lists
    populateList('secondaryGoals', data.secondary_goals);
    populateList('constraints', data.constraints);
    populateList('ambiguities', data.ambiguities);
    
    // Display JSON
    document.getElementById('jsonOutput').textContent = JSON.stringify(data, null, 2);
    
    // Show results
    document.getElementById('results').classList.remove('hidden');
}

/**
 * Populate a list element with items or show "None" if empty
 * 
 * @param {string} elementId - ID of the list element to populate
 * @param {Array} items - Array of items to display
 */
function populateList(elementId, items) {
    const listElement = document.getElementById(elementId);
    listElement.innerHTML = '';
    
    if (!items || items.length === 0) {
        // Display placeholder for empty lists
        const li = document.createElement('li');
        li.textContent = 'None';
        li.className = 'empty';
        listElement.appendChild(li);
    } else {
        // Create list item for each entry
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            listElement.appendChild(li);
        });
    }
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').classList.remove('hidden');
}

function copyJSON() {
    const jsonText = document.getElementById('jsonOutput').textContent;
    navigator.clipboard.writeText(jsonText).then(() => {
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    });
}

// Allow Enter key to submit (Ctrl+Enter for newline in textarea)
document.getElementById('userInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
        e.preventDefault();
        classifyIntent();
    }
});
