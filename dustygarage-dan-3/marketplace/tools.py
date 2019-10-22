import datetime
from datetime import datetime
from flask import (Blueprint, flash, render_template, session,
                   request, url_for, redirect)
from .models import Tool, Bid, User
from .forms import BidForm, MarkSold, UndoSold, CreateForm
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from decimal import Decimal, getcontext
import os
from . import db

bp = Blueprint('tool', __name__, url_prefix='/tools')

# create a page that will show the details of the tools
@bp.route('/<id>', methods=["POST", "GET"])
def show(id):

    bform = BidForm()

    user_obj = session.get('user_id')

    tool = Tool.query.filter_by(id=id).first()
    print(tool)

    # check that the product exists in the DB
    if tool == None:
        return redirect('../not_found')

    vieweditems = session.get('vieweditems')
    if id not in vieweditems:
        vieweditems.append(id)
    session['vieweditems'] = vieweditems
    print(vieweditems)

    list_price = tool.list_price

    # format list price for whole numbers and decimals
    # if list_price.is_integer():
    #     list_price = '${:.0f}'.format(list_price)
    # else:
    #     list_price = '${:,.2f}'.format(tool.list_price)

    bid_user = Bid.query.filter_by(user_id=user_obj, tool_id=id).first()
    current_bid_amount = ""

    # if the current logged in user has made a bid on this item, pass the amount
    if bid_user is not None:
        current_bid_amount = bid_user.bid_amount

    return render_template('tools/item.html', tool=tool, list_price=list_price, form=bform, bid_user=bid_user, current_bid_amount=current_bid_amount)

# <-------------------------------------Manage Item


@bp.route('/<id>/manage', methods=["POST", "GET"])
@login_required
def manage(id):
    soldForm = MarkSold(request.form)
    undoForm = UndoSold(request.form)

    # get the user id from the current session
    userid = session.get('user_id')
    intuserid = int(userid)
    # get the current tool details passed through the url
    tool = Tool.query.filter_by(id=id).first()
    print("tool details:")
    print(tool)
    tool_user = int(tool.user_id)
    print("Tool Listed By:")
    print(tool_user)
    print("Current Logged in user:")
    print(userid)

    if intuserid != tool_user:
        print("users do not match")
        return redirect('../not_found')

    # pass the sold status of the item
    sold_user = tool.sold_status
    print("tool soldstatus:")
    print(sold_user)

    bid_user = None
    set_to_zero = 0
    # If a user has not been marked as sold, show a list of current bids
    if sold_user == 0:
        print("THIS ITEM HAS ***NOT*** BEEN SOLD")

        bid_user = db.session.query(User, Bid).join(
            Bid).filter_by(tool_id=id).all()
        print('Current Bids')
        print(bid_user)

    # If a user has been marked as sold, show the details of that user and bid
    if sold_user != 0:
        print("THIS ITEM HAS BEEN SOLD")

        # join the user and bid table
        bid_user = db.session.query(User, Bid).filter(
            Bid.user_id == User.id).filter(Bid.tool_id == Tool.id).filter(Tool.sold_status == Bid.user_id).all()

    # User submits a mark as sold OR undo
    if request.method == "POST":
        if soldForm.submit.data:
            form_input = soldForm.bid_user_id.data
            print("Form Input:")
            print(form_input)
            update_tool = Tool.query.get(id)
            update_tool.sold_status = form_input
            update_tool.sold_date = datetime.now()
            db.session.commit()
            print('COMMITED TO DB')

        if undoForm.submit_undo.data:
            form_input = undoForm.undoSold.data
            print("Form Input:")
            print(form_input)
            update_tool = Tool.query.get(id)
            update_tool.sold_status = form_input
            update_tool.sold_date = 0
            db.session.commit()
            print('COMMITED TO DB')

        # redirect back to the manage page with refreshed list
        return redirect(url_for('tool.manage', id=id))

    return render_template('tools/manage.html', soldForm=soldForm, userid=userid, tool=tool, undoForm=undoForm, bid_user=bid_user, set_to_zero=set_to_zero)

    # db_file_path = check_file(form)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = CreateForm()
    heading = "List an Item"
    if form.validate_on_submit():
        print("Form validated")
        new_tool = Tool(
            tool_name=form.tool_name.data,
            modelNo=form.modelNo.data,
            list_price=form.list_price.data,
            category=form.category.data,
            user_id=session.get("user_id"),
            desc=form.desc.data,
            brand=form.brand.data,
        )
        db.session.add(new_tool)

        db.session.commit()
        return redirect(url_for("tool.create"))

    return render_template("tools/create.html", form=form, heading=heading)


@bp.route('/<toolid>/bid', methods=['GET', 'POST'])
def bid(toolid):
    form = BidForm()
    tool = Tool.query.filter_by(id=toolid).first()
    print(tool)
    tool_id = tool.id
    tool_list_price = float(tool.list_price)
    print(tool_list_price)
    user_obj = session.get('user_id')
    # check if a bid exists for this user
    bid_user = Bid.query.filter_by(user_id=user_obj, tool_id=toolid).first()

    if bid_user is None:
        # get the tool object associated with the page
        if form.validate_on_submit():
            bid = Bid(bid_amount=form.bidamount.data,
                      tool_id=toolid, user_id=user_obj)
            bid_float = float(bid.bid_amount)
            if bid_float < tool_list_price:
                flash('Bid amount needs to be higher than the list price',
                      'alert alert-danger')
                print('Bid amount needs to be higher than the list price',
                      'alert alert-danger')
                return redirect(url_for('tool.show', id=tool_id))

            # add and commit to bid db
            db.session.add(bid)
            db.session.commit()
            print(u'Your bid has been added', 'success')
            flash(u'Bid successfully sent to seller for review',
                  'alert alert-success')

    else:
        if form.validate_on_submit():
            bid_id = bid_user.id
            bid = form.bidamount.data
            print(bid)
            bid_float = float(bid)
            if bid_float < tool_list_price:
                flash(u'Bid amount needs to be higher than the list price',
                      'alert alert-danger')
                print(u'Bid amount needs to be higher than the list price',
                      'alert alert-danger')
                return redirect(url_for('tool.show', id=tool_id))

            # retrieve current bid
            current_bid = Bid.query.get(bid_id)
            print(current_bid)
            current_bid.bid_amount = bid

            db.session.commit()
            print(u'Your bid has been updated', 'alert alert-success')
            flash(
                u'Success, Your updated bid has been sent to the seller for review', 'alert alert-success')
    # redirect to the item page
    return redirect(url_for('tool.show', id=tool_id))


def check_file(form):
    fp = form.files.data

    # retrieve the file
    filename = fp.filename
    print(fp.filename)
    # Current OS path of the file
    BASE_PATH = os.path.dirname(__file__)

    upload_path = os.path.join(
        BASE_PATH, 'static/img', secure_filename(filename))
    db_upload_path = secure_filename(filename)
    print(db_upload_path)
    fp.save(upload_path)
    return db_upload_path
