from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_required
from flask import session as login_session
from flask import session
from sqlalchemy import desc
from .models import User, Bid, Tool

from .forms import LoginForm, RegisterForm, CreateForm, SearchForm, Results, LandingForm
import sqlalchemy as db
from . import db

import re
#from flask_table import Table, Col

print("this is __name__")
print(type(__name__))
print(__name__)

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    tools = Tool.query.order_by(desc(Tool.date_created)).limit(4).all()
    print(tools)
    form_land = LandingForm()
    print("Form has not validated")
    search_results = []
    search = SearchForm()
    if request.args.get("landing_search") != None:
        print("Form has validated")
        search_string = request.args.get("landing_search")
        print(search_string)

        all_tools = Tool.query.all()
        for tool in all_tools:
            if re.search(search_string, tool.tool_name):
                search_results.append(tool)

        print("Below is Search results")

        # display results
        table = Results(search_results)
        table.border = True
        # del input_string
        return render_template("results.html", form=search, table=table)
    return render_template("index.html", tools=tools, form=form_land)


@bp.route("/results", methods=["GET", "POST"])
def search():

    search = SearchForm()
    search_results = []

    if search.validate_on_submit():

        search_string = search.data["search"]
        print(search_string)
        if search_string != "":
            all_tools = Tool.query.all()
            for tool in all_tools:
                if re.search(search_string, tool.tool_name):
                    search_results.append(tool)
        else:
            print("This string is empty")
        print("Below is Search results")

        # display results
        table = Results(search_results)
        table.border = True
        return render_template("results.html", form=search, table=table)

    return render_template("results.html", form=search)
