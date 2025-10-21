from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            result = eval(expression)
        except:
            result = "Error"

        # --- SAVE TO HISTORY ---
        if "history" not in session:
            session["history"] = []
        session["history"].append(f"Calci: {expression} = {result}")

    return render_template("index.html", result=result)


from datetime import datetime

@app.route("/age", methods=["GET", "POST"])
def age():
    result = None
    if request.method == "POST":
        dob = request.form.get("dob")
        current = request.form.get("current")

        dob_date = datetime.strptime(dob, "%Y-%m-%d")
        current_date = datetime.strptime(current, "%Y-%m-%d") if current else datetime.now()

        # --- Calculate years, months, days ---
        years = current_date.year - dob_date.year
        months = current_date.month - dob_date.month
        days = current_date.day - dob_date.day

        # Adjust if month/day are negative
        if days < 0:
            from calendar import monthrange
            prev_month_days = monthrange(current_date.year, current_date.month - 1 if current_date.month > 1 else 12)[1]
            days += prev_month_days
            months -= 1

        if months < 0:
            months += 12
            years -= 1

        result = f"{years} years, {months} months, and {days} days"

        # --- SAVE TO HISTORY ---
        if "history" not in session:
            session["history"] = []
        session["history"].append(f"Age: DOB={dob}, Result={result}")

    return render_template("age.html", result=result)



@app.route("/emi", methods=["GET", "POST"])
def emi():
    result = None
    if request.method == "POST":
        principal = float(request.form.get("principal"))
        rate = float(request.form.get("rate"))
        time = float(request.form.get("time"))

        monthly_rate = rate / (12 * 100)
        months = time * 12
        emi = principal * monthly_rate * ((1 + monthly_rate)**months) / (((1 + monthly_rate)**months) - 1)
        result = f"₹ {emi:,.2f}"

        # --- SAVE TO HISTORY ---
        if "history" not in session:
            session["history"] = []
        session["history"].append(f"EMI: P={principal}, R={rate}, T={time}, EMI={result}")

    return render_template("emi.html", result=result)


@app.route("/code", methods=["GET", "POST"])
def code_calculator():
    result = ""
    expression = ""
    if request.method == "POST":
        try:
            expression = request.form["expression"]
            result = eval(expression)
        except:
            result = "Error"

        # --- SAVE TO HISTORY ---
        if "history" not in session:
            session["history"] = []
        session["history"].append(f"Expression: {expression} = {result}")

    return render_template("code.html", result=result, expression=expression)


@app.route("/history")
def history():
    hist = session.get("history", [])
    return render_template("history.html", history=hist)


@app.route("/clear-history", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(debug=True)
