from quackORM import quack, quackTable, quackDataTypes
import os
from datetime import datetime

testquack = quack(dbtype='mysql', dbname='testquack', dropDBOnMigrate=True)

class animal(quackTable):
    def __init__(self):
        self.nombre = quackDataTypes.String(required=True)
        self.nombrecientifico = quackDataTypes.String(required=True)
        self.descripcion = quackDataTypes.String(required=True)

class persona(quackTable):
    def __init__(self):
        self.dpi = quackDataTypes.String(required=True)
        self.estadocivil = quackDataTypes.String(required=False)

class cuidador(persona, quackTable):
    def __init__(self):
        self.nombre = quackDataTypes.String(required=True)
        self.descripcion = quackDataTypes.String(required=True)

class pato(animal, cuidador, quackTable):
    def __init__(self):
        self.edad = quackDataTypes.Int(required=True)
        self.peso = quackDataTypes.Float()

testquack.migrate(persona, animal, pato, cuidador)
# print(dir(pato()))