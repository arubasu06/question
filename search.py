import pandas as pd
import eel
import sys
import datetime

RECEIPT_FOLDER="./receipt"

class Food_MenuItem:
    def __init__(self, item_code, item_name, price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price

    def info(self):
        return self.item_name + ': ¥' + str(self.price)

class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        self.set_datetime()
    
    def set_datetime(self):
        self.datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    def add_item_order(self, item_code, item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)

    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))

    def get_item_data(self,buy_item_code):
            for m in self.item_master:
                if buy_item_code==m.item_code:
                    return m.item_name,m.price

    def input_order(self,buy_item_code,buy_item_count):
        item_info=self.get_item_data(buy_item_code)
        eel.buy_item_view_js("{0[0]} ({0[1]} 円) が {1} 個注文されました".format(item_info,buy_item_count))
        self.item_order_list.append(buy_item_code)
        self.item_count_list.append(buy_item_count)

    def view_order(self):
        number=1
        self.sum_price=0
        self.sum_count=0
        self.receipt_name="receipt_{}.log".format(self.datetime)
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("注文商品一覧\n")
        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            result=self.get_item_data(item_order)
            self.sum_price+=result[1]*int(item_count)
            self.sum_count+=int(item_count)
            receipt_data="{0}.{2}({1}) : ￥{3:,}　{4}個 = ￥{5:,}".format(number,item_order,result[0],result[1],item_count,int(result[1])*int(item_count))
            self.write_receipt(receipt_data)
            eel.pay_money_js("{0}.{2}({1}) : ￥{3:,}　{4}個 = ￥{5:,}".format(number,item_order,result[0],result[1],item_count,int(result[1])*int(item_count)))
            number+=1

        # 合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("合計金額:￥{:,} {}個".format(self.sum_price,self.sum_count))
        eel.pay_money_js("-----------------------------------------------")
        eel.pay_money_js("合計金額:￥{:,} 購入数{}個".format(self.sum_price,self.sum_count))
        eel.pay_money_js("-----------------------------------------------")

    def input_change_money(self,pay_money):
        self.change_money = int(pay_money) - self.sum_price
        if self.change_money>=0:
            print("投入金額は" + str(pay_money) + '円です')
            print("お釣りは" + str(self.change_money) + '円です')
            eel.change_money_js("お釣り  ：{}円".format(self.change_money))
            print("お買い上げありがとうございます!")
            eel.change_money_js("お買い上げありがとうございます!")
        else:
            print("お預かり金が不足しています。再度入力してください")
            eel.change_money_js("お預かり金が不足しています。再度入力してください")

    def write_receipt(self,text):
        print(text)
        with open(RECEIPT_FOLDER + "\\" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n")

def add_item_master_by_csv(csv_path):
    print("-----------------------")
    item_master=[]
    count=0
    try:
        item_master_df=pd.read_csv(csv_path,dtype={"item_code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
        for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
            item_master.append(Food_MenuItem(item_code,item_name,price))
            print("{}:{}円  商品番号({})".format(item_name,price,item_code))
            eel.menu_view_js("{}:{}円  商品番号:{}".format(item_name,price,item_code))
            count+=1
        print("{}品の登録を完了。".format(count))
        eel.menu_view_js("-----------{}品の登録を完了-----------".format(count))
        
        print("-----------------------")
        return item_master

    except:
        print("-----------マスタ登録が失敗-----------")
        print("-----------------------")
        eel.menu_view_js("-----------マスタ登録が失敗-----------")
        sys.exit()

