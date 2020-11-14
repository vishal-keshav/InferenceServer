// transform cropper dataURI output to a Blob which Dropzone accepts
// function dataURItoBlob(dataURI) {
//     var byteString = atob(dataURI.split(',')[1]);
//     var ab = new ArrayBuffer(byteString.length);
//     var ia = new Uint8Array(ab);
//     for (var i = 0; i < byteString.length; i++) {
//         ia[i] = byteString.charCodeAt(i);
//     }
//     return new Blob([ab], { type: 'image/jpeg' });
// }

// modal window template
var modalTemplate = '<div class="modal" tabindex="-1">'+
                        <!-- bootstrap modal here -->
                        '<h2>Crop as close to the border as possible</h2>'+
                        '<div class="image-container"></div>'+
                        '<div class="buttons">'+
                            '<button type="button" class="reset">Reset</button>'+
                            '<button type="button" class="crop-upload">Submit</button>'+
                        '</div>'+
                    '</div>';

// initialize dropzone
Dropzone.autoDiscover = false;
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
            document.getElementById("output-text").textContent = response;
        }

    }
);

// listen to thumbnail event
// myDropzone.on('thumbnail', function (file) {
//     if (file.width < 50) {
//         // validate width to prevent too small files to be uploaded
//         // .. add some error message here
//         return;
//     }
//     // cache filename to re-assign it to cropped file
//     //var cachedFilename = file.name;
//     //I dont need this since I'm changing filename
//
//     // remove not cropped file from dropzone (we will replace it later)
//     myDropzone.removeFile(file);
//
//     // initialize FileReader which reads uploaded file
//     var reader = new FileReader();
//     reader.onloadend = function () {
//         // add uploaded and read image to modal
//         $img.attr('src', reader.result);
//     };
//     // read uploaded file (triggers code above)
//     reader.readAsDataURL(file);
//
//     var blob = $img.cropper('getCroppedCanvas',{fillColor:'#ffffff'}).toDataURL();
//     // transform it to Blob object
//     var newFile = dataURItoBlob(blob);
//
//     // assign original filename
//     //newFile.name = cachedFilename;
//     newFile.name = 'user_image.jpg'
//
//     myDropzone.addFile(newFile);
//     // upload file with dropzone
//     myDropzone.processQueue();
//
// });
