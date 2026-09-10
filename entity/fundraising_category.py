from dataclasses import dataclass
from typing import List, Optional, Tuple
from db import get_connection
import sqlite3

@dataclass
class FundraisingCategory:
    """
    Entity class representing a fundraising category.
    Example categories: Medical, Education, Community Support,Emergency Relief, etc.
    """
    categoryId: Optional[int]
    categoryName: str

    @classmethod
    def fromRow(cls, row) -> "FundraisingCategory":
        """
        Create a FundraisingCategory instance from a database row.
        """
        return cls(
            categoryId = row["category_id"],
            categoryName = row["category_name"]
        )
    
    @classmethod
    def categoryExists(cls, categoryName: str) -> bool:
        """
        Checks if a fundraising category with the same name exists.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT 1
            FROM category
            WHERE LOWER(category_name) = LOWER(?)
            """, #checks if matching category exists, lower() allows case-insensitive
            (categoryName.strip(),)
        )
        row = cursor.fetchone() #gets first matching results if there is any
        connection.close()
        return row is not None #return true if matching category found if not return false
    
    @classmethod
    def createCategory(cls, categoryName: str) -> Tuple[bool, str]:
        """
        Create and store a new fundraising category to database.
        """
        #Check for duplicate category name before creating a new category.
        if cls.categoryExists(categoryName):
            return False, f"Category '{categoryName}' already exists"
        else:
            connection = get_connection()
            cursor = connection.execute(
                """
                INSERT INTO category (category_name)
                Values (?)
                """,
                (categoryName.strip(),)
            )
            connection.commit()
            cls(
                categoryId = cursor.lastrowid,
                categoryName = categoryName.strip()
            )
            connection.close()
            return True, f"Category '{categoryName}' created successfully"
    
    @classmethod
    def getAllCategories(cls) -> List["FundraisingCategory"]:
        """
        Retrieve all fundraising categories from the database.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT category_id, category_name
            FROM category
            ORDER BY category_id
            """
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]

    @classmethod
    def getCategoryById(cls, categoryId: int) -> Optional["FundraisingCategory"]:
        """
        Retrieve one fundraising category by category ID.
        """
        connection = get_connection()
        cursor = connection.execute(
            """
            SELECT category_id, category_name
            FROM category
            WHERE category_id = ?
            """,
            (categoryId,)
        )
        row = cursor.fetchone()
        connection.close()

        if not row:
            return None

        return cls.fromRow(row)
    
    @classmethod
    def searchCategories(cls, searchTerm: str) -> List["FundraisingCategory"]:
        """
        Search for fundraising categories that match the search term.
        """
        connection = get_connection()
        keyword = f"%{searchTerm.strip()}%"
        cursor = connection.execute(
            """
            SELECT category_id, category_name
            FROM category
            WHERE LOWER(category_name) LIKE LOWER(?)
            ORDER BY category_id
            """,
            (keyword,)
        )
        rows = cursor.fetchall()
        connection.close()

        return [cls.fromRow(row) for row in rows]
    
    @classmethod
    def updateCategory(cls, categoryId: int, newCategoryName: str) -> Tuple[bool, str]:
        """
        Update the name of an existing fundraising category.
        """

        connection = get_connection()

        try:
            # Check if the category exists before updating
            cursor = connection.execute(
                "SELECT 1 FROM category WHERE category_id = ?",
                (categoryId,)
            )
            row = cursor.fetchone()

            # If the category does not exist, return False with an error message
            if not row:
                return False, "Category id does not exist."

            # Update the category with the new name
            connection.execute(
                """
                UPDATE category
                SET category_name = ?
                WHERE category_id = ?
                """,
                (newCategoryName.strip(), categoryId)
            )

            connection.commit()
            return True, "Category updated successfully."

        # Category name is unique, so if the new name already exists for another category, an IntegrityError will be raised.    
        except sqlite3.IntegrityError:
            return False, "Category name already exists."
        
        # Catch any other database errors that may occur and return a generic error message.
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        
        finally:
            connection.close()

    @classmethod
    def deleteCategory(cls, categoryId: int) -> Tuple[bool, str]:
        """
        Delete an existing fundraising category from the database.
        """
        connection = get_connection()

        try:
            # Check if the category exists before deleting
            cursor = connection.execute(
                "SELECT 1 FROM category WHERE category_id = ?",
                (categoryId,)
            )
            row = cursor.fetchone()

            # If the category does not exist, return False with an error message
            if not row:
                return False, "Category id does not exist."

            # Delete the category
            connection.execute(
                """
                DELETE FROM category
                WHERE category_id = ?
                """,
                (categoryId,)
            )

            connection.commit()
            return True, "Category deleted successfully."

        # If the category is associated with existing fundraising activities, an IntegrityError will be raised due to foreign key constraint.    
        except sqlite3.IntegrityError:
            return False, "Category is associated with existing fundraising activities."

        # Catch any other database errors that may occur and return a generic error message.
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        
        finally:
            connection.close()
