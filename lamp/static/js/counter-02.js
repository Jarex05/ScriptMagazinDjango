// Добавляем прослушку на всем окне

window.addEventListener('click', function (event) {

    // Обьявляем переменную для счетчика
    let counter;

    // Проверяем клик строго по кнопкам Плюс либо Минус
    if (event.target.dataset.action === 'plus' || event.target.dataset.action === 'minus') {

            // Находим обертку счетчика
        const counterWrapper = event.target.closest('.counter-wrapper');

        // Находим див с числом счетчика для его изменения
        counter = counterWrapper.querySelector('[data-counter]');

    }


    // Проверяемб является ли элемент по которому был совершен клик кнопкой Плюс
    if (event.target.dataset.action === 'plus') {

        counter.innerText = ++counter.innerText;
    }

    // Проверяемб является ли элемент по которому был совершен клик кнопкой Минус
    if (event.target.dataset.action === 'minus') {
       
        // Проверяем чтобы счетчик был больше 1
        if ( parseInt(counter.innerText) > 1 ) {

            // Изменяем текст в счетчике, уменьшая его на 1 и не ниже 0
            counter.innerText = --counter.innerText;
        } else if (event.target.closest('.cart-wrapper') && parseInt(counter.innerText) === 1) {

            // Удаляем товар из корзины
            event.target.closest('.cart-item').remove();

            // Отображение статуса корзины: Пустая / Полная
            toggleCartStatus();

            // Пересчет общей стоимости товара в корзине
            calcCartPrice();

        }

    }

    // Проверяем клик на + или - внутри корзины
    if (event.target.hasAttribute('data-action') && event.target.closest('.cart-wrapper')) {

        // Пересчет общей стоимости товара в корзине
        calcCartPrice();

    }


});


