from .object import Object
from .associable import Associable
from .bus import Bus
class Net(Object, Associable):
    def __init__(self, name, associate_with = None):
        Object.__init__(self, name)
        Associable.__init__(self, associate_with)

    def is_part_of_bus(self):
        return isinstance(self.associated_with(), Bus)

    def bus(self):
        if self.is_part_of_bus():
            return self.associated_with()
        else:
            return self

    def verilog_type(self):
        return 'wire'

    def verilog_declare(self):
        if isinstance(self.associated_with(), Bus):
            return self.associated_with().verilog_declare(self)
        else:
            return self.verilog_type() + ' ' + self.get_object_name() + ';'

    def __lt__(self, other):
        if self.is_part_of_bus():
            sw = self.bus().width()
        else:
            sw = 0
            
        if other.is_part_of_bus():
            ow = other.bus().width()
        else:
            ow = 0

        if (sw!=ow):
            return sw>ow

        return self.get_object_name() < other.get_object_name()

