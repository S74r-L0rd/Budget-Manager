// Wait for DOM to fully load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all categories to be collapsed
    initializeCategories();
    
    // Add event listeners to amount inputs and period selects
    setupInputListeners();
    
    // Add event listener to view period selector
    document.getElementById('view-period').addEventListener('change', updateTotals);
    
    // Setup savings calculator functionality
    setupSavingsCalculator();
});

// Initialize all category details to be hidden
function initializeCategories() {
    // Get all category details elements and hide them initially
    const categoryDetails = document.querySelectorAll('.category-details');
    categoryDetails.forEach(detail => {
        detail.style.display = 'none';
    });
    
    // Calculate initial totals
    updateTotals();
}

// Setup input event listeners for amount changes and period changes
function setupInputListeners() {
    // Add event listeners to all amount inputs
    const amountInputs = document.querySelectorAll('.amount-input');
    amountInputs.forEach(input => {
        input.addEventListener('input', updateTotals);
    });
    
    // Add event listeners to all period selects
    const periodSelects = document.querySelectorAll('.period-select');
    periodSelects.forEach(select => {
        select.addEventListener('change', updateTotals);
    });
}

// Toggle category details visibility
function toggleCategory(categoryId) {
    const details = document.getElementById(`${categoryId}-details`);
    const toggleIcon = document.getElementById(`${categoryId}-toggle-icon`);
    
    if (details.style.display === 'none' || details.style.display === '') {
        details.style.display = 'block';
        toggleIcon.style.transform = 'rotate(180deg)';
    } else {
        details.style.display = 'none';
        toggleIcon.style.transform = 'rotate(0deg)';
    }
}

// Update all totals based on inputs and selected view period
function updateTotals() {
    // Get the selected view period
    const viewPeriod = document.getElementById('view-period').value;
    
    // Update category totals for all categories
    updateCategoryTotal('income');
    updateCategoryTotal('home');
    updateCategoryTotal('insurance');
    updateCategoryTotal('groceries');
    updateCategoryTotal('personal');
    updateCategoryTotal('entertainment');
    updateCategoryTotal('transport');
    updateCategoryTotal('children');
    updateCategoryTotal('education');
    updateCategoryTotal('gifts');
    
    // Update overall total
    updateOverallTotal();
}

// Update the total for a specific category
function updateCategoryTotal(categoryId) {
    let categoryTotal = 0;
    const viewPeriod = document.getElementById('view-period').value;
    
    // Find all amount inputs in this category
    const categoryItems = document.querySelectorAll(`#${categoryId}-details .budget-item`);
    
    categoryItems.forEach(item => {
        const amountInput = item.querySelector('.amount-input');
        const periodSelect = item.querySelector('.period-select');
        
        if (amountInput && periodSelect && amountInput.value) {
            const amount = parseFloat(amountInput.value) || 0;
            const period = periodSelect.value;
            
            // Convert amount to the view period
            const convertedAmount = convertAmount(amount, period, viewPeriod);
            categoryTotal += convertedAmount;
        }
    });
    
    // Update the category total in the UI
    const categoryAmount = document.querySelector(`#${categoryId}-category .category-amount`);
    if (categoryAmount) {
        categoryAmount.textContent = '$' + categoryTotal.toFixed(0);
    }
    
    return categoryTotal;
}

// Update the overall total
function updateOverallTotal() {
    // Income is positive
    const incomeTotal = updateCategoryTotal('income');
    
    // All other categories are expenses
    const homeTotal = updateCategoryTotal('home');
    const insuranceTotal = updateCategoryTotal('insurance');
    const groceriesTotal = updateCategoryTotal('groceries');
    const personalTotal = updateCategoryTotal('personal');
    const entertainmentTotal = updateCategoryTotal('entertainment');
    const transportTotal = updateCategoryTotal('transport');
    const childrenTotal = updateCategoryTotal('children');
    const educationTotal = updateCategoryTotal('education');
    const giftsTotal = updateCategoryTotal('gifts');
    
    // Total expenses
    const expensesTotal = homeTotal + insuranceTotal + groceriesTotal + personalTotal + 
                          entertainmentTotal + transportTotal + childrenTotal + 
                          educationTotal + giftsTotal;
    
    // Net balance
    const netBalance = incomeTotal - expensesTotal;
    
    // Update the summary total in the UI
    const totalAmount = document.querySelector('.budget-summary .total-amount');
    if (totalAmount) {
        totalAmount.textContent = '$' + netBalance.toFixed(0);
    }
}

// Convert amount between different periods
function convertAmount(amount, fromPeriod, toPeriod) {
    // Convert to annual amount first
    let annualAmount = 0;
    
    switch (fromPeriod) {
        case 'weekly':
            annualAmount = amount * 52;
            break;
        case 'fortnightly':
            annualAmount = amount * 26;
            break;
        case 'monthly':
            annualAmount = amount * 12;
            break;
        case 'annually':
            annualAmount = amount;
            break;
        default:
            annualAmount = amount;
    }
    
    // Convert from annual to target period
    switch (toPeriod) {
        case 'weekly':
            return annualAmount / 52;
        case 'monthly':
            return annualAmount / 12;
        case 'annually':
            return annualAmount;
        default:
            return annualAmount;
    }
}

// Format currency for display
function formatCurrency(amount) {
    return '$' + amount.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}

// Setup savings calculator functionality
function setupSavingsCalculator() {
    // Get form elements
    const savingsActionSelect = document.getElementById('savings-action');
    const savingsAmountTypeSelect = document.getElementById('savings-amount-type');
    const amountInputContainer = document.getElementById('amount-input-container');
    const specificAmountInput = document.getElementById('specific-amount');
    const timeAmountInput = document.getElementById('time-amount');
    const timeUnitSelect = document.getElementById('time-unit');
    const startingBalanceInput = document.getElementById('starting-balance');
    const interestRateInput = document.getElementById('interest-rate');
    const regularSavingsInput = document.getElementById('regular-savings');
    const savingsFrequencySelect = document.getElementById('savings-frequency');
    const calculateButton = document.getElementById('calculate-savings');
    const resetButton = document.getElementById('reset-savings');
    const savingsResults = document.getElementById('savings-results');
    
    // Add event listener to amount type select
    savingsAmountTypeSelect.addEventListener('change', function() {
        if (this.value === 'an-amount-of') {
            amountInputContainer.style.display = 'flex';
        } else {
            amountInputContainer.style.display = 'none';
        }
    });
    
    // Add event listener to calculate button
    calculateButton.addEventListener('click', function() {
        calculateSavings();
    });
    
    // Add event listener to reset button
    resetButton.addEventListener('click', function() {
        resetSavingsCalculator();
    });
    
    // Calculate savings based on inputs
    function calculateSavings() {
        // Get input values
        const isSpending = savingsActionSelect.value === 'spend';
        const isSpecificAmount = savingsAmountTypeSelect.value === 'an-amount-of';
        const specificAmount = parseFloat(specificAmountInput.value) || 0;
        const timeAmount = parseInt(timeAmountInput.value) || 1;
        const timeUnit = timeUnitSelect.value;
        const startingBalance = parseFloat(startingBalanceInput.value) || 0;
        const interestRate = parseFloat(interestRateInput.value) || 0;
        const regularSavings = parseFloat(regularSavingsInput.value) || 0;
        const savingsFrequency = savingsFrequencySelect.value;
        
        // Convert time to months
        let timeInMonths = 0;
        if (timeUnit === 'years') {
            timeInMonths = timeAmount * 12;
        } else {
            timeInMonths = timeAmount;
        }
        
        // Calculate frequency multiplier
        let frequencyMultiplier = 0;
        switch (savingsFrequency) {
            case 'weekly':
                frequencyMultiplier = 52 / 12;
                break;
            case 'fortnightly':
                frequencyMultiplier = 26 / 12;
                break;
            case 'monthly':
                frequencyMultiplier = 1;
                break;
            case 'quarterly':
                frequencyMultiplier = 1 / 3;
                break;
            case 'yearly':
                frequencyMultiplier = 1 / 12;
                break;
        }
        
        // Calculate final balance
        const monthlyInterestRate = interestRate / 100 / 12;
        const monthlySavings = regularSavings * frequencyMultiplier;
        let finalBalance = startingBalance;
        let totalDeposits = 0;
        
        for (let i = 0; i < timeInMonths; i++) {
            finalBalance += monthlySavings;
            totalDeposits += monthlySavings;
            
            // Apply interest
            finalBalance *= (1 + monthlyInterestRate);
        }
        
        // Calculate interest earned
        const interestEarned = finalBalance - startingBalance - totalDeposits;
        
        // Update results
        document.getElementById('final-balance').textContent = formatCurrency(finalBalance);
        document.getElementById('total-deposits').textContent = formatCurrency(totalDeposits);
        document.getElementById('interest-earned').textContent = formatCurrency(interestEarned);
        
        // Show results section
        savingsResults.style.display = 'block';
        
        // Generate tips based on calculations
        generateSavingsTips(monthlySavings, interestRate, savingsFrequency);
    }
    
    // Reset form inputs
    function resetSavingsCalculator() {
        savingsActionSelect.value = 'save';
        savingsAmountTypeSelect.value = 'as-much-as-possible';
        amountInputContainer.style.display = 'none';
        specificAmountInput.value = '';
        timeAmountInput.value = '1';
        timeUnitSelect.value = 'years';
        startingBalanceInput.value = '';
        interestRateInput.value = '';
        regularSavingsInput.value = '';
        savingsFrequencySelect.value = 'monthly';
        
        // Hide results section
        savingsResults.style.display = 'none';
    }
    
    // Generate personalized tips based on inputs
    function generateSavingsTips(monthlySavings, interestRate, savingsFrequency) {
        const tipsList = document.getElementById('savings-tips-list');
        tipsList.innerHTML = '';
        
        // Add tips based on inputs
        if (monthlySavings < 100) {
            addTip('Consider increasing your regular contributions to at least $100 per month');
        }
        
        if (interestRate < 3) {
            addTip('Look for savings accounts with higher interest rates (aim for 3% or higher)');
        }
        
        if (savingsFrequency === 'quarterly' || savingsFrequency === 'yearly') {
            addTip('Increase your deposit frequency to monthly or fortnightly for better compounding');
        }
        
        // Add standard tips
        addTip('Set up automatic transfers to your savings account');
        addTip('Review and reduce unnecessary expenses');
        
        function addTip(text) {
            const li = document.createElement('li');
            li.textContent = text;
            tipsList.appendChild(li);
        }
    }
}
