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
        
        // Orchestration Logic: Module 2 runs ONLY if ambiguities exist
        if (data.ambiguities && data.ambiguities.length > 0) {
            await resolveAmbiguity(data);
        } else {
            document.getElementById('resolutionResults').classList.add('hidden');
        }
        
    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('classifyBtn').disabled = false;
    }
}

/**
 * Stage 2: Resolve ambiguities in the classified intent
 * @apiNote This stage is only triggered if ambiguities are detected in Stage 1.
 * Calls the resolution API and displays either a question or assumptions
 * 
 * @param {Object} intentData - The output from Module 1
 */
async function resolveAmbiguity(intentData) {
    try {
        const response = await fetch('/api/resolve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(intentData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            console.error('Resolution failed:', data.error);
            return;
        }
        
        displayResolution(data);
        
        // Orchestration Logic: Module 3 runs if resolution is AssumptionsMade (or effectively successful)
        // If it was ClarificationRequired, we stop.
        if (data.resolution_type === 'AssumptionsMade') {
             // Merge resolution data back into intentData for the final plan
             // We need to pass the FULL context to Module 3
             const fullContext = { ...intentData, ...data };
             await generateExecutionPlan(fullContext);
        }
        
    } catch (error) {
        console.error('Error in resolution stage:', error);
    }
}

/**
 * Stage 3: Generate Execution Plan
 * Calls the planning API and displays the final roadmap
 */
async function generateExecutionPlan(resolvedIntent) {
    try {
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(resolvedIntent)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            console.error('Planning failed:', data.error);
            return;
        }
        
        displayPlan(data);
        
    } catch (error) {
        console.error('Error in planning stage:', error);
    }
}

/**
 * Display resolution results in the UI
 * 
 * @param {Object} data - Resolution object from Module 2
 */
function displayResolution(data) {
    const resolutionDiv = document.getElementById('resolutionResults');
    const questionContainer = document.getElementById('questionContainer');
    const assumptionsContainer = document.getElementById('assumptionsContainer');
    const resolutionType = document.getElementById('resolutionType');
    
    resolutionType.textContent = data.resolution_type;
    resolutionType.className = `value badge badge-${data.resolution_type.toLowerCase()}`;
    
    if (data.resolution_type === 'ClarificationRequired') {
        questionContainer.classList.remove('hidden');
        assumptionsContainer.classList.add('hidden');
        document.getElementById('clarificationQuestion').textContent = data.clarification_question;
    } else {
        questionContainer.classList.add('hidden');
        assumptionsContainer.classList.remove('hidden');
        renderListSection('assumptionsList', 'assumptionsContainer', data.assumptions);
    }
    
    resolutionDiv.classList.remove('hidden');
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
    
    // Populate lists with conditional rendering
    renderListSection('secondaryGoals', 'secondaryGoalsSection', data.secondary_goals);
    renderListSection('constraints', 'constraintsSection', data.constraints);
    renderListSection('ambiguities', 'ambiguitiesSection', data.ambiguities);
    
    // Display JSON
    document.getElementById('jsonOutput').textContent = JSON.stringify(data, null, 2);
    
    // Show results
    document.getElementById('results').classList.remove('hidden');
}

/**
 * Conditionally render a list section based on item count
 * 
 * @param {string} listId - ID of the UL element
 * @param {string} sectionId - ID of the container DIV element
 * @param {Array} items - Array of items to check
 */
function renderListSection(listId, sectionId, items) {
    const listElement = document.getElementById(listId);
    const sectionElement = document.getElementById(sectionId);
    
    if (items && items.length > 0) {
        listElement.innerHTML = '';
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            listElement.appendChild(li);
        });
        sectionElement.classList.remove('hidden');
    } else {
        sectionElement.classList.add('hidden');
    }
}

function displayPlan(data) {
    const planSection = document.getElementById('planResults'); // Needs to be added to HTML
    if (!planSection) return; // Guard clause if HTML not updated yet

    planSection.classList.remove('hidden');
    
    // Strategy
    document.getElementById('strategyValue').textContent = data.execution_strategy;
    
    // Risks
    renderListSection('riskList', 'riskSection', data.risk_flags);
    
    // Success Criteria
    renderListSection('successList', 'successSection', data.success_criteria);
    
    // Resources
    renderListSection('resourceList', 'resourceSection', data.suggested_tools_or_resources);
    
    // Steps
    const stepList = document.getElementById('stepsList');
    stepList.innerHTML = '';
    data.recommended_next_steps.forEach(step => {
        const div = document.createElement('div');
        div.className = 'step-card';
        div.innerHTML = `
            <div class="step-num">${step.step}</div>
            <div class="step-content">
                <h4>${step.action}</h4>
                <p>${step.rationale}</p>
            </div>
        `;
        stepList.appendChild(div);
    });
}

/**
 * Toggle visibility of the Raw JSON section
 */
function toggleJson() {
    const wrapper = document.getElementById('jsonWrapper');
    const icon = document.getElementById('jsonToggleIcon');
    const isHidden = wrapper.classList.contains('hidden');
    
    if (isHidden) {
        wrapper.classList.remove('hidden');
        icon.textContent = '▼';
    } else {
        wrapper.classList.add('hidden');
        icon.textContent = '▶';
    }
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').classList.remove('hidden');
}

function copyJSON(event) {
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
