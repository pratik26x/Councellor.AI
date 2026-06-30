document.querySelectorAll('.faq-item').forEach(item => {
    item.querySelector('.question').addEventListener('click', () => {
        const answer = item.querySelector('.answer');
        const toggleIcon = item.querySelector('.toggle-icon');
        
        if (answer.style.display === 'block') {
            answer.style.display = 'none';
            toggleIcon.textContent = '+';
            toggleIcon.style.transform = 'rotate(0deg)';
        } else {
            answer.style.display = 'block';
            toggleIcon.textContent = '-';
            toggleIcon.style.transform = 'rotate(45deg)';
        }
    });
});

const contactButton = document.querySelector('.horizantal-menu a.contact-button');


contactButton.addEventListener('click', function(event) {
    event.preventDefault(); 


    document.querySelector('.contact').scrollIntoView({ 
        behavior: 'smooth' 
    });
    
});
