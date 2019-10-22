import datetime
from flask import (Blueprint, flash, render_template, session,
                   request, url_for, redirect)
from .models import Tool, Bid, User
from sqlalchemy import desc
from .forms import BidForm, MarkSold, UndoSold, CreateForm
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from decimal import Decimal, getcontext
import os
from . import db

bp = Blueprint('userdash', __name__, url_prefix='/userdash')


@bp.route('/main/<userid>', methods=["POST", "GET"])
@login_required
def maindash(userid):
    # count tools selling
    tool = Tool.query.filter_by(user_id=userid).filter(
        Tool.sold_status == 0).all()
    tool_length = len(tool)
    # tool_length = session.get('tool_length', None)

    # count bids made by user
    bids = db.session.query(Tool, Bid).join(
        Bid).filter_by(user_id=userid).all()
    bid_length = len(bids)

    # tools sold by user
    sold = Tool.query.filter_by(user_id=userid).filter(
        Tool.sold_status != 0).all()
    sold_length = len(sold)

    # recently viewed itemts list
    recently_viewed = session.get('vieweditems')

    views = Tool.query.filter(Tool.id.in_(recently_viewed)).all()
    return render_template('userdash/maindash.html', userid=userid, tool_length=tool_length, bid_length=bid_length, sold_length=sold_length, views=views)


@bp.route('/userselling/<userid>', methods=["POST", "GET"])
@login_required
def userselling(userid):

    print(userid)
    # query db for tools current user has listed
    tool = Tool.query.filter_by(user_id=userid).filter(
        Tool.sold_status == 0).all()
    tool_length = len(tool)

    print(tool)
    print("-----------Tool length below---------------------")
    print(tool_length)
    return render_template('userdash/manageselling.html', userid=userid, tool=tool)


@bp.route('/userbids/<userid>', methods=["POST", "GET"])
@login_required
def userbids(userid):
    # query db for bids current user has made
    bids = db.session.query(Tool, Bid).join(
        Bid).filter_by(user_id=userid).all()
    print(bids)
    current_user = session.get('user_id')

    # if the url userid does not match the logged in user - log them out
    # if current_user != userid:
    #     return redirect(url_for('auth.logout'))
    return render_template('userdash/managebids.html', userid=userid, bids=bids)
