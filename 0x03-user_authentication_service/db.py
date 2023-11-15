"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
from user import Base, User

class DB:
    """ Class to manage the Database.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): User's email.
            hashed_password (str): User's hashed password.

        Returns:
            User: User object representing the added user.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the user.

        Returns:
            User: User object representing the found user.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If wrong query arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments.")

    
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user in the database based on the provided user_id and keyword arguments.

        Args:
            user_id (int): User's ID.
            **kwargs: Arbitrary keyword arguments to update the user.

        Raises:
            ValueError: If an invalid argument is passed.
        """
        user_to_update = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if hasattr(user_to_update, key):
                setattr(user_to_update, key, value)
            else:
                raise ValueError(f"Invalid argument: {key}")
            self._session.add(userFound)
            self._session.commit()
        return None
