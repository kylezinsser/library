// Feels a bit hacky, but this lets me re-use the Flask-WTForms for both adding and deleting resources
if (window.location.href.substring(window.location.href.lastIndexOf('/') + 1) == 'add')
    $('#delete').hide();
        
$(document).ready(function(){

    $('#delete').click(function(event){
        event.preventDefault();

        url = window.location.href;
        delete_url = url.substring(0, url.lastIndexOf('/'));

        console.log("Deleting: " + delete_url);
        deleteResource(delete_url);
    })

    function deleteResource(url) {
        $.ajax({
            url: url,
            type: 'DELETE',
            success: function (result) {
                if(result.success == true)
                    window.location.replace(url.substring(0, url.lastIndexOf('/')));
            }
        });
    }

});