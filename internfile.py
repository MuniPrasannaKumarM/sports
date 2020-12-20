import pymongo
from flask import Flask, request, render_template
from flask import session as web_session
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["intern"]
collection = database["miskaa"]
app = Flask(__name__)
app.secret_key = 'super secret key'
# importing and initializing of DataBase is done and collections are created for the user
@app.route("/", methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        user = "miskaa"
        web_session['user'] = user
        dbup = collection.find({'username': user})
        count = 0
        for i in dbup:
            count += 1
        if count == 0:
            collection.insert_one({'username': user, 'items': []})  # inserting a document in the collection for the user
        getitems = request.form.get('getitems')             # used to get the items from the cart
        if getitems == 'GET ITEMS':
            mj = {'username': user}
            m = collection.find(mj)
            for i in m:
                print(i)
            for j in i['items']:
                print(j)
            return render_template('getitems.html', user=user, length1=len(i['items']), list2=i['items'])
    return render_template('mainpage1.html')

@app.route('/additems',methods=['POST', 'GET'])    # used to add the items to the cart by entering the data in the text box
def additems():
    user = web_session['user']
    item = request.form.get('itemadd')
    print(item)
    if item != None:
        print("coming")
        collection.update_one({'username': user}, {'$push': {'items': item}})
    return render_template('additems.html')

@app.route('/removeitems',methods=['POST', 'GET'])              # used to remove the element from the cart by removing and inserting the updated data
def removeitems():
    if request.method == 'POST':
        getItem = request.form.get('itemrem')
        user = web_session['user']
        myquery = {"username": user}
        res = collection.find(myquery)
        ind = 0
        for ind in res:
            print(ind)
        listitem = ind['items']
        listitem.remove(getItem)
        print(listitem)
        collection.update_one({'username': user}, {'$set': {'items': listitem}})
    return render_template('removeitems.html')

if __name__ == '__main__':
    app.run(debug=True)

