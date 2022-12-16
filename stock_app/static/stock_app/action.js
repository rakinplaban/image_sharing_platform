document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#image-upload').addEventListener('click', ()=> {
        document.querySelector('.bg-model').style.display = 'flex';
    });

    document.querySelector('.close').addEventListener('click', ()=> {
        document.querySelector('.bg-model').style.display = 'none';
    });
    // for(i=1;i<100;i++){
    //     if(document.querySelector(`#image-detail-${i}`) != null){
    //     document.querySelector(`#image-detail-${i}`).addEventListener('click', ()=> {
    //         document.querySelector('.bg-model-1').style.display = 'flex';
    //     });
    //     }
    // }
    document.querySelector('#image-detail').addEventListener('click', ()=> {
        document.querySelector('.bg-model-1').style.display = 'flex';
    });

    document.querySelector('.close-1').addEventListener('click', ()=> {
        document.querySelector('.bg-model-1').style.display = 'none';
    });

    
    // Add like
    $(".add-wishlist").on('click',function(){
        var _pid = $(this).data('image');
        var _btn = $(this);
        console.log(_pid)
        $.ajax({
            url : "/add-wishlist",
            data:{
                image_id : _pid
            },
            dataType:'json',
            success : function(res){
                if (res.bool == true){
                    _btn.addClass('remove-wishlist').removeClass('add-wishlist');
                }

            }
        });  
    });

    $(".remove-wishlist").on('click',function(){
        var _pid = $(this).data('image');
        var _btn = $(this);
        console.log(_pid)
        $.ajax({
            url : "/remove-wishlist",
            data:{
                image_id : _pid
            },
            dataType:'json',
            success : function(res){
                if (res.bool == true){
                    _btn.addClass('add-wishlist').removeClass('remove-wishlist');
                }

            }
        });  
    });
    // Endlike

})