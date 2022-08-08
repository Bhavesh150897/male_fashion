$('.plus-cart').click(function () {
    var id = $(this).attr("pid");
    var eml = $(this);
    $.ajax(
        {
            type: "GET",
            url: "/pluscart",
            data: {
                prod_id: id
            },
            success: function (data) {
                $('.quantity-val-'+data.prod_id).val(data.quantity)
                $('#amount').text('$ ' + data.amount);
                $('#totalamount').text('$ ' + data.totalamount);
            }
        })
});

$('.minus-cart').click(function () {
    var id = $(this).attr("pid");
    var eml = $(this);
    $.ajax(
        {
            type: "GET",
            url: "/minuscart",
            data: {
                prod_id: id
            },
            success: function (data) {
                $('.quantity-val-'+data.prod_id).val(data.quantity)
                $('#amount').text('$ ' + data.amount);
                $('#totalamount').text('$ ' + data.totalamount);
            }
        })
});

$('.remove-cart').click(function () {
    var id = $(this).attr("pid");
    var elm = $(this);
    $.ajax(
        {
            type: "GET",
            url: '/removecart',
            data: {
                prod_id: id
            },
            success: function (data) {
                $('.main-tr-'+data.prod_id).remove();
                $('#amount').text('$ ' + data.amount);
                $('#totalamount').text('$ ' + data.totalamount);
            }
        })
});

$('body').on('click','.add-favourite',function (argument) {
    var obj = $(this);
    id = $(this).data("id");
    $.ajax({
        type: "GET",
        url: `/product/${id}/favourites`,
        success: function (data) {
            if (data.product == true) {
                obj.html('<i class="fa fa-heart fill-color"></i> Delete From Favourite');
                toastr.success('Product Add to Favourite Successfully!')
            }else{
                obj.html('<i class="fa fa-heart"></i> Add to Favourite');
                toastr.success('Product Delete From Favourite Successfully!')
            }
        },
    });
})

$('body').on('click','.shop-add-to-fav',function (argument) {

    var obj = $(this);
    id = $(this).data("id");
    
    $.ajax({
        type: "GET",
        url: `/product/${id}/favourites`,
        success: function (data) {
            if (auth == 'False') {
                toastr.error('Oops!, You have not logged in!')
            }else{
                if (data.product == true) {
                    obj.html('<i class="fa fa-heart fill-color"></i>');
                    toastr.success('Product Add to Favourite Successfully!')
                }else{
                    obj.html('<i class="fa fa-heart"></i>');
                    toastr.success('Product Delete From Favourite Successfully!')
                }
            }
        },
    });
})
