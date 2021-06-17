const toggler = document.querySelector('.navbar__toggler');
const navbar = document.querySelector('.navbar__collapse');

toggler.classList.remove('navbar__toggler--hide');
navbar.classList.toggle('navbar__collapse--closed');

const getToggle = toggler.addEventListener ('click', function() {
  toggler.classList.toggle('navbar__toggler--open');
  navbar.classList.toggle('navbar__collapse--closed');
});

const dropDown = document.querySelector('.navbar__dropdown-button');

const getDropDown = dropDown.addEventListener ('click', function() {
  dropDown.classList.toggle('navbar__dropdown-button--open');
});

export {getToggle, getDropDown};
