function calcCartPrice() {

    const cartWrapper = document.querySelector('.cart-wrapper');
    const priceElements = cartWrapper.querySelectorAll('.price__currency');

    const totalPriceEl = document.querySelector('.total-price');

    // Общая стоимость товара
    let priceTotal = 0;
    

    // Обходим все блоки с ценами в корзине
    priceElements.forEach(function (item) {

        // Находим колличество товара
        const amountEl = item.closest('.cart-item').querySelector('[data-counter]');
        // Добавляем стоимость товара в общую стоимость (кол-во * цену)
        priceTotal += parseInt(item.innerText) * parseInt(amountEl.innerText);
        
    });

    //Отображаем цену на странице
    totalPriceEl.innerText = priceTotal;

}