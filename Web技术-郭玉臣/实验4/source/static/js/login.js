const container = document.querySelector('#container');
const signInSwitchButton = document.querySelector('#signIn');
const signUpSwitchButton = document.querySelector('#signUp');
const signInSubmitButton = document.getElementById('signInForm');
const signInPwd = document.getElementById('signInPwd');
const signInPwdMd5 = document.getElementById('signInPwdMd5');
const signUpPwd = document.getElementById('signUpPwd');
const signUpPwdMd5 = document.getElementById('signUpPwdMd5');



signUpSwitchButton.addEventListener('click', () => 
    container.classList.add('right-panel-active')
);

signInSwitchButton.addEventListener('click', () => 
    container.classList.remove('right-panel-active')
);

function signInEncryption(){
    signInPwdMd5.value = md5(signInPwd.value);
}

function signUpEncryption(){
    signUpPwdMd5.value = md5(signUpPwd.value);
}
