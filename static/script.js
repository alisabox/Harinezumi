// Toggle

let toggler = document.querySelector('.navbar__toggler');
let navbar = document.querySelector('.navbar__collapse')

toggler.classList.remove('navbar__toggler--hide');
navbar.classList.toggle('navbar__collapse--closed')

toggler.addEventListener ('click', function() {
    toggler.classList.toggle('navbar__toggler--open');
    navbar.classList.toggle('navbar__collapse--closed');
});

// Drop-down menu

let dropDown = document.querySelector('.navbar__dropdown-button');

dropDown.addEventListener ('click', function() {
  dropDown.classList.toggle('navbar__dropdown-button--open');
});

// Carousel

let carousel = document.querySelector('.carousel');

if (carousel) {
  let carouselItem = carousel.querySelectorAll('.carousel__item');
  let carouselSlides = carousel.querySelectorAll('.carousel__slide')
  let nextItem = carousel.querySelector('.carousel__next');
  let previousItem = carousel.querySelector('.carousel__previous');
  let slideIndex = 0;
  let slide1 = carousel.querySelector('.carousel__slide--1');
  let slide2 = carousel.querySelector('.carousel__slide--2');
  let slide3 = carousel.querySelector('.carousel__slide--3');
  let image1 = carousel.querySelector('.carousel__item--1');
  let image2 = carousel.querySelector('.carousel__item--2');
  let image3 = carousel.querySelector('.carousel__item--3');

  if (image1.classList.contains('carousel__item--current')) {
    slide1.classList.add('carousel__slide--active');
    slideIndex = 0;
  }

  if (image2.classList.contains('carousel__item--current')) {
    slide2.classList.add('carousel__slide--active');
    slideIndex = 1;
  }

  if (image3.classList.contains('carousel__item--current')) {
    slide3.classList.add('carousel__slide--active');
    slideIndex = 2;
  }

  slide1.addEventListener('click', function() {
    if (!slide1.classList.contains('carousel__slide--active')) {
      slide1.classList.add('carousel__slide--active');
      slide2.classList.remove('carousel__slide--active');
      slide3.classList.remove('carousel__slide--active');
    }
    image1.classList.add('carousel__item--current');
    image2.classList.remove('carousel__item--current');
    image3.classList.remove('carousel__item--current');
    slideIndex = 0;
  })

  slide2.addEventListener('click', function() {
    if (!slide2.classList.contains('carousel__slide--active')) {
      slide2.classList.add('carousel__slide--active');
      slide1.classList.remove('carousel__slide--active');
      slide3.classList.remove('carousel__slide--active');
    }
    image2.classList.add('carousel__item--current');
    image1.classList.remove('carousel__item--current');
    image3.classList.remove('carousel__item--current');
    slideIndex = 1;
  })

  slide3.addEventListener('click', function() {
    if (!slide3.classList.contains('carousel__slide--active')) {
      slide3.classList.add('carousel__slide--active');
      slide2.classList.remove('carousel__slide--active');
      slide1.classList.remove('carousel__slide--active');
    }
    image3.classList.add('carousel__item--current');
    image2.classList.remove('carousel__item--current');
    image1.classList.remove('carousel__item--current');
    slideIndex = 2;
  })

  nextItem.addEventListener('click', function() {
    if (carouselItem[carouselItem.length-1].classList.contains('carousel__item--current')) {
      carouselItem[carouselItem.length-1].classList.remove('carousel__item--current');
      carouselItem[0].classList.add('carousel__item--current');
      carouselSlides[carouselSlides.length-1].classList.remove('carousel__slide--active');
      carouselSlides[0].classList.add('carousel__slide--active');
      slideIndex = 0;
    }
    else {
      carouselItem[slideIndex].classList.remove('carousel__item--current');
      carouselItem[slideIndex+1].classList.add('carousel__item--current');
      carouselSlides[slideIndex].classList.remove('carousel__slide--active');
      carouselSlides[slideIndex+1].classList.add('carousel__slide--active');
      slideIndex++;
    }
  })
  previousItem.addEventListener('click', function() {
    if (carouselItem[0].classList.contains('carousel__item--current')) {
      carouselItem[0].classList.remove('carousel__item--current');
      carouselItem[carouselItem.length-1].classList.add('carousel__item--current');
      carouselSlides[0].classList.remove('carousel__slide--active');
      carouselSlides[carouselSlides.length-1].classList.add('carousel__slide--active');
      slideIndex = carouselItem.length-1;
    }
    else {
      carouselItem[slideIndex].classList.remove('carousel__item--current');
      carouselItem[slideIndex-1].classList.add('carousel__item--current');
      carouselSlides[slideIndex].classList.remove('carousel__slide--active');
      carouselSlides[slideIndex-1].classList.add('carousel__slide--active');
      slideIndex--;
    }
  })

  const interval = setInterval(function() {
    if (carouselItem[carouselItem.length-1].classList.contains('carousel__item--current')) {
      carouselItem[carouselItem.length-1].classList.remove('carousel__item--current');
      carouselItem[0].classList.add('carousel__item--current');
      carouselSlides[carouselSlides.length-1].classList.remove('carousel__slide--active');
      carouselSlides[0].classList.add('carousel__slide--active');
      slideIndex = 0;
    }
    else {
      carouselItem[slideIndex].classList.remove('carousel__item--current');
      carouselItem[slideIndex+1].classList.add('carousel__item--current');
      carouselSlides[slideIndex].classList.remove('carousel__slide--active');
      carouselSlides[slideIndex+1].classList.add('carousel__slide--active');
      slideIndex++;
    }
  }, 5000);
};


// Search

let search = document.querySelector('.navbar__search-input')

search.addEventListener('keyup', function() {
  if (search.value) {
    $.get('/search?q=' + search.value.toLowerCase(), function(searchOutput)
    {
      let list = '';
      for (let i in searchOutput) {
        console.log(searchOutput)
        let link = searchOutput[i][1];
        list += '<li><a href="' + link + '">' + searchOutput[i][0] + '</a></li>';

      }
      let seachedData = document.querySelector('.navbar__search-output')
      seachedData.classList.remove('visually-hidden');
      seachedData.innerHTML = list;
    })
  } else {
    let seachedData = document.querySelector('.navbar__search-output')
    seachedData.innerHTML = '';
    seachedData.classList.add('visually-hidden');
  }
});
