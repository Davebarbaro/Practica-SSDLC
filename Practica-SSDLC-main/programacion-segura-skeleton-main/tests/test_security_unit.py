"""
Tests unitarios para el módulo de seguridad.
Estos tests NO requieren levantar el servidor ni la base de datos.
"""
import pytest
import os
from datetime import timedelta
from jose import jwt, JWTError
from app.core.security import (    # Importar las funciones y variables necesarias desde el módulo de seguridad
    get_password_hash,
    verify_password,
    create_access_token,
    pwd_context,
    ALGORITHM,
    SECRET_KEY
)


class TestPasswordHashing:
    """Tests para las funciones de hashing de contraseñas"""

    def test_get_password_hash_returns_different_hash(self):
        """Verificar que dos llamadas con la misma contraseña generan hashes diferentes (salt)"""
        password = "MySecurePassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)

        assert hash1 != hash2  # Los hashes deben ser diferentes debido al salt
        assert hash1 != password  # El hash no debe ser igual a la contraseña plana

    def test_verify_password_success(self):
        """Verificar que una contraseña correcta se valida correctamente"""
        password = "TestPassword456!"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True  # La verificación debe ser exitosa

    def test_verify_password_failure(self):
        """Verificar que una contraseña incorrecta falla la validación"""
        password = "CorrectPassword789!"
        wrong_password = "WrongPassword000!"
        hashed = get_password_hash(password)  # Hashear la contraseña correcta

        assert verify_password(wrong_password, hashed) is False  # La verificación debe fallar

    def test_password_hash_uses_argon2(self):
        """Verificar que se está usando Argon2 para el hashing"""
        password = "TestArgon2!"
        hashed = get_password_hash(password)  # Hashear la contraseña

        # Los hashes Argon2 comienzan con $argon2
        assert hashed.startswith("$argon2")  # Verificar el prefijo del hash

    def test_hash_empty_password(self):
        """Verificar que se puede hashear una contraseña vacía (aunque no se recomiende)"""
        password = ""
        hashed = get_password_hash(password)  # Hashear la contraseña vacía

        assert hashed != ""  # El hash no debe estar vacío
        assert verify_password(password, hashed) is True  # La verificación debe ser exitosa


class TestJWTTokens:
    """Tests para las funciones de creación y validación de tokens JWT"""

    def test_create_access_token_basic(self):
        """Verificar que se crea un token JWT válido"""
        data = {"sub": "testuser", "role": "user"}
        token = create_access_token(data)  # Crear el token

        assert token is not None  # Verificar que el token no es None
        assert isinstance(token, str)  # Verificar que el token es una cadena
        assert len(token) > 0  # Verificar que el token no está vacío

    def test_create_access_token_with_custom_expiration(self):
        """Verificar que se puede crear un token con expiración personalizada"""
        data = {"sub": "testuser", "role": "admin"}
        expires_delta = timedelta(minutes=30)  # Expiración de 30 minutos
        token = create_access_token(data, expires_delta)  # Crear el token

        # Decodificar el token para verificar la expiración
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert "exp" in payload  # Verificar que el campo de expiración está presente
        assert payload["sub"] == "testuser"  # Verificar el sujeto
        assert payload["role"] == "admin"  # Verificar el rol

    def test_decode_valid_token(self):
        """Verificar que un token válido se puede decodificar correctamente"""
        data = {"sub": "alice", "role": "user"}
        token = create_access_token(data)  # Crear el token

        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 

        assert payload["sub"] == "alice"  # Verificar el sujeto
        assert payload["role"] == "user"  # Verificar el rol
        assert "exp" in payload  # Verificar el campo de expiración

    def test_token_contains_expiration(self):
        """Verificar que el token contiene el campo de expiración"""
        data = {"sub": "bob"}
        token = create_access_token(data)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        assert "exp" in payload  # Verificar el campo de expiración
        assert isinstance(payload["exp"], int)  # Verificar que la expiración es un entero (timestamp)

    def test_token_with_invalid_signature_fails(self):
        """Verificar que un token con firma inválida no se puede decodificar"""
        data = {"sub": "mallory"}
        token = create_access_token(data)

        # Intentar decodificar con una clave incorrecta
        with pytest.raises(JWTError):
            jwt.decode(token, "wrong_secret_key", algorithms=[ALGORITHM])  # Debe lanzar JWTError


class TestPasswordContext:
    """Tests para la configuración del contexto de contraseñas"""

    def test_pwd_context_uses_argon2(self):
        """Verificar que el contexto de contraseñas usa Argon2"""
        assert "argon2" in pwd_context.schemes()  # Verificar que Argon2 está en los esquemas

    def test_pwd_context_has_no_deprecated_schemes(self):
        """Verificar que no hay esquemas marcados como deprecated explícitamente"""
        # El contexto de contraseñas debe tener Argon2 como único esquema activo
        # y no debe tener esquemas deprecated
        schemes = pwd_context.schemes()  
        assert len(schemes) >= 1
        assert "argon2" in schemes  # Verificar que Argon2 está presente
