import datetime
import heapq
import xml.etree.ElementTree as ET

start_time = datetime.datetime.now()
print(f"Processing started at: {start_time}\n")

tree = ET.parse('orders 1.xml')

class Book:
  def __init__(self,book):
    self.book = book
    self.orders = {} # orderId -> vol, price, operation
    self.buy_heap = [] # maxHeap
    self.sell_heap = [] # minHeap

  def add_order(self, orderId, volume, price, operation):
    if operation == "BUY":
      while self.sell_heap and self.sell_heap[0][0] <= price and volume > 0:
        temp_price, temp_orderId = heapq.heappop(self.sell_heap)
        if temp_orderId not in self.orders:
          continue
        temp_volume = self.orders[temp_orderId][0]
        if temp_volume >= volume:
          temp_volume = temp_volume - volume
          self.orders[temp_orderId] = [temp_volume,temp_price,self.orders[temp_orderId][2]]
          volume = 0
          heapq.heappush(self.sell_heap,(temp_price,temp_orderId))
        else:
          volume = volume - temp_volume
          del self.orders[temp_orderId]

      if volume > 0:
        heapq.heappush(self.buy_heap, (-price,orderId))

    else:
      while self.buy_heap and -self.buy_heap[0][0] >= price and volume > 0:
        temp_price, temp_orderId = heapq.heappop(self.buy_heap)
        if temp_orderId not in self.orders:
          continue
        temp_price = -temp_price
        temp_volume = self.orders[temp_orderId][0]
        if temp_volume >= volume:
          temp_volume = temp_volume - volume
          self.orders[temp_orderId] = [temp_volume,temp_price,self.orders[temp_orderId][2]]
          volume = 0
          heapq.heappush(self.buy_heap,(-temp_price,temp_orderId))
        else:
          volume = volume - temp_volume
          del self.orders[temp_orderId]

      if volume > 0:
        heapq.heappush(self.sell_heap, (price,orderId))
    
    if volume > 0:
      self.orders[orderId] = [volume, price, operation]

  def delete_order(self, orderId):
    if orderId in self.orders:
      del self.orders[orderId]


  def show(self):
    print(f"book: {self.book}")
    buy = "Buy"
    c = "--"
    sell = "Sell"
    print(f"{buy: >12}{c : ^4}{sell : <2}")
    print("============================")
    self.buy_heap = sorted(self.buy_heap)
    self.sell_heap = sorted(self.sell_heap)
    sells, buys = [], []

    for price, orderId in self.buy_heap:
      if orderId in self.orders:
        buys.append((self.orders[orderId][0],-price))

    for price, orderId in self.sell_heap:
      if orderId in self.orders:
        sells.append((self.orders[orderId][0],price))


    max_len = max(len(buys), len(sells))

    for i in range(max_len):
      buy = f"{buys[i][0]}@{buys[i][1]}" if i < len(buys) else ""
      c = "--"
      sell = f"{sells[i][0]}@{sells[i][1]}" if i < len(sells) else ""
      print(f"{buy: >12}{c : ^4}{sell : <2}")



root = tree.getroot()
books = {}

# Iterate through the elements in the XML
for element in root:
    if element.tag == 'AddOrder':
        book_name = element.get('book')
        order_id = int(element.get('orderId'))
        operation = element.get('operation')
        price = float(element.get('price'))
        volume = int(element.get('volume'))

        if book_name not in books:
            books[book_name] = Book(book_name)

        books[book_name].add_order(order_id, volume,price,operation)

    elif element.tag == 'DeleteOrder':
        book_name = element.get('book')
        order_id = int(element.get('orderId'))

        if book_name in books:
            books[book_name].delete_order(order_id)


sorted_books = []
for key in books.keys():
  sorted_books.append(key)

sorted_books = sorted(sorted_books)

for book in sorted_books:
  print("y")
  books[book].show()
  print()


completion_time = datetime.datetime.now()
duration = completion_time - start_time

print(f"Processing completed at: {completion_time}")
print(f"Processing Duration: {duration.total_seconds()} seconds")