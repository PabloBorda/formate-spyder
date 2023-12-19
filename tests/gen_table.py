# -*- coding: utf-8 -*-
import tablib

data = tablib.Dataset(headers=['First Name', 'Last Name', 'Age'])
for i in [('Kenneth', 'Reitz', 22), ('Bessie', 'Monke', 21)]:
    data.append(i)
print(str(data.export("html")))