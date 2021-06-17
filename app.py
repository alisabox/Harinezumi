import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, flash, redirect, render_template, request, session, jsonify

# Open on python3 -m flask run

# Configure application
app = Flask(__name__)
app.secret_key = "super secret key"

DATABASE = 'database.db'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
  response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
  response.headers["Expires"] = 0
  response.headers["Pragma"] = "no-cache"
  return response

@app.route("/", methods=["GET", "POST"])
def index():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()

  if request.method == "POST":
    purchase = request.form.get("purchase")
    getProduct = db.execute("SELECT * FROM catalog WHERE id = ?", (purchase,))
    product = []
    for i in getProduct:
      product.append(i)
    product = product[0]
    if session.get("user_id") is None:
      db.execute("INSERT INTO users (username, password, user_type) VALUES ('unset', 'unset', 'guest')")
      con.commit()
      id = db.execute("SELECT last_insert_rowid() FROM users WHERE user_type = 'guest'")
      guestId = []
      for i in id:
        guestId.append(i)
      session["user_id"] = guestId[0][0]
    similarProductsData = db.execute("SELECT * FROM cart WHERE product = ? AND user_id = ?", (product[2], session.get("user_id"),))
    similarProducts = []
    for row in similarProductsData:
      similarProducts.append(row)
    if similarProducts == []:
      db.execute("INSERT INTO cart (user_id, category, product, price, quantity) VALUES (?, ?, ?, ?, 1)", (session.get("user_id"), product[1], product[2], product[3],))
      con.commit()
    else:
      db.execute("UPDATE cart SET quantity = quantity + 1, price = ? WHERE product = ? AND user_id = ?", (product[3], product[2], session.get("user_id"),))
      con.commit()
    cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
    cart = []
    for row in cartData:
      cart.append(row)
    cart = cart[0][0]
    featured = db.execute("SELECT * FROM catalog WHERE featured = 1")
    return render_template("index.html", featured=featured, cart=cart)
  else:
    cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
    cart = []
    for row in cartData:
      cart.append(row)
    cart = cart[0][0]
    if session.get("user_id"):
      statusData = db.execute("SELECT user_type FROM users WHERE id = ?", (session.get("user_id"),))
      status = []
      for i in statusData:
        status.append(i)
      if status[0][0] == 'guest':
        featured = db.execute("SELECT * FROM catalog WHERE featured = 1")
        return render_template("index.html", featured=featured, cart=cart)

    featured = db.execute("SELECT * FROM catalog WHERE featured = 1")
    return render_template("index.html", featured=featured, status=True, cart=cart)


@app.route("/login", methods=["GET", "POST"])
def login():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  # User reached route via POST (as by submitting a form via POST)
  if request.method == "POST":
    # Ensure username was submitted
    if not request.form.get("email"):
      message = "Invalid email or/and password"
      return render_template("login.html", message=message, cart=cart)

    # Ensure password was submitted
    elif not request.form.get("password"):
      message = "Invalid email or/and password"
      return render_template("login.html", message=message, cart=cart)

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("email"),))
    user = []
    for row in rows:
      user.append(row)

    # Ensure username exists and password is correct
    if len(user) != 1 or not check_password_hash(user[0][2], request.form.get("password")):
      message = "Invalid email or/and password"
      return render_template("login.html", message=message, cart=cart)

    # Check for active guest sessions
    if session.get("user_id"):
      db.execute("UPDATE cart SET user_id = REPLACE(user_id, ?, ?)", (session.get("user_id"), user[0][0],))
      con.commit()
      db.execute("DELETE FROM users WHERE id = ? AND user_type = 'guest'", (session.get("user_id"),))
      con.commit()

    # Remember which user has logged in
    session["user_id"] = user[0][0]

    # Redirect user to home page
    return redirect("/")

  # User reached route via GET (as by clicking a link or via redirect)
  else:
    if session.get("user_id"):
      statusData = db.execute("SELECT user_type FROM users WHERE id = ?", (session.get("user_id"),))
      status = []
      for i in statusData:
        status.append(i)
      if status[0][0] == 'guest':
        return render_template("login.html", cart=cart)
    return render_template("login.html", status=True, cart=cart)

@app.route("/register", methods=["GET", "POST"])
def register():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  # User reached route via POST (as by submitting a form via POST)
  if request.method == "POST":
    # Ensure username was submitted
    username = request.form.get("email")
    if not username:
      flash("Invalid email or/and password")
      return render_template("register.html", cart=cart)

    # Ensure password was submitted
    password = request.form.get("password")
    if not password:
      flash("Invalid email or/and password")
      return render_template("register.html", cart=cart)

    # Conditions for a valid password:
      # Should have at least one number.
      # Should have at least one uppercase and one lowercase character.
      # Should have at least one special symbol.
      # Should be between 6 to 20 characters long.
    SpecialSym = ['$', '@', '#', '%', '!']
    if len(password) < 6:
      flash("Password length should be at least 6 characters")
      return render_template("register.html", cart=cart)
    if len(password) > 20:
      flash("Password length should be at not longer than 20 characters")
      return render_template("register.html", cart=cart)
    if not any(char.isdigit() for char in password):
      flash("Password should have at least one numeral")
      return render_template("register.html", cart=cart)
    if not any(char.isupper() for char in password):
      flash("Password should have at least one uppercase letter")
      return render_template("register.html", cart=cart)
    if not any(char.islower() for char in password):
      flash("Password should have at least one lowercase letter")
      return render_template("register.html", cart=cart)
    if not any(char in SpecialSym for char in password):
      flash("Password should have at least one of the symbols $@#!")
      return render_template("register.html", cart=cart)

    # Check the confirmation
    confirmation = request.form.get("confirmation")
    if confirmation != password:
      flash("Not matching passwords")
      return render_template("register.html", cart=cart)

    hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    # Register into database
    db.execute("INSERT INTO users (username, password, user_type) VALUES(?, ?, 'user')", (username, hashed))
    con.commit()
    rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = []
    for row in rows:
      user.append(row)

    # Check for active guest sessions
    if session.get("user_id"):
      db.execute("UPDATE cart SET user_id = REPLACE(user_id, ?, ?)", (session.get("user_id"), user[0][0],))
      con.commit()
      db.execute("DELETE FROM users WHERE id = ? AND user_type = 'guest'", (session.get("user_id"),))
      con.commit()

    # Remember which user has logged in
    session["user_id"] = user[0][0]
    
    flash("You are registered!")
    return render_template("register.html", cart=cart)

  # User reached route via GET (as by clicking a link or via redirect)
  else:
    return render_template("register.html", cart=cart)

@app.route("/logout")
def logout():
  # Log user out

  # Forget any user_id
  session.clear()

  # Redirect user to login form
  return redirect("/")


@app.route("/cart", methods=["GET", "POST"])
def cart():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  if request.method == "POST":

    removeProduct = request.form.get("remove")
    db.execute("DELETE FROM cart WHERE purchase_id = ? AND user_id = ?", (removeProduct, session.get("user_id"),))
    con.commit()

    reduce = request.form.get("reduce")
    db.execute("UPDATE cart SET quantity = (quantity - 1) WHERE quantity > 1 AND purchase_id = ? AND user_id = ?", (reduce, session.get("user_id"),))
    con.commit()

    increase = request.form.get("increase")
    db.execute("UPDATE cart SET quantity = (quantity + 1) WHERE quantity < 20 AND purchase_id = ? AND user_id = ?", (increase, session.get("user_id"),))
    con.commit()

    # Get data from cart
    cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
    cart = []
    for row in cartData:
      cart.append(row)
    cart = cart[0][0]

    checkout = request.form.get("checkout")
    if checkout:
      statusData = db.execute("SELECT user_type FROM users WHERE id = ?", (session.get("user_id"),))
      status = []
      for i in statusData:
        status.append(i)
      if status[0][0] == 'guest':
        flash("Please, log in to continue to checkout")
        return redirect("/login")
      else:
        db.execute("DELETE FROM cart WHERE user_id = ?", (session.get("user_id"),))
        con.commit()
        cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
        cart = []
        for row in cartData:
          cart.append(row)
        cart = cart[0][0]
        return render_template("cart.html", message='Your purchase is successful!', status=True, cart=cart)

  purchasesData = db.execute("SELECT * FROM cart WHERE user_id = ?", (session.get("user_id"),))
  purchases = []
  totalAmount = 0
  for row in purchasesData:
    purchases.append(row)
    totalAmount = totalAmount + (row[4] * row[5])
  if session.get("user_id"):
    statusData = db.execute("SELECT user_type FROM users WHERE id = ?", (session.get("user_id"),))
    status = []
    for i in statusData:
      status.append(i)
    if status[0][0] == 'guest':
      return render_template("cart.html", purchases=purchases, totalAmount=totalAmount, cart=cart)
  return render_template("cart.html", purchases=purchases, totalAmount=totalAmount, status=True, cart=cart)


@app.route("/catalog", methods=["GET", "POST"])
def catalog():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  if request.method == "POST":
    purchase = request.form.get("purchase")
    getProduct = db.execute("SELECT * FROM catalog WHERE id = ?", (purchase,))
    product = []
    for i in getProduct:
      product.append(i)
    product = product[0]
    if session.get("user_id") is None:
      db.execute("INSERT INTO users (username, password, user_type) VALUES ('unset', 'unset', 'guest')")
      con.commit()
      id = db.execute("SELECT last_insert_rowid() FROM users WHERE user_type = 'guest'")
      guestId = []
      for i in id:
        guestId.append(i)
      session["user_id"] = guestId[0][0]
    similarProductsData = db.execute("SELECT * FROM cart WHERE product = ? AND user_id = ?", (product[2], session.get("user_id"),))
    similarProducts = []
    for row in similarProductsData:
      similarProducts.append(row)
    if similarProducts == []:
      db.execute("INSERT INTO cart (user_id, category, product, price, quantity) VALUES (?, ?, ?, ?, 1)", (session.get("user_id"), product[1], product[2], product[3],))
      con.commit()
    else:
      db.execute("UPDATE cart SET quantity = quantity + 1, price = ? WHERE product = ? AND user_id = ?", (product[3], product[2], session.get("user_id"),))
      con.commit()
    return redirect(request.referrer)
  else:
    if session.get("user_id"):
      statusData = db.execute("SELECT user_type FROM users WHERE id = ?", (session.get("user_id"),))
      status = []
      for i in statusData:
        status.append(i)
      if status[0][0] == 'guest':
        products = db.execute("SELECT * FROM catalog")
        return render_template("catalog.html", products=products, total=True, cart=cart)
    products = db.execute("SELECT * FROM catalog")
    return render_template("catalog.html", products=products, status=True, total=True, cart=cart)


@app.route("/fruit", methods=["GET", "POST"])
def fruit():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Fruits, Vegetables and Berries'")
  category = 'Fruits, Vegetables and Berries'
  return render_template("catalog.html", products=products, category=category, cart=cart)

@app.route("/dairy", methods=["GET", "POST"])
def dairy():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Dairy'")
  category = 'Dairy'
  return render_template("catalog.html", products=products, category=category, cart=cart)


@app.route("/meat", methods=["GET", "POST"])
def meat():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Meat and fish'")
  category = 'Meat and fish'
  return render_template("catalog.html", products=products, category=category, cart=cart)

@app.route("/cereals", methods=["GET", "POST"])
def cereals():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Cereals'")
  category = 'Cereals'
  return render_template("catalog.html", products=products, category=category, cart=cart)

@app.route("/drinks", methods=["GET", "POST"])
def drinks():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Drinks'")
  category = 'Drinks'
  return render_template("catalog.html", products=products, category=category, cart=cart)

@app.route("/bread", methods=["GET", "POST"])
def bread():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Bread and bakery'")
  category = 'Bread and bakery'
  return render_template("catalog.html", products=products, category=category, cart=cart)

@app.route("/ready", methods=["GET", "POST"])
def ready():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Ready-made food'")
  category = 'Ready-made food'
  return render_template("catalog.html", products=products, category=category, cart=cart)

@app.route("/snaks", methods=["GET", "POST"])
def snaks():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Snacks'")
  category = 'Snacks'
  return render_template("catalog.html", products=products, category=category, cart=cart)

@app.route("/pet", methods=["GET", "POST"])
def pet():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  # Get data from cart
  cartData = db.execute("SELECT SUM(quantity) FROM cart WHERE user_id = ?", (session.get("user_id"),))
  cart = []
  for row in cartData:
    cart.append(row)
  cart = cart[0][0]

  products = db.execute("SELECT * FROM catalog WHERE category = 'Pet food'")
  category = 'Pet food'
  return render_template("catalog.html", products=products, category=category, cart=cart)

@app.route("/search")
def search():
  con = sqlite3.connect(DATABASE)
  db = con.cursor()
  search = request.args.get("q")

  if search:
    searchData = db.execute("SELECT product, link FROM catalog WHERE product LIKE ?", ("%" + search + "%",))
    searchOutput = []
    for item in searchData:
      searchOutput.append(item)
    return jsonify(searchOutput)
