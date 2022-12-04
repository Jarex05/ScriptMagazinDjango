$(document).ready(function () {
    var form = $("#form_buying_product");
    console.log(form);

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
                    console.log(data.products);
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
});








{/* <div class="row g-3 form_buying_product" >

<div class="col-3">
    <input type="number" class="form-control number" name="number" min="1" value="1">
</div>
<div class="col-auto">
     <button type="submit" class="btn btn-warning submit_btn"
                             data-product_id="{{ product_img.product.id }}"
                             data-name="{{ product_img.product.title }}"
                             data-price="{{ product_img.product.price }}"


     >в корзину</button>
</div>
</div> */}






$(document).ready(function(){
 
    function basketUpdating(product_id, nmb, is_delete){
        var data ={};
        data.product_id = product_id;
        data.nmb = nmb;
        var csrf_token ={% csrf_token %}; // тут я напрямую вставил токен
        data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data['is_delete'] = true
        }

         
        $.ajax({
            url: ajax_url ,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                if (data.products_total_nmb || data.products_total_nmb == 0){
                    $('#basket_total_nmb').text(data.products_total_nmb)
                    $('.basket-items ul').html("");
                    $.each(data.products, function(k, v){
                        $('.basket-items ul').append('<li>'+v.name+', '+v.nmb+' шт. '+' по '+v.price_per_item+' руб ' +
                      '<a class="delete-item" href="" data-product_id="'+v.id+'">X</a>'+
                        '</li>');
                    });
                }
            }
        })
    }
    $(".submit_btn").on('click', function(e){
        e.preventDefault();
        var nmb = $(this).closest(".row").find('.number').val();
         var product_id = $(this).data('product_id');
        var product_name =  $(this).data('name');
        var product_price =  $(this).data('price');
   var ajax_url =  $(this).data('url');
       basketUpdating(product_id, nmb, is_delete=false);