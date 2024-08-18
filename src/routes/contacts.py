from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User
from src.repository import contacts as repository_contents

from src.schemas.contacts import ContactSchema, ContactUpdateSchema, ContactResponse
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=list[ContactResponse])
async def get_all_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                           db: AsyncSession = Depends(get_db),
                           user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve all contacts with pagination support.

    This endpoint retrieves a list of contacts for the authenticated user,
    with support for pagination through `limit` and `offset` query parameters.

    :param limit: The maximum number of contacts to return (default is 10, minimum is 10, maximum is 500).
    :type limit: int
    :param offset: The number of contacts to skip before starting to collect the result set (default is 0, minimum is 0).
    :type offset: int
    :param db: Database session dependency.
    :type db: AsyncSession
    :param user: The current authenticated user.
    :type user: User
    :return: A list of contacts.
    :rtype: list[ContactResponse]
    """
    contacts = await repository_contents.get_contacts(limit, offset, db, user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a specific contact by its ID.

    This endpoint retrieves a contact for the authenticated user based on the provided contact ID.

    :param contact_id: The ID of the contact to retrieve (must be greater than or equal to 1).
    :type contact_id: int
    :param db: Database session dependency.
    :type db: AsyncSession
    :param user: The current authenticated user.
    :type user: User
    :raises HTTPException: If the contact is not found, a 404 status code is returned.
    :return: The contact details.
    :rtype: ContactResponse
    """
    contact = await repository_contents.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    Create a new contact.

    This endpoint allows the authenticated user to create a new contact.

    :param body: The data for the new contact.
    :type body: ContactSchema
    :param db: Database session dependency.
    :type db: AsyncSession
    :param user: The current authenticated user.
    :type user: User
    :return: The created contact details.
    :rtype: ContactResponse
    :status 201: The contact was created successfully.
    """
    contact = await repository_contents.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    Update an existing contact by its ID.

    This endpoint allows the authenticated user to update the details of a contact.

    :param body: The updated data for the contact.
    :type body: ContactUpdateSchema
    :param contact_id: The ID of the contact to update (must be greater than or equal to 1).
    :type contact_id: int
    :param db: Database session dependency.
    :type db: AsyncSession
    :param user: The current authenticated user.
    :type user: User
    :raises HTTPException: If the contact is not found, a 404 status code is returned.
    :return: The updated contact details.
    :rtype: ContactResponse
    """
    contact = await repository_contents.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    Delete a contact by its ID.

    This endpoint allows the authenticated user to delete a contact.

    :param contact_id: The ID of the contact to delete (must be greater than or equal to 1).
    :type contact_id: int
    :param db: Database session dependency.
    :type db: AsyncSession
    :param user: The current authenticated user.
    :type user: User
    :return: No content on successful deletion.
    :rtype: None
    :status 204: The contact was deleted successfully.
    """
    contact = await repository_contents.delete_contact(contact_id, db, user)
    return contact
