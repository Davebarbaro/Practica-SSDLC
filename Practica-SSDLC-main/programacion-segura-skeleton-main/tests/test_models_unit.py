"""
Tests unitarios para los modelos y esquemas de datos.
Estos tests NO requieren levantar el servidor ni la base de datos.
"""
import pytest
from pydantic import ValidationError
from app.models.schemas import UserCreate, UserOut, Token, MessageCreate, MessageOut


class TestUserCreateSchema:
    """Tests para el esquema de creación de usuarios"""

    def test_valid_user_create(self):
        """Verificar que un usuario válido se crea correctamente"""
        user_data = {
            "username": "testuser",
            "password": "SecurePass123!",
            "email": "test@example.com"
        }
        user = UserCreate(**user_data)  # crear instancia del esquema

        assert user.username == "testuser"  # verificar username
        assert user.password == "SecurePass123!"  # verificar password
        assert user.email == "test@example.com"  # verificar email

    def test_username_too_short(self):
        """Verificar que un username demasiado corto falla la validación"""
        user_data = {
            "username": "ab",  # Menos de 3 caracteres
            "password": "SecurePass123!",
            "email": "test@example.com"
        }

        with pytest.raises(ValidationError) as exc_info:  # Se espera un error de validación
            UserCreate(**user_data)

        assert "username" in str(exc_info.value)  # Verificar que el error es por el username

    def test_username_too_long(self):
        """Verificar que un username demasiado largo falla la validación"""
        user_data = {
            "username": "a" * 51,  # Más de 50 caracteres
            "password": "SecurePass123!",
            "email": "test@example.com"
        }

        with pytest.raises(ValidationError) as exc_info:  # Se espera un error de validación
            UserCreate(**user_data)

        assert "username" in str(exc_info.value)

    def test_password_too_short(self):
        """Verificar que una contraseña demasiado corta falla la validación"""
        user_data = {
            "username": "testuser",
            "password": "short",  # Menos de 8 caracteres
            "email": "test@example.com"
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        assert "password" in str(exc_info.value)  # Verificar que el error es por la contraseña

    def test_password_too_long(self):
        """Verificar que una contraseña demasiado larga falla la validación"""
        user_data = {
            "username": "testuser",
            "password": "a" * 129,  # Más de 128 caracteres
            "email": "test@example.com"
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        assert "password" in str(exc_info.value)  # Verificar que el error es por la contraseña

    def test_invalid_email_format(self):
        """Verificar que un email inválido falla la validación"""
        user_data = {
            "username": "testuser",
            "password": "SecurePass123!",
            "email": "not-an-email"  # Email inválido
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        assert "email" in str(exc_info.value)  # Verificar que el error es por el email

    def test_missing_required_fields(self):
        """Verificar que faltan campos requeridos falla la validación"""
        user_data = {
            "username": "testuser"
            # Faltan password y email
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        error_str = str(exc_info.value)
        assert "password" in error_str or "email" in error_str  # Verificar que el error es por los campos faltantes


class TestUserOutSchema:
    """Tests para el esquema de salida de usuarios"""

    def test_valid_user_out(self):
        """Verificar que un UserOut válido se crea correctamente"""
        user_data = {
            "id": 1,
            "username": "testuser",
            "role": "user"
        }
        user = UserOut(**user_data)  # crear instancia del esquema

        assert user.id == 1 
        assert user.username == "testuser"
        assert user.role == "user"   #se verifican que los campos son correctos

    def test_user_out_missing_field(self):
        """Verificar que falta un campo requerido falla la validación"""
        user_data = {
            "id": 1,
            "username": "testuser"
            # Falta role
        }

        with pytest.raises(ValidationError):
            UserOut(**user_data)    # Se espera un error de validación por falta de campo


class TestTokenSchema:
    """Tests para el esquema de tokens"""

    def test_valid_token(self):
        """Verificar que un token válido se crea correctamente"""
        token_data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user"
        }
        token = Token(**token_data)

        assert token.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        assert token.token_type == "bearer"
        assert token.username == "testuser"
        assert token.email == "test@example.com"
        assert token.role == "user"  #se verifican que los campos son correctos 

    def test_token_default_type(self):
        """Verificar que el token_type tiene un valor por defecto"""
        token_data = {
            "access_token": "test_token",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user"
        }
        token = Token(**token_data)

        assert token.token_type == "bearer"  # Valor por defecto

    def test_token_missing_required_fields(self):
        """Verificar que faltan campos requeridos falla la validación"""
        token_data = {
            "access_token": "test_token"
            # Faltan username, email, role
        }

        with pytest.raises(ValidationError):
            Token(**token_data)    # Se espera un error de validación por falta de campos


class TestMessageCreateSchema:
    """Tests para el esquema de creación de mensajes"""

    def test_valid_message_create(self):
        """Verificar que un mensaje válido se crea correctamente"""
        message_data = {
            "content": "Este es un mensaje de prueba"
        }
        message = MessageCreate(**message_data)

        assert message.content == "Este es un mensaje de prueba"  #se verifica que el contenido es correcto

    def test_message_empty_content(self):
        """Verificar que un mensaje vacío falla la validación"""
        message_data = {
            "content": ""  # Contenido vacío
        }

        with pytest.raises(ValidationError) as exc_info:  # Se espera un error de validación
            MessageCreate(**message_data)

        assert "content" in str(exc_info.value)  # Verificar que el error es por el contenido

    def test_message_too_long(self):
        """Verificar que un mensaje demasiado largo falla la validación"""
        message_data = {
            "content": "a" * 501  # Más de 500 caracteres
        }

        with pytest.raises(ValidationError) as exc_info: # Se espera un error de validación
            MessageCreate(**message_data)

        assert "content" in str(exc_info.value)  # Verificar que el error es por el contenido

    def test_message_exact_max_length(self):
        """Verificar que un mensaje con exactamente 500 caracteres es válido"""
        message_data = {
            "content": "a" * 500  # Exactamente 500 caracteres
        }
        message = MessageCreate(**message_data)  # crear instancia del esquema

        assert len(message.content) == 500  # Verificar que el contenido tiene 500 caracteres y es válido

    def test_message_exact_min_length(self):
        """Verificar que un mensaje con exactamente 1 carácter es válido"""
        message_data = {
            "content": "a"  # Exactamente 1 carácter
        }
        message = MessageCreate(**message_data)  # crear instancia del esquema

        assert len(message.content) == 1  # Verificar que el contenido tiene 1 carácter y es válido


class TestMessageOutSchema:
    """Tests para el esquema de salida de mensajes"""

    def test_valid_message_out(self):
        """Verificar que un MessageOut válido se crea correctamente"""
        message_data = {
            "id": 1,
            "content": "Mensaje de prueba",
            "owner_id": 5
        }
        message = MessageOut(**message_data)  # crear instancia del esquema

        assert message.id == 1
        assert message.content == "Mensaje de prueba"
        assert message.owner_id == 5  #se verifican que los campos son correctos

    def test_message_out_missing_field(self):
        """Verificar que falta un campo requerido falla la validación"""
        message_data = {
            "id": 1,
            "content": "Mensaje de prueba"
            # Falta owner_id
        }

        with pytest.raises(ValidationError):  # Se espera un error de validación por falta de campo
            MessageOut(**message_data) 
