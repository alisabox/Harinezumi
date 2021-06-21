const password = document.querySelector('#password');
const confirmation = document.querySelector('#confirmation');
const showPassword = document.querySelector('#show-password');

if (confirmation) {
  const message = document.querySelector('.message--login');
  const letter = message.querySelector('.message__letter');
  const capital = message.querySelector('.message__capital');
  const number = message.querySelector('.message__number');
  const special = message.querySelector('.message__special');
  const length = message.querySelector('.message__length');
  const confirmationMessage = document.querySelector('.message--confirmation');
  const confirmed = document.querySelector('.message__confirmed');

  password.addEventListener('focus', () => {
    message.style.display = 'block';
  });

  password.addEventListener('blur', () => {
    message.style.display = 'none';
  });

  password.addEventListener('keyup', () => {
    const lowerCaseLetters = /[a-z]/g;
    if(password.value.match(lowerCaseLetters)) {
      letter.classList.remove('message__invalid');
      letter.classList.add('message__valid');
    } else {
      letter.classList.remove('message__valid');
      letter.classList.add('message__invalid');
    }

    const upperCaseLetters = /[A-Z]/g;
    if(password.value.match(upperCaseLetters)) {
      capital.classList.remove('message__invalid');
      capital.classList.add('message__valid');
    } else {
      capital.classList.remove('message__valid');
      capital.classList.add('message__invalid');
    }

    const numbers = /[0-9]/g;
    if(password.value.match(numbers)) {
      number.classList.remove('message__invalid');
      number.classList.add('message__valid');
    } else {
      number.classList.remove('message__valid');
      number.classList.add('message__invalid');
    }

    const specials = /[$@#!]/g;
    if(password.value.match(specials)) {
      special.classList.remove('message__invalid');
      special.classList.add('message__valid');
    } else {
      special.classList.remove('message__valid');
      special.classList.add('message__invalid');
    }

    if(password.value.length >=6 && password.value.length <=20) {
      length.classList.remove('message__invalid');
      length.classList.add('message__valid');
    } else {
      length.classList.remove('message__valid');
      length.classList.add('message__invalid');
    }
  });

  confirmation.addEventListener('focus', () => {
    confirmationMessage.style.display = 'block';
  });

  confirmation.addEventListener('blur', () => {
    confirmationMessage.style.display = 'none';
  });

  confirmation.addEventListener('keyup', () => {
    if(password.value !== '' && password.value === confirmation.value) {
      confirmed.classList.remove('message__invalid');
      confirmed.classList.add('message__valid');
    } else {
      confirmed.classList.remove('message__valid');
      confirmed.classList.add('message__invalid');
    }
  });

  showPassword.addEventListener('click', () => {
    if (password.type === 'password' && confirmation.type === 'password') {
      password.type = 'text';
      confirmation.type = 'text';
    } else {
      password.type = 'password';
      confirmation.type = 'password';
    }
  });
} else {
  showPassword.addEventListener('click', () => {
    if (password.type === 'password') {
      password.type = 'text';
    } else {
      password.type = 'password';
    }
  });
}
