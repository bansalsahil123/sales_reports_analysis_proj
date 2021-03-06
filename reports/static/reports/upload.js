const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value 
const alertBox = document.getElementById('alert-box')
const handleAlerts = function(type,msg){
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">${msg} </div>`

}

Dropzone.autoDiscover = false
const myDropzone = new Dropzone('#my-dropozne', {
    url: '/reports/upload/',
    init: function() {
        this.on('sending', function(file, xhr, formData){
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success',function(file,response){
            console.log(response)
            if(response.ex){
                handleAlerts('danger','file already exist')
            }
            else{
                handleAlerts('success','file uploaded successfully')
            }


        })
    
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles: '.csv'
})