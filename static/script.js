document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const predictBtn = document.getElementById('predictBtn');
    const predictionResult = document.getElementById('predictionResult');
    const errorMessage = document.getElementById('errorMessage');
    const salaryResult = document.getElementById('salaryResult');
    const errorText = document.getElementById('errorText');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset messages
        predictionResult.style.display = 'none';
        errorMessage.style.display = 'none';
        
        // Show loading state
        predictBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Predicting...';
        predictBtn.disabled = true;
        form.classList.add('loading');

        try {
            // Get form data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Convert numeric fields
            data.Total_Experience = parseFloat(data.Total_Experience);
            data.Total_Experience_in_field_applied = parseFloat(data.Total_Experience_in_field_applied);
            data.Current_CTC = parseFloat(data.Current_CTC);
            data.No_Of_Companies_worked = parseInt(data.No_Of_Companies_worked);
            data.Passing_Year_Of_Graduation = parseInt(data.Passing_Year_Of_Graduation);
            data.Number_of_Publications = parseInt(data.Number_of_Publications);
            data.Certifications = parseInt(data.Certifications);
            data.International_degree_any = parseInt(data.International_degree_any);

            // Handle optional fields
            if (!data.Passing_Year_Of_PG) data.Passing_Year_Of_PG = '';
            if (!data.Passing_Year_Of_PHD) data.Passing_Year_Of_PHD = '';

            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                // Display prediction result
                salaryResult.textContent = result.formatted_salary;
                predictionResult.style.display = 'block';
                
                // Smooth scroll to result
                predictionResult.scrollIntoView({ behavior: 'smooth' });
            } else {
                // Display error
                errorText.textContent = result.error || 'An error occurred during prediction.';
                errorMessage.style.display = 'block';
            }

        } catch (error) {
            console.error('Error:', error);
            errorText.textContent = 'Network error. Please try again.';
            errorMessage.style.display = 'block';
        } finally {
            // Reset button state
            predictBtn.innerHTML = 'Predict Expected CTC';
            predictBtn.disabled = false;
            form.classList.remove('loading');
        }
    });

    // Real-time validation for numeric inputs
    const numericInputs = form.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const min = parseFloat(this.min);
            const max = parseFloat(this.max);
            const value = parseFloat(this.value);
            
            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });

    // Dynamic form behavior based on education level
    const educationSelect = form.querySelector('select[name="Education"]');
    
    function updateFormForEducation() {
        const educationLevel = educationSelect.value;
        // You can add dynamic behavior here based on education level
        console.log('Education level changed to:', educationLevel);
    }
    
    educationSelect.addEventListener('change', updateFormForEducation);
});