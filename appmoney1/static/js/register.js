const usernameField=document.querySelector('#usernameField');
const feedbackArea=document.querySelector('.invalid_feedback');
const emailField=document.querySelector('#emailField');
const emailFeedbackArea = document.querySelector('.emailFeedbackArea');
const passwordField=document.querySelector('#passwordField');
const usernameSuccessOut = document.querySelector('.usernameSuccessOut');
const emailSuccessOut = document.querySelector('.emailSuccessOut');
const showPassword=document.querySelector('.showPassword');
const submitBtn=document.querySelector('.submit-btn');


const handleToggleInput=(e)=>{
if(showPassword.textContent==='SHOW'){
showPassword.textContent='HIDE';
passwordField.setAttribute('type','text');
}else{
showPassword.textContent='SHOW';
passwordField.setAttribute('type','password');
}

};


showPassword.addEventListener('click', handleToggleInput);

emailField.addEventListener('keyup', (e) => {

    const emailVal=e.target.value;
    emailSuccessOut.style.display='block';
    emailSuccessOut.textContent=`Checking ${emailVal}`;

    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display='none';


    if (emailVal.length > -10){

        fetch("/authentication/validate-email",{
            body: JSON.stringify(emailVal),
            method: 'post',

            })
        .then(response => response.json())
        .then(data => {
        console.log('data', data);
        emailSuccessOut.style.display='none';
        if (data.email_error){

        submitBtn.disabled=true;
        emailField.classList.add('is-invalid');
        emailFeedbackArea.style.display='block';
        emailFeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
        }else{
        submitBtn.removeAttribute('disabled');
        }
        });

    }
});

usernameField.addEventListener('keyup', (e) => {

    const usernameVal=e.target.value;
    usernameSuccessOut.style.display='block';
    usernameSuccessOut.textContent=`Checking ${usernameVal}`;

    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display='none';


    if (usernameVal.length > -10){

        fetch("/authentication/validate-username",{
            body: JSON.stringify(usernameVal),
            method: 'post',

            })
        .then(response => response.json())
        .then(data => {
        console.log('data', data);
        usernameSuccessOut.style.display='none';
        if (data.username_error){
        usernameField.classList.add('is-invalid');
        feedbackArea.style.display='block';
        feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
        submitBtn.disabled=true;
        }else{
        submitBtn.removeAttribute('disabled');
        }
        });

    }
});