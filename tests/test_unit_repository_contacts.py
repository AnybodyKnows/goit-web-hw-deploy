import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Contacts, User
from src.schemas.contacts import ContactSchema, ContactUpdateSchema
from src.repository.contacts import get_contacts, get_contact, create_contact, update_contact, delete_contact


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, email="test@example.com")
        # self.mock_contact = Contacts(id=1, user_id=1, name="Test", email="test@example.com", phone="1234567890")
        # self.mock_contacts = [self.mock_contact]
        # self.mock_schema = ContactSchema()
        # self.mock_update_schema = ContactUpdateSchema()

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contacts(id=1, full_name="test_name1", email="test_email1",
                     phone_number="1236547891", user=self.user),
            Contacts(id=2, full_name="test_name2", email="test_email2",
                     phone_number="9876543210", user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact_id = 1
        contacts = [
            Contacts(id=1, full_name="test_name1", email="test_email1",
                     phone_number="1236547891", user=self.user),
            Contacts(id=2, full_name="test_name2", email="test_email2",
                     phone_number="9876543210", user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalar_one_or_none.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contact(contact_id, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactSchema(full_name="test_name", email="test_email@example.com",
                             phone_number="1234567890", birthday="2024-01-01")
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contacts)
        self.assertEqual(result.full_name, body.full_name)
        self.assertEqual(result.email, body.email)

    async def test_update_contact(self):
        contact_id = 1
        body = ContactUpdateSchema(full_name="test_name", email="test_email@example.com",
                                   phone_number="9876543210", birthday="2024-01-01")
        contacts = Contacts(id=1, full_name="test_name1", email="test_email@example.com",
                            phone_number="1236547891", birthday="2024-01-01", user=self.user)
        mocked_contacts = MagicMock()
        mocked_contacts.scalar_one_or_none.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await update_contact(contact_id, body, self.session, self.user)
        self.assertEqual(result.phone_number, body.phone_number)
