class Employee():
    company = 'Stack'

    def __init__(this, name):
        this.name = name
        this.company = Employee.company


employee1 = Employee('Mark Hana')
employee1.company = 'Tech Gmbh'

print(employee1._attribute)

