$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})
$('.plus-cart').click(function () {
    var id=$(this).attr('pid').toString();
    /*console.log(id)*/
    var eml=this.parentNode.children[2]
    /* the above eml can store the last node of current quantity. this is for printing to quantity total amount
    in the output page*/
    /*console.log(id)*/
    $.ajax(
        {
            type:'GET',
            url:"/pluscart",
            data:{
                prod_id:id
            },
            success:function (data) {
                eml.innerText=data.quantity
                document.getElementById("amount").innerText=data.amount
                document.getElementById("totalamount").innerText=data.totalamount
                /*get element by id can fatch data from add to cart.html because there we define
                class id for amount and total amount*/
                
            }
        })
})
/*here .plus cart is the class name in add to cart.html... while we click on + at
that time function is called here this is current class object. from here we get id of product
this product we will send to the view  we are sending data whith the help of ajax*/
$('.minus-cart').click(function () {
    var id=$(this).attr('pid').toString();
    var eml=this.parentNode.children[2];
    $.ajax(
        {
            type:'GET',
            url:"/minuscart",
            data:{
                prod_id:id
            },
            success:function (data) {

                eml.innerText=data.quantity
                document.getElementById("amount").innerText=data.amount
                document.getElementById("totalamount").innerText=data.totalamount


            }
        })
})

$('.remove-cart').click(function () {
    var id=$(this).attr('pid').toString();
    var eml=this
    $.ajax(
        {
            type:'GET',
            url:"/removecart",
            data:{
                prod_id:id
            },
            success:function (data) {
                console.log("Delete")
                document.getElementById("amount").innerText=data.amount
                document.getElementById("totalamount").innerText=data.totalamount
                eml.parentNode.parentNode.parentNode.parentNode.remove()

            }
        })
})