from dataclasses import dataclass
from typing import List, Optional, Tuple
from db import get_connection
import sqlite3


@dataclass
class UserProfile:
    """
    Entity class representing a user profile (role).
    Example profiles: User Admin, Fundraiser, Donor, Platform Management.
    """
    profileId: Optional[int]
    profileName: str
    profileDescription: str

    @classmethod
    def fromRow(cls, row) -> "UserProfile":
        """
        Create a UserProfile instance from a database row.
        """
        return cls(
            profileId = row["profile_id"],
            profileName = row["profile_name"],
            profileDescription= row["profile_desc"]
        )

    @classmethod
    def profileExists(cls, profileName: str) -> bool:
        """
        checks if a user profile with the given name exists.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT 1
            FROM user_profile
            WHERE LOWER(profile_name) = LOWER(?)
            """, #checks if matching profile exists, lower() allows case-insensitive
            (profileName.strip(),)
        )
        row = cursor.fetchone() #gets first matching results if there is any
        connection.close()
        return row is not None #return true if matching profile found if not return false


    @classmethod
    def createProfile(cls, profileName: str, profileDescription: str) -> Tuple[bool, str]:
        """
        Create and store a new user profile to databse.
        """
        #Check for duplicate profile name before creating a new profile.
        if cls.profileExists(profileName):
            return False, f"Profile '{profileName}' already exists"
        else:
            connection = get_connection()
            cursor = connection.execute(
                """
                INSERT INTO user_profile (profile_name, profile_desc)
                Values (?, ?)
                """,
                (profileName.strip(), profileDescription.strip())
            )
            connection.commit()
            cls(
                profileId = cursor.lastrowid,
                profileName=profileName.strip(),
                profileDescription=profileDescription.strip()
            )
            connection.close()
            return True, f"Profile '{profileName}' created successfully."
        
    # A method to retrieve all profiles for demo purposes.
    @classmethod
    def getAllProfiles(cls) -> List["UserProfile"]:
        """
        Return all stored profiles.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT profile_id, profile_name, profile_desc
            FROM user_profile
            ORDER BY profile_id
            """
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def searchProfiles(cls, searchTerm: str) -> List["UserProfile"]:
        """
        Search user profiles by name or description
        """
        connection = get_connection()
        keyword = f"%{searchTerm.strip()}%"
        cursor = connection.execute(
            """
            SELECT profile_id, profile_name, profile_desc
            FROM user_profile
            WHERE LOWER(profile_name) LIKE LOWER(?)
                or LOWER(profile_desc) LIKE LOWER(?)
            ORDER BY profile_id
            """, #LIKE used for partial matching
            (keyword, keyword)
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]
    
    @classmethod
    def updateProfile(cls, profileId: int, profileName: str, profileDescription: str) -> Tuple[bool, str]:
        """
        Update an existing user profile in the database.
        """
        connection = get_connection()

        try:
            # Check if the profile exists before updating
            cursor = connection.execute(
                "SELECT 1 FROM user_profile WHERE profile_id = ?",
                (profileId,)
            )
            row = cursor.fetchone()

            # If the profile does not exist, return False with an error message
            if not row:
                return False, "Profile id does not exist."

            # Update the profile with the new name and description
            connection.execute(
                """
                UPDATE user_profile
                SET profile_name = ?, profile_desc = ?
                WHERE profile_id = ?
                """,
                (profileName.strip(), profileDescription.strip(), profileId)
            )

            connection.commit()
            return True, "Profile updated successfully."

        # Profile name is unique, so if the new name already exists for another profile, an IntegrityError will be raised.    
        except sqlite3.IntegrityError:
            return False, "Profile name already exists."
        
        # Catch any other database errors that may occur and return a generic error message.
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        
        finally:
            connection.close()
    
    @classmethod
    def deleteProfile(cls, profileId: int) -> Tuple[bool, str]:
        """
        Delete an existing user profile from the database.
        """
        connection = get_connection()
        try:
            # Check if the profile exists before deleting
            cursor = connection.execute(
                "SELECT 1 FROM user_profile WHERE profile_id = ?",
                (profileId,)
            )
            row = cursor.fetchone()

            # If the profile does not exist, return False with an error message
            if not row:
                return False, "Profile id does not exist."

            # Delete the profile
            connection.execute(
                "DELETE FROM user_profile WHERE profile_id = ?",
                (profileId,)
            )

            connection.commit()
            return True, "Profile deleted successfully."
        
        # If the profile is associated with existing users, an IntegrityError will be raised due to foreign key constraint.
        except sqlite3.IntegrityError:
            return False, "Cannot delete profile as it is associated with existing users."

        # Catch any other database errors that may occur and return a generic error message.
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        
        finally:
            connection.close()
