// Set test input to variable
textInput = document.getElementById('formula-name');
// Set image input to variable
imageInput = document.getElementById('formula-image');

/*
If text in input, image input disabled + is no longer required
If text not in input, image input enabled + is required
*/
textInput.addEventListener('input', () => {
    if (textInput.value == '') {
        imageInput.disabled = false
        imageInput.removeAttribute('required')
    } else {
        imageInput.disabled = true 
        imageInput.setAttribute('required', '')
    }
})

/* 
If image inputted, text input disabled + is no longer required
If image not inputted, text input enabled + is required
*/
imageInput.addEventListener('input', () => {
    if (imageInput.value == '') {
        textInput.disabled = false 
        textInput.removeAttribute('required')
    } else {
        textInput.disabled = true 
        textInput.setAttribute('required', '')
    }
})