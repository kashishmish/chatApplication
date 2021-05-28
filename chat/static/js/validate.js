var pattern1=/^[a-zA-Z ]{3,}$/;
var pattern2=/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
var pattern3=/^[a-zA-Z0-9]{5,}$/;
var pattern4=/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$/;
function name_confirm()
{
    var name=document.getElementById("full_name").value;
    var name_statu=document.getElementById("name_status");
    if(name.match(pattern1))
    {
        name_statu.innerHTML="Correct";
        name_statu.style.color="green";
    }
    else
    {
        name_statu.innerHTML="Invalid Name";
        name_statu.style.color="red";
    }
}
function email_confirm()
{
    var email=document.getElementById("full_email").value;
    var email_statu=document.getElementById("email_status");
    if(email.match(pattern2))
    {
        email_statu.innerHTML="Correct";
        email_statu.style.color="green";
    }
    else
    {
        email_statu.innerHTML="Invalid email";
        email_statu.style.color="red";
    }
}

function username_confirm()
{
    var username=document.getElementById("full_username").value;
    var username_statu=document.getElementById("username_status");
    if(username.match(pattern3))
    {
        username_statu.innerHTML="Correct";
        username_statu.style.color="green";
    }
    else
    {
        username_statu.innerHTML="Invalid username";
        username_statu.style.color="red";
    }
}

function confirm_password()
{
    var password=document.getElementById("full_password").value;
    var password_statu=document.getElementById("password_status");
    if(password.match(pattern4))
    {
        password_statu.innerHTML="Correct";
        password_statu.style.color="green";
    }
    else
    {
        password_statu.innerHTML="Invalid password";
        password_statu.style.color="red";
    }
}
function c_password_confirm()
{
    var password=document.getElementById("full_password").value;
    var c_password=document.getElementById("full_c_password").value;
    var c_password_statu=document.getElementById("c_password_status");
    if(password==c_password)
    {
        c_password_statu.innerHTML="Correct";
        c_password_statu.style.color="green";
    }
    else
    {
        c_password_statu.innerHTML="confirm password doesn't match";
        c_password_statu.style.color="red";
    }
}
function validate()
{
    var name=document.getElementById("full_name").value;
    var email=document.getElementById("full_email").value;
    var username=document.getElementById("full_username").value;
    var password=document.getElementById("full_password").value;
    var c_password=document.getElementById("full_c_password").value;
    if(name.match(pattern1))
    {
        if(email.match(pattern2))
        {
            if(username.match(pattern3))
            {
                if(password.match(pattern4))
                {
                    if(password==c_password)
                    {
                        alert("Now you are good to go")
                        return true;
                    }
                    else{
                        alert("confirm password doesn't matches with password");
                        return false;
                    }
                }
                else{
                    alert("password is weak");
                    return false;
                }
            }
            else{
                alert("username is invalid");
                return false;
            }
        }
        else{
            alert("Email is invalid");
            return false;
        }
    }
    else{
        alert("name is invalid");
        return false;
    }
}
