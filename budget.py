"""
Budget app by Sofia Zavala
04/12/2021
"""


class Category():
    def __init__(self, na):
        self.name = na
        self.ledger = []

    def get_balance(self):
        """
        Sum all amounts(withdrawals and deposits) in the ledger.
        Return sum.
        """
        balance = 0
        for entry in self.ledger:
            amt = entry['amount']
            balance += amt
        return balance

    def deposit(self, amount, description=''):
        """
        Add an entry to this budget's ledger.
        Given an amount to add to the budget,
        and a description of why the money is going into the budget,
        Record this info in the ledger as a dict.
        """
        dep_entry = {"amount": amount, "description": description}
        self.ledger.append(dep_entry)

    def withdraw(self, amount, description=''):
        """
        Add an entry to this budget's ledger.
        Given an amount to withdraw,
        and a description of why the money is being taken out,
        Record this info in the ledger as a dict,
        iff there are enough funds.
        Return True if the withdraw is success, False otherwise.
        """
        amt = amount * -1
        with_entry = {"amount": amt, "description": description}
        if self.check_funds(amount):
            self.ledger.append(with_entry)
            return True
        else:
            return False

    def transfer(self, amount, category):
        """
        Send money from this budget to a different budget.
        1. Withdraw amount from this budget.
        2. If withdraw successful then deposit amount into other budget.
        Return True if success, False otherwise.
        """
        if self.check_funds(amount):
            with_description = f"Transfer to {category.name}"
            self.withdraw(amount, with_description)
            dep_description = f"Transfer from {self.name}"
            category.deposit(amount, dep_description)
            return True
        else:
            return False

    def check_funds(self, amount):
        """
        Return True if the current balance - amount is greater than zero.
        False, otherwise.
        """
        current_balance = self.get_balance()
        if (current_balance - amount) >= 0:
            return True
        else:
            return False

    def __str__(self):
        """
        Make it pretty.
        Returns a title line, a line for each transaction
        description and amount, and a total line.
        """
        title = '{:*^30}'.format(self.name)
        lines = ''
        for entry in self.ledger:
            des = entry["description"][:23]
            amt = entry["amount"]
            txt = '{description:<23}{amount:>7.2f}'
            line = txt.format(description=des, amount=amt)
            lines += line + '\n'
        total = 'Total: {:.2f}'.format(self.get_balance())
        return title + '\n' + lines + total


def create_spend_chart(categories: list):
    """
    Given a list of Category obj,
    return a histogram of spending.
    Y-axis is percent of total withdrawals.
    X-axis is category name.
    """
    how_many = len(categories)
    head = 'Percentage spent by category\n'
    dash = '    ' + (how_many * 3 * '-') + '-\n'

    def spent(category: Category):
        """
        For a category,
        Return spent, the sum of withdrawals.
        """
        spent = 0
        for entry in category.ledger:
            if entry["amount"] < 0:
                spent += entry["amount"]
        return spent

    total_spent = sum([spent(cat) for cat in categories])

    def percentage(category: Category):
        percent = (spent(category) / total_spent) * 100
        percent -= percent % 10
        return percent

    def y_axis():
        tens = [num for num in range(0, 101, 10)]
        tens.sort(reverse=True)
        percents = [percentage(cat) for cat in categories]
        lines = ''
        for num in tens:
            txt = '{num:>3}|'
            lines += txt.format(num=num)
            for x in range(len(percents)):
                if percents[x] == num:
                    bar = 'o'
                    percents[x] -= 10
                else:
                    bar = ' '
                lines += '{bar:^3}'.format(bar=bar)
            lines += ' \n'
        return lines

    def x_axis():
        names = []
        max_name = 0
        for cat in categories:
            letters = list(cat.name)
            names.append(letters)
            length = len(letters)
            if length > max_name:
                max_name = length
        for name in names:
            while len(name) < max_name:
                name.append(' ')
                if len(name) == max_name:
                    break
        lines = ''
        for x in range(max_name):
            lines += '    '
            for name in names:
                lines += '{:^3}'.format(name[x])
            lines += ' \n'
        lines = lines[:-1]
        return lines
    return head + y_axis() + dash + x_axis()


if __name__ == '__main__':
    t1 = Category('Groceries')

    t1.deposit(1000.99, 'paycheck')
    t1.deposit(0, 'null')
    t1.deposit(.99, 'loose change')

    status = t1.withdraw(0, 'null')
    t1.withdraw(199.99, 'BLT ingredients')
    status = t1.withdraw(.99, 'a very long description of a snack')
    status = t1.withdraw(2000.99, 'fancy snack')
    # Should fail bc lack of funds

    t2 = Category('Clubbing')
    t2.deposit(300.99, 'paycheck')
    status = t1.transfer(100, t2)
    t2.withdraw(100, 'Tresor')
    t2.withdraw(100, 'Leather night')

    print(t1)
    print(t2)

    print(create_spend_chart([t1, t2]))
