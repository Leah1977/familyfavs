$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('select').formSelect();
  
 
  // credit for code - Code Institute mini project

  validateMaterializeSelect();
  function validateMaterializeSelect() {
      let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
      let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
      if ($("select.validate").prop("required")) {
          $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
      }
      $(".select-wrapper input.select-dropdown").on("focusin", function () {
          $(this).parent(".select-wrapper").on("change", function () {
              if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                  $(this).children("input").css(classValid);
              }
          });
      }).on("click", function () {
          if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
              $(this).parent(".select-wrapper").children("input").css(classValid);
          } else {
              $(".select-wrapper input.select-dropdown").on("focusout", function () {
                  if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                      if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                          $(this).parent(".select-wrapper").children("input").css(classInvalid);
                      }
                  }
              });
          }
      });
  }
});

// end credit

const checkPasswordMatch = () => {
let password = document.getElementById('password');
let confirmPassword = document.getElementById('confirm_password');
let btnRegister = document.querySelector('.btn-register');
let btnLogin = document.querySelector('btn-login');
let strengthMeter = document.getElementById('strength-meter');

passwordInput.addEventListener('input', updateStrengthMeter)
updateStrengthMeter()

function updateStrengthMeter() {
    let weakPassword = calculatePasswordStrength
    (passwordInput.value)

    let strength = 100
    weakPassword.forEach(weakPassword => {
        if (weakPassword == null) return
        strength -= weakPassword.deduction
    })
        strengthMeter.style.setProperty('--strength', strength)
    }

    function calculatePasswordStrength(password){
        let weakPasswords = []
        weakPassword.push(lengthWeakPassword(password))
        return weakPassword
    }

    function lengthWeakPassword(password) {
        let length = password.length

        if(length <= 6) {
            return { 
                message: 'Your password is too short',
                deduction: 40
            }
        }

        if (length <= 10) {
            return { 
                message: 'Your password could be longer',
                deduction: 15
            }
        }

        if (length <= 10) {
            return { 
                message: 'Your password could be longer',
                deduction: 15
            }
        }

    }
    if (password.value !== confirmPassword.value) {
        
    }

}

