from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Database(SQLAlchemy):

    def init(self, app: Flask):
        """Create all database tables and seed initial data if needed."""
        from app import models  #type: ignore[import]
        
        self.init_app(app)
        self.create_all()
        self.seed_initial_data()
       
    def seed_initial_data(self):
        """Seed the database with initial data."""
        self._seed_categories()
        self._seed_locations()

    def _seed_categories(self):
        """Seed the database with default categories."""
        from app.models.category import Category
        if self.session.query(Category).count() > 0:
            return
        
        categories = [
            'Router',
            'Printer', 
            'NVR',
            'Laptop',
            'Smart Speaker',
            'Smart TV',
            'Smart Phone',
            'Tablet',
            'Desktop',
            'Smart Radio',
            'AP',
            'NAS'
        ]
        
        for category_name in categories:
            category = Category()
            category.name = category_name
            self.session.add(category)
        self.session.commit()

    def _seed_locations(self):
        """Seed the database with default locations."""
        from app.models.location import Location
        if self.session.query(Location).count() > 0:
            return
       
        locations = [
            'Bedroom',
            'Kitchen',
            'Living',
            'Rumpus',
            'Hallway',
            'Work',
            'Study',
            'Dining',
            'Garage',
            'Lounge',
            'Bathroom',
        ]
        
        for location_name in locations:
            location = Location()
            location.name = location_name
            self.session.add(location)
        self.session.commit()
