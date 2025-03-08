from flask import Flask, render_template, request, redirect, url_for

app = Flask(_name_)

# Code correct pour accéder
SECRET_CODE = "1234"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_code = request.form.get("code")
        if user_code == SECRET_CODE:
            return redirect(url_for("calcul"))
        else:
            return render_template("index.html", error="Code incorrect, essayez encore.")
    return render_template("index.html", error=None)

@app.route("/calcul", methods=["GET", "POST"])
def calcul():
    if request.method == "POST":
        try:
            # Récupération des entrées utilisateur
            x_A = float(request.form["x_A"])
            D_AB_0 = float(request.form["D_AB_0"])
            D_BA_0 = float(request.form["D_BA_0"])
            q_A = float(request.form["q_A"])
            q_B = float(request.form["q_B"])
            r_A = float(request.form["r_A"])
            r_B = float(request.form["r_B"])
            a_AB = float(request.form["a_AB"])
            a_BA = float(request.form["a_BA"])
            T = float(request.form["T"])
            D_exp = float(request.form["D_exp"])

            # Calcul de lambda
            lambda_A = (r_A) ** (1/3)
            lambda_B = (r_B) ** (1/3)

            # Calcul de phi (fraction de surface)
            phi_A = (x_A * lambda_A) / (x_A * lambda_A + (1 - x_A) * lambda_B)
            phi_B = ((1 - x_A) * lambda_B) / (x_A * lambda_A + (1 - x_A) * lambda_B)

            # Calcul de theta (paramètre de volume)
            somme_xq = x_A * q_A + (1 - x_A) * q_B
            theta_A = (x_A * q_A) / somme_xq
            theta_B = ((1 - x_A) * q_B) / somme_xq

            # Calcul des valeurs de tau
            tau_AB = math.exp(-a_AB / T)
            tau_BA = math.exp(-a_BA / T)

            # Calcul de θ_AA et θ_BB
            theta_AA = (theta_A * 1) / (theta_A * 1 + theta_B * tau_BA)
            theta_BB = (theta_B * 1) / (theta_A * tau_AB + theta_B * 1)

            # Calcul de theta_ji
            theta_AB = (theta_A * tau_AB) / (theta_A * tau_AB + theta_B * 1)
            theta_BA = (theta_B * tau_BA) / (theta_A * 1 + theta_B * tau_BA)

            # Calcul du logarithme du coefficient de diffusion
            ln_D_AB = ((x_A * math.log(D_BA_0) + (1 - x_A) * math.log(D_AB_0)) +
                       2 * (x_A * math.log(x_A / phi_A) + (1 - x_A) * math.log((1 - x_A) / phi_B)) +
                       2 * x_A * (1 - x_A) * ((phi_A / x_A) * (1 - (lambda_A / lambda_B)) + (phi_B / (1 - x_A) * (1 - (lambda_B / lambda_A)))) +
                       x_A * q_B * ((1 - theta_AB*2) * math.log(tau_AB) + (1 - theta_AA*2) * tau_BA * math.log(tau_BA)) +
                       (1 - x_A) * q_A * ((1 - theta_BA*2) * math.log(tau_BA) + (1 - theta_BB*2) * tau_AB * math.log(tau_AB)))

            # Calcul du coefficient de diffusion
            D_AB = math.exp(ln_D_AB)

            # Calcul de l'erreur relative
            erreur = abs((D_AB - D_exp) / D_exp) * 100

            return render_template("calcul.html", result=D_AB, erreur=erreur)

        except ValueError:
            return render_template("calcul.html", error="Veuillez entrer des valeurs valides.")

    return render_template("calcul.html", result=None, erreur=None)
    
if _name_ == "_main_":
    app.run(debug=True)