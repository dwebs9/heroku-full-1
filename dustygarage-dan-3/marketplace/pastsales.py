

# in tools.py  create route:

@bp.route('/sellhistory/<userid>', methods=["POST", "GET"])
@login_required
def userdash(userid):

    print(userid)
    unsold = ""

    tool = Tool.query.filter(
        Tool.sold_status != unsold).filter_by(user_id=userid).all()
    print(tool)

    return render_template('tools/sellhistory.html', userid=userid, tool=tool, bids=bids)



#in html iterate over bootstrap table


