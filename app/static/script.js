// Feels a bit hacky, but this lets me re-use the Flask-WTForms for both adding and deleting resources
if (window.location.href.substring(window.location.href.lastIndexOf('/') + 1) == 'add')
    $('#delete').hide();
        
$(document).ready(function(){

    $("form input:text").first().focus();

    $('#delete').click(function(event){
        event.preventDefault();

        if (confirm('Are you sure you want to delete this entry?')) {
            url = window.location.href;
            delete_url = url.substring(0, url.lastIndexOf('/'));
    
            console.log("Deleting: " + delete_url);
            deleteResource(delete_url);
        } else {
            console.log('Deletion cancelled.');
        }
    })
    
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

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