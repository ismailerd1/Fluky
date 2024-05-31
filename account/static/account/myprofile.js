function enterEditMode(){
    var about= document.querySelector('.about')
    var hidden_about=document.querySelector('.hidden_about')
    var edit_icon= document.querySelector('.edit_icon')
    var save_btn= document.querySelector('.save_btn')
    var mybio= document.querySelector('.mybio')
    var mytags= document.querySelector('.mytags')
    var input_area = document.querySelector('#input_area')
    var tag_area = document.querySelector('#tag_area')



    input_area.value = mybio.textContent.trim();
    tag_area.value = mytags.textContent.trim();

    document.querySelector('.mybio').textContent= '';
    document.querySelector('.mytags').textContent= '';

    about.style.display='none';
    hidden_about.style.display='block';
    edit_icon.style.display= 'none';
    save_btn.style.display='block';
    

}


function updateppmode(){
    var updatesec = document.querySelector('.update_sec')
    var update_btn = document.querySelector('.update_btn')

    update_btn.style.display='none';
    updatesec.style.display='block';
    



}
