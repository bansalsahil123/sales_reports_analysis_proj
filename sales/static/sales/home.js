console.log('sssss')
const report_btn = document.getElementById("report-btn")
const img = document.getElementById('img')
const modal_body = document.getElementById('modal-body')
const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const reportForm = document.getElementById('report-form')
const alertBox = document.getElementById('alert-box')

    

console.log(report_btn)
console.log(img)
console.log("ssssa")
console.log(modal_body)

if (img){

    report_btn.classList.remove('not-visible')
}

const handleAlerts = function(type,msg){
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">${msg} </div>`

}


report_btn.addEventListener('click',()=>{
    console.log('clicked')
    img.setAttribute('class','w-100')
    modal_body.prepend(img)

    reportForm.addEventListener('submit',function(e){
        e.preventDefault()
        console.log("Submit cliecked befoe")
        const formData= new FormData()
        formData.append('csrfmiddlewaretoken',csrf)
        formData.append('name',reportName.value),
        formData.append('remarks',reportRemarks.value)
        formData.append('img',img.src)
        console.log(reportName.value)

        $.ajax({
            type:'POST',
            url:'/reports/save/',
            data:formData,
            success:function(response){

                console.log(response)
                handleAlerts('success','Report created') 
            },
            error: function(error){
                console.log(error)
                handleAlerts('danger','ups...wrong')
            },
            processData: false,
            contentType: false,
        })
    })



     

})
