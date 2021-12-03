'''
Generates Mock Data for testing purposes.
run in django shell
"python webventory/manage.py shell webventory/home/gen_mock_data.py"
'''

import random
from datetime import datetime

from models import Item, ItemHistory

items = []
# Generates Random Items
for _ in range(100):
    new_item = Item(name="test", description="this is a description", quantity=f'{random.randint(0, 1000)}',
                    price=f'{random.random() * random.randint(0, 10):.2f}', user_visability='true')
    new_item.save()
    items.append(new_item)
# Generates Random Changes
for _ in range(25):
    for item in items:
        ItemHistory(item_id=item, date_of_change=datetime.now(), price_before=item.price,
                    price_after=f'{random.random() * random.randint(0, 10):.2f}',
                    quantity_before=item.quantity, quantity_after=f'{random.randint(0, 1000)}').save()
