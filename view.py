import eel
import search
import desktop

app_name="html"
end_point="index.html"
size=(800,800)


global item_master

def main_1(csv_name):#メニューの登録処理
    ITEM_MASTER_CSV_PATH= './' + csv_name
    # CSVからマスタへ登録
    item_master = add_item_master_by_csv(ITEM_MASTER_CSV_PATH) 

def main_2(buy_item_code,buy_item_count):#商品番号&個数入力する処理
    order=Order(item_master)
    order.input_order(buy_item_code,buy_item_count)

def main_3():#購入する商品番号&個数表示する処理
    order=Order(item_master)
    order.view_order() 

def main_4(change_money):#支払金額入力~お釣り受け取りまでの処理
    order=Order(item_master)
    order.input_change_money(change_money)

@ eel.expose
def main_1(csv_name):
    search.main_1(csv_name)

@ eel.expose
def main_2(buy_item_code,buy_item_count):
    search.main_2(buy_item_code,buy_item_count)

@ eel.expose
def main_3():
    search.main_3()

@ eel.expose
def main_4(pay_money):
    search.main_4(pay_money)

desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)