/*ENLARGING WIREFRAME IMAGE ON CLICK*/
(function () {
    $('.wireframe_small').on('click', function () {
        $(this).toggleClass('wireframe_medium')
    })
})()