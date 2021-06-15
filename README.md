# E-Commerce web-site "Harenezumi"
#### Video Demo:  <https://www.youtube.com/watch?v=CIlSwBbL3Dg>
#### Description:
This is a web-site for daily grocery shopping that makes shopping experience fun and easy, especially when other closest stores are far from home or when you cannot leave your home for any reason.

Harenezumi means headgehog in japanese. So site logo depicts a cute headgehog.

The web-site is adaptive and accessible.

The web-site contains a layout page with head and footer for all other pages. Header is not included in layout as it varies by page.

The web-site also consists of 5 pages that extend layout. These are:
  - index page or the main page of the site
  - catalog page
  - cart page
  - login page
  - register page than can be accessed from login page

On all pages user will have access to main page by clicking logo in the header, to search of products by their name, to their cart, to login and to catalog, which has a dropdown menu with subcategories. If user is already logged in, instead of login he/she will see "Logout" text.

On the **main page** users will see a carousel slider with special offers animated with CSS and JS. By clicking on the text on slider user will be redirected to featured products within catalog.
Under the carousel slider there's a list of other special offers which can be a on discount or promotion. User can add these product directly to his/her cart.

On the **category page** user will see all products available or filter them by category using menu on the left (desktop verion) or dropdown menu in header (mobile and tablet versions). User can add these product directly to his/her cart.
Pages for each product are not created in this version, but will be added on further updates.

On the **cart page** user will see a list of all products that he/she added and total sum of purchase. Here user can change quantity of each product or remove any of them. Sum of purchase will be recalculated accordingly. 

Also total quantity of products added to cart is displayed in header near cart icon. It is visible on all pages of the web-site and changes if user add new products to cart of removes them.

When user is ready to check out, after clicking on 'Check out' button the site follows one of the routs: 
  - if user is logged as user, flash message appears informing that the purchase is successfull and cart get cleaned
  - if user is a guest, he/she get redirected to **login page** with prompt to log in in order to proceed with purchase. After loggin in, the contents of the cart is attributed from guest user session to registered user session, so user can continue from where he/she left cart page

If user has not yet been registered in system, he/she can register by clicking "Register" button on Login page. **Register page** has additional password confirmation. The web-site defines minimun length and symbols that password must contain and prompts the user accordingly. Password is securely hashed.

In **search field** user can search products by their name, and by clicking on search result he/she will be redirected to the product category on catalog page (since product pages are not available so far). Search is realized with jasonify.
