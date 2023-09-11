from sqlalchemy.orm import DeclarativeBase
from typing import Any
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy.orm import mapped_column, Mapped


class Base(DeclarativeBase):
    pk: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    def __repr__(self) -> str:
        return self._repr(id=self.id)

    def _repr(self, **fields: Any) -> str:
        """
        Helper for __repr__
        """
        field_strings = list()
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"
