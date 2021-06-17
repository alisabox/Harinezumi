const search = document.querySelector('.navbar__search-input')

const getSearch = search.addEventListener('keyup', function() {
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

export {getSearch};
