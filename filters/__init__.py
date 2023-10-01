from .private_chat import IsPrivate
from .admins import IsAdmin
from loader import dp
dp.filters_factory.bind(IsPrivate)
dp.filters_factory.bind(IsAdmin)