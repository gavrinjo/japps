from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistarationForm, LoginForm
app = Flask(__name__)

app.config["SECRET_KEY"] = "3eccb7be0b8fab6d1a7d4a70414cebd0"

posts = [
    {
        "company": "STUDIO ARTIS d.o.o.",
        "position": "Projektant suradnik(m / ž)",
        "location": "Seget Donji",
        "deadline": "19.09.2018.",
        "href": "https://www.moj-posao.net/Posao/395550/Projektant-suradnik-mz/"
    },
    {
        "company": "Quid Est",
        "position": "Promotor / Prodajni predstavnik (m/ž)",
        "location": "Zagreb",
        "deadline": "27.09.2018.",
        "href": "https://www.moj-posao.net/Posao/393666/Promotor-Prodajni-predstavnik-mz/"
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistarationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "admin":
            flash("You have been loged in", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check your email and password", "danger")
    return render_template("login.html", title="Login", form=form)

if __name__ == "__main__":
    app.run(debug=True)
