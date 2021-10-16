
# models.py file
from django.db import models
from django_matplotlib import MatplotlibFigureField
from matplotlib.pyplot import figure


class graph(models.Model):
    figure = MatplotlibFigureField(figure='graph')
