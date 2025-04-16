class AuthService:
    def __init__(self):
        # In a real application, you would connect to a database
        # This is just a simple demo implementation
        self.users = {
            "admin": {
                "password": "admin123",
                "role": "admin",
                "name": "Administrator"
            },
            "user": {
                "password": "user123",
                "role": "user",
                "name": "Test User"
            },
            # Add more test users here if needed
            "test": {
                "password": "test123",
                "role": "user",
                "name": "Test Account"
            }
        }

    def login(self, username, password):
        """
        Authenticate a user
        Returns: dict with success status and user info or error message
        """
        user = self.users.get(username)
        
        if not user:
            return {
                "success": False,
                "message": "User not found"
            }
            
        if user["password"] != password:
            return {
                "success": False,
                "message": "Invalid password"
            }
            
        return {
            "success": True,
            "user": {
                "username": username,
                "role": user["role"],
                "name": user["name"]
            }
        }

    def register(self, username, password, name):
        """
        Register a new user
        Returns: dict with success status and message
        """
        if username in self.users:
            return {
                "success": False,
                "message": "Username already exists"
            }
            
        self.users[username] = {
            "password": password,
            "role": "user",
            "name": name
        }
        
        return {
            "success": True,
            "message": "User registered successfully"
        }