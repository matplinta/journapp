# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
# from app.models.color import ColorEnum  # noqa
from app.models.note import Note  # noqa
from app.models.tag import Tag  # noqa
from app.models.user import User  # noqa
