#!/usr/bin/python3
class generator():
    def __init__(self, name, capacity, kwh_cost, durability):
        self.name = name
        self.kwh_cost = kwh_cost
        self.capacity = capacity
        self.durability = durability

    def __str__(self):
        return (f'''This is generator {self.name}
                The Capacity of the generator is: {self.capacity} MW
                The Cost of 1 unit (kWh) is: {self.kwh_cost}$
                The durability of the generator is: {self.durability} days'''.replace(" "*4, ""))
