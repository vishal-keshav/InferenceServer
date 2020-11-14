// initialize dropzone
Dropzone.autoDiscover = true;
var myDropzone = new Dropzone(
    "#droparea",
    {
        autoProcessQueue: true,  // means that the queue of files will process immediately after 'success'
        // ..your other parameters..

        url: "/uploadajax",  // connects to uploadfile in app.py
        paramName: "file", // The name that will be used to transfer the file
        maxFilesize: 1.0, // MB
        uploadMultiple: false, //Don't permit multiple uploads
        accept: function(file, done) {
            console.log("uploaded");
            done();
        },
        init: function() {  // I believe this removes an old file if a new file is added, see https://stackoverflow.com/questions/18048825/how-to-limit-the-number-of-dropzone-js-files-uploaded
            this.on("addedfile", function() {
              if (this.files[1]!=null){
                this.removeFile(this.files[0]);
              }
            });
        },
        success: function(file,response) {
            console.log('success');
            console.log(response);
            document.getElementById("output-text").innerHTML = response.replace(/\n/g, '<br>');
        }

    }
);

function default_option()
{
    $.ajax({
        type: "POST",
        url: "/radio_button",
        data: JSON.stringify({"radio_sel" : $(".radio_sel:checked").val()}),  // converts to json that can be read by python
        success: function(response) {
            document.getElementById("output-text").innerHTML = response.replace(/\n/g, '<br>');
            console.log('radio button success');
        },
        error: function() {
            console.log('error in get request for radio button');
        }
    });
}

// This just clicks the first button to populate the initial results
$(document).ready(function() {
   $(".radio_sel:checked").trigger('click');
});
