from flask import Flask, render_template, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

import possible_cards

app = Flask(__name__)

app.config["SECRET_KEY"] = "testkey"


class OpponentForm(FlaskForm):

    unit_cost = StringField("Unit Cost:")
    fire = StringField("Fire:")
    time = StringField("Time:")
    justice = StringField("Justice:")
    primal = StringField("Primal:")
    shadow = StringField("Shadow:")
    search = SubmitField("Search")
    img_list = list()


@app.route("/", methods=["GET", "POST"])
def index():

    form = OpponentForm()
    unit_cost = "0"

    if form.validate_on_submit():
        unit_cost = form.unit_cost.data
        fire = form.fire.data
        time = form.time.data
        justice = form.justice.data
        primal = form.primal.data
        shadow = form.shadow.data

        form.unit_cost.data = ""
        form.fire.data = ""
        form.time.data = ""
        form.justice.data = ""
        form.primal.data = ""
        form.shadow.data = ""

        opponent_influence = {
            "F": fire,
            "T": time,
            "J": justice,
            "P": primal,
            "S": shadow,
        }

        for influence in opponent_influence:
            if opponent_influence[influence] is "":
                opponent_influence[influence] = 0
            else:
                opponent_influence[influence] = int(opponent_influence[influence])

        print(opponent_influence)
        all_stealth_cards = possible_cards.get_all_stealth_cards()
        cards_possible = possible_cards.list_possible_cards(
            all_stealth_cards, int(unit_cost), opponent_influence
        )
        print(cards_possible)
        form.img_list.clear()
        for card in cards_possible:
            print(card)
            form.img_list.append(card.img_url)

    return render_template(
        "index.html", form=form, unit_cost=unit_cost, img_list=form.img_list
    )


if __name__ == "__main__":
    app.run()
