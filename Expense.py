class Expense:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

expenses = [
    Expense("Milk", "Food", 50),
    Expense("Bus", "Travel", 30),
    Expense("Book", "Education", 200),
    Expense("Rice", "Food", 500),
    Expense("Petrol", "Travel", 300)
]

print("Expenses:")
for e in expenses:
    print(e.name, "-", e.category, "-", e.amount)

total = 0
for e in expenses:
    total += e.amount

print("\nTotal Spending:", total)

category_total = {}

for e in expenses:
    if e.category in category_total:
        category_total[e.category] += e.amount
    else:
        category_total[e.category] = e.amount

print("\nCategory-wise Spending:")
for category, amount in category_total.items():
    print(category, ":", amount)