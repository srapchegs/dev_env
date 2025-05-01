// Когда html документ готов (прорисован)
$(document).ready(function () {
    function sendMessage() {
        const input = document.getElementById('user-input');
        const message = input.value.trim();
        if (message === '') return;
  
        const chatMessages = document.getElementById('chat-messages');
  
        // Отображаем сообщение пользователя
        const userMsg = document.createElement('div');
        userMsg.className = 'message user-message';
        userMsg.textContent = message;
        chatMessages.appendChild(userMsg);
  
        input.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;
  
        // Отправляем сообщение на сервер
        $.ajax({
          url: '/chat/answer/',
          method: 'POST',
          data: {
            message: message,
            csrfmiddlewaretoken: '{{ csrf_token }}'
          },
          success: function(data) {
            // Преобразуем текст, заменяя URL на кликабельную ссылку
            let response = data.response.replace(
              /(https?:\/\/[^\s]+)/g,
              '<a href="$1" target="_blank">$1</a>'
            );
            const botMsg = document.createElement('div');
            botMsg.className = 'message bot-message';
            botMsg.innerHTML = response;
            chatMessages.appendChild(botMsg);
            chatMessages.scrollTop = chatMessages.scrollHeight;
          },
          error: function(xhr) {
            const errorMsg = document.createElement('div');
            errorMsg.className = 'message bot-message';
            errorMsg.textContent = 'Ошибка: ' + xhr.statusText;
            chatMessages.appendChild(errorMsg);
            chatMessages.scrollTop = chatMessages.scrollHeight;
          }
        });
      }
      
    $(document).on("click", ".add-to-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        let goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var product_id = $(this).data("product-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");

        var svgNoAdded = $(this).find(".no_added");
        var svgAdded = $(this).find(".added");

        var btnNoAdded = $(document).find(".buttons-container-detail2");
        var btnAdded = $(document).find(".buttons-container-detail1");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                cartCount++;
                goodsInCartCount.text(cartCount);  
                svgNoAdded.removeClass("activeds");
                svgAdded.addClass("activeds"); 
                btnNoAdded.removeClass("activedz");
                btnAdded.addClass("activedz");  
            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });
    $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= 1;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });
    $(document).on('change', ".change-count", function() {
        var cartID = $(this).data('cart-id');
        var quantity = $(this).val();
        var url = $(this).data('cart-change-url');
        updateCart(cartID, quantity, url);
    });
    function updateCart(cartID, quantity, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);
            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    };
});