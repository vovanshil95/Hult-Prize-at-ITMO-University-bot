class VkKeyboard(object):

    __slots__ = ('one_time', 'lines', 'keyboard', 'inline')

    def __init__(self, one_time=False, inline=False):
        pass

    def get_keyboard(self):
        return None


    def add_button(self, label, color=None, payload=None):
        pass

    def add_callback_button(self, label, color=None, payload=None):
        pass

    def add_location_button(self, payload=None):
        pass

    def add_vkpay_button(self, hash, payload=None):
        pass

    def add_vkapps_button(self, app_id, owner_id, label, hash, payload=None):
        pass

    def add_openlink_button(self, label, link, payload=None):
        pass

    def add_line(self):
        pass
