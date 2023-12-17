function nextSlide(slideNumber) {
    const currentSlide = document.querySelector('.slide.active');
    if (currentSlide) {
        currentSlide.classList.remove('active');
    }
    const nextSlide = document.getElementById('slide' + slideNumber);
    if (nextSlide) {
        nextSlide.classList.add('active');
    }

    if(slideNumber == 2){
        send_vk_id();
    }
    if(slideNumber == 3){
        send_question();
        send_gigachat();
    }
}

// Активируем первый слайд при загрузке
window.onload = function() {
    nextSlide(1);
};
