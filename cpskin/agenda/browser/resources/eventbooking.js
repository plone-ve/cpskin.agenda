// jquery for search button in navigation 

$( document ).ready(function() {
       $(".toggle-button").click(function( event ){
         var toggle_button_id = this.id;
         var toggle_block_id = toggle_button_id.replace("-button", "-block");
         $("#" + toggle_block_id).toggleClass("active desactive");
         event.stopImmediatePropagation();
       });
});

