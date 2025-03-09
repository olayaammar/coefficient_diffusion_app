from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Clé secrète pour sécuriser la session

# Code d'accès défini (change-le si nécessaire)
ACCESS_CODE = "1234"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        code = request.form.get("code")
        if code == ACCESS_CODE:
            session["logged_in"] = True  # Marquer l'utilisateur comme connecté
            return redirect(url_for("diffusion"))
        else:
            return render_template("login.html", error="Code incorrect ! Réessayez.")
    return render_template("login.html")

@app.route("/diffusion", methods=["GET", "POST"])
def diffusion():
    if not session.get("logged_in"):  # Vérifie si l'utilisateur est connecté
        return redirect(url_for("login"))
    if request.method == "POST":
        try:
            x_A = float(request.form.get("x_A"))
            D_AB_0 = float(request.form.get("D_AB_0"))
            D_BA_0 = float(request.form.get("D_BA_0"))
            q_A = float(request.form.get("q_A"))
            q_B = float(request.form.get("q_B"))
            r_A = float(request.form.get("r_A"))
            r_B = float(request.form.get("r_B"))
            a_AB = float(request.form.get("a_AB"))
            a_BA = float(request.form.get("a_BA"))
            T = float(request.form.get("T"))
            D_exp = float(request.form.get("D_exp"))

            import math
            lambda_A = (r_A) ** (1 / 3)
            lambda_B = (r_B) ** (1 / 3)
            phi_A = (x_A * lambda_A) / (x_A * lambda_A + (1 - x_A) * lambda_B)
            phi_B = ((1 - x_A) * lambda_B) / (x_A * lambda_A + (1 - x_A) * lambda_B)
            somme_xq = x_A * q_A + (1 - x_A) * q_B
            theta_A = (x_A * q_A) / somme_xq
            theta_B = ((1 - x_A) * q_B) / somme_xq
            tau_AA = 1
            tau_BB = 1
            tau_AB = math.exp(-a_AB / T)
            tau_BA = math.exp(-a_BA / T)
            theta_AA = (theta_A * tau_AA) / (theta_A * tau_AA + theta_B * tau_BA)
            theta_BB = (theta_B * tau_BB) / (theta_A * tau_AB + theta_B * tau_BB)
            theta_AB = (theta_A * tau_AB) / (theta_A * tau_AB + theta_B * tau_BB)
            theta_BA = (theta_B * tau_BA) / (theta_A * tau_AA + theta_B * tau_BA)
            ln_D_AB = ((x_A * math.log(D_BA_0) + (1 - x_A) * math.log(D_AB_0)) +
                       2 * (x_A * math.log(x_A / phi_A) + (1 - x_A) * math.log((1 - x_A) / phi_B)) +
                       2 * x_A * (1 - x_A) * ((phi_A / x_A) * (1 - (lambda_A / lambda_B)) +
                                              (phi_B / (1 - x_A)) * (1 - (lambda_B / lambda_A))) +
                       x_A * q_B * ((1 - theta_AB*2) * math.log(tau_AB) + (1 - theta_AA*2) * tau_BA * math.log(tau_BA)) +
                       (1 - x_A) * q_A * ((1 - theta_BA*2) * math.log(tau_BA) + (1 - theta_BB*2) * tau_AB * math.log(tau_AB)))
            D_AB = math.exp(ln_D_AB)
            erreur = abs((D_AB - D_exp) / D_exp) * 100
            return render_template("diffusion.html", D_AB=D_AB, erreur=erreur)
        except ValueError:
            return render_template("diffusion.html", error="Erreur : Veuillez entrer des valeurs numériques valides.")
    return render_template("diffusion.html", D_AB=None, erreur=None)

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/historique")
def historique():
    return render_template("historique.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
