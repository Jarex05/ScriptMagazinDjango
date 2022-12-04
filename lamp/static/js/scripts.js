$(document).ready(function () {
    var form = $("#form_buying_product");
    console.log(form);
    var cartEmptyBadge = document.querySelector('[data-cart-empty]');

    function basketUpdating(product_id, nmb, is_delete) {
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete) {
            data["is_delete"] = true;
        }

        var url = form.attr("action");

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("OK");
                console.log(data.products_total_nmb);
                if (data.products_total_nmb || data.products_total_nmb == 0) {
                    $('#basket_total_nmb').text("(" + data.products_total_nmb + ")");
                    $('#basket_total_amount').text(  data.order_total_price );
                    console.log(data.products.length);
                    $('.cart-wrapper').html("");
                    
                                $.each(data.products, function(k, v){
                                    
                                    $('.cart-wrapper').append(`<div class="cart-item">
                                                        <div class="cart-item__top">
                                                        <div class="cart-item__img">
                                                            <img src="` + v.image + `" alt="">
                                                        </div>
                                                        <div class="cart-item__desc">
                                                            <div class="cart-item__title">` + v.name + `</div>
                                                            <div class="cart-item__weight">6 шт. / 205г.</div>
                                                            
                                                                    
                                                            <div class="cart-item__details">
                                                            
                                                                <div class="items items--small counter-wrapper">
                                                                    <div class="items__control" data-action="minus">-</div>
                                                                    <div class="items__current" data-counter="">` + v.nmb + `</div>
                                                                    <div class="items__control" data-action="plus">+</div>
                                                                </div>
                                                            
                                                                <div class="price">
                                                                    <div class="price__currency">` + v.price_per_item + ` ₽</div>
                                                                </div>
                                                                        
                                                            </div>
                                                        </div>
                                                        <a class="delete-item" href="" data-product_id="` + v.id + `">x</a>
                                                        </div>
                                                                
                                                    </div>`)
                                    
                                });
                                if(data.products.length > 0) {
                                    cartEmptyBadge.classList.add('none');
                                } else {
                                    cartEmptyBadge.classList.remove('none');
                                }
                          
                }
            },
            error: function () {
                console.log("error");
            }
        })
    }
    $(document).on('click', "#submit_btn", function(e) {
        e.preventDefault();
        var nmb = $(this).closest(".card").find('#number').val();
        var product_image = $(this).data("image");
        var product_id = $(this).data('product_id');
        var product_name =  $(this).data('name');
        var product_price =  $(this).data('price');
        console.log(product_id);
        console.log(product_image);
        console.log(product_name);
        console.log(nmb);
        console.log(product_price);
        
        basketUpdating(product_id, nmb, is_delete=false)

    });

    $(document).on('click', '.delete-item', function (e) {
        e.preventDefault();
        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true)
    });

    function calculatingBasketAmount() {
        var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function () {
            total_order_amount += parseFloat($(this).text());
        });
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };
    $(document).on('change', ".product-in-basket-nmb", function () {
        var current_nmb = $(this).val();
        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        console.log(current_price);
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2);
        console.log(total_amount);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);
        

        calculatingBasketAmount();
    });

    calculatingBasketAmount();
});