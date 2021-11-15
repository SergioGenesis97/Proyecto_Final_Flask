var TxtNombre = document.getElementById('txtUsername');
var TxtPass = document.getElementById('txtPass');
var TxtCorreo = document.getElementById('txtCorreo');
var LabelImg = document.getElementById('txtFoto');
var Error = document.getElementById('DivError');

function enviarForm(){

    var mensajeError = [];
    
    if(TxtNombre.value == null || TxtNombre.value == ''){
        mensajeError.push('Ingresa un Username!');
    }

    if(TxtPass.value == null || TxtPass.value == ''){
        mensajeError.push('Ingresa una Password!');
    }

    if(TxtCorreo.value == null || TxtCorreo.value == ''){
        mensajeError.push('Ingresa un Correo!');
    }

    if(LabelImg.value == null || LabelImg.value == ''){
        mensajeError.push('Añade una Imagen!');
    }

    Error.style.color = 'red';
    Error.innerHTML = mensajeError.join(', ');

    console.log('Guardando Formulario...');
    return false;
}

function LlamarError(contenedor, mensaje){

    var contenedorError = document.getElementById(contenedor);
    var mensajeError = document.createElement("P")

    mensajeError.innerText = mensaje;
    mensajeError.style.backgroundColor = "#dbb4b5";
    mensajeError.style.color = "#cf1b21";  
    mensajeError.className = "mensaje-error";
    contenedorError.appendChild(mensajeError);

    setTimeout(()=>{
        mensajeError.remove();
    }, 4000)
}


function ValidaEdicion(){
    
    valorTexto = document.getElementById('txtUsername').value;
    valorPass = document.getElementById('txtPass').value;
    valorCorreo = document.getElementById('txtCorreo').value;
    // image = document.getElementById("txtFoto").value;

    if(valorTexto == null || valorTexto.length == 0){
        LlamarError("DivErrorUsuario", "El campo de usuario es obligatorio")
        return false;
    }else if(valorPass == null || valorPass.length == 0){
        LlamarError("DivErrorPass", "El campo de contraseña es obligatorio");
        return false;
    }else if(valorCorreo == null || valorCorreo.length == 0){
        LlamarError("DivErrorCorreo", "El campo de correo es obligatorio");
        return false;
    // 
    }
    //else if(image == null  || image.length == 0){
    //     LlamarError("DivErrorIMG", "La imagen del usuario es obligatoria");
    //     return false;
    // }
    return true;
}