function handleContactForm(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    if (name && email && message) {
        alert(`Thank you, ${name}, for reaching out! We'll contact you at ${email} soon.`);
    } else {
        alert("Please complete all fields before submitting the form.");
    }
    document.getElementById('contactForm').reset();
}
function selectPlan(planName) {
    document.getElementById('plan').value = planName;
    window.scrollTo({
        top: document.querySelector('.form-container').offsetTop,
        behavior: 'smooth'
    });
}

function handleFormSubmission(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const plan = document.getElementById('plan').value;

    if (name && plan) {
        alert(`Thank you for registering, ${name}! You have selected the ${plan}.`);
    } else {
        alert("Please complete all fields before submitting.");
    }

    document.getElementById('registrationForm').reset();
}