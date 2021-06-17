const carousel = document.querySelector('.carousel');

const carouselItem = carousel.querySelectorAll('.carousel__item');
const carouselSlides = carousel.querySelectorAll('.carousel__slide');
const nextItem = carousel.querySelector('.carousel__next');
const previousItem = carousel.querySelector('.carousel__previous');

let slideIndex = 0;
const slide1 = carousel.querySelector('.carousel__slide--1');
const slide2 = carousel.querySelector('.carousel__slide--2');
const slide3 = carousel.querySelector('.carousel__slide--3');
const image1 = carousel.querySelector('.carousel__item--1');
const image2 = carousel.querySelector('.carousel__item--2');
const image3 = carousel.querySelector('.carousel__item--3');

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

const slideToFirst = slide1.addEventListener ('click', function() {
  if (!slide1.classList.contains('carousel__slide--active')) {
    slide1.classList.add('carousel__slide--active');
    slide2.classList.remove('carousel__slide--active');
    slide3.classList.remove('carousel__slide--active');
  }
  image1.classList.add('carousel__item--current');
  image2.classList.remove('carousel__item--current');
  image3.classList.remove('carousel__item--current');
  slideIndex = 0;
});

const slideToSecond = slide2.addEventListener ('click', function() {
  if (!slide2.classList.contains('carousel__slide--active')) {
    slide2.classList.add('carousel__slide--active');
    slide1.classList.remove('carousel__slide--active');
    slide3.classList.remove('carousel__slide--active');
  }
  image2.classList.add('carousel__item--current');
  image1.classList.remove('carousel__item--current');
  image3.classList.remove('carousel__item--current');
  slideIndex = 1;
});

const slideToThird = slide3.addEventListener ('click', function() {
  if (!slide3.classList.contains('carousel__slide--active')) {
    slide3.classList.add('carousel__slide--active');
    slide2.classList.remove('carousel__slide--active');
    slide1.classList.remove('carousel__slide--active');
  }
  image3.classList.add('carousel__item--current');
  image2.classList.remove('carousel__item--current');
  image1.classList.remove('carousel__item--current');
  slideIndex = 2;
});

const slideToNext = nextItem.addEventListener ('click', function() {
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
});

const slideToPrevious = previousItem.addEventListener ('click', function() {
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
});

const rotateSlides = () => {
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
}

export {slideToFirst, slideToSecond, slideToThird, slideToNext, slideToPrevious, rotateSlides};
