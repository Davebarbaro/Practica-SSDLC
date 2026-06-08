import httpx, pytest

BASE = "http://127.0.0.1:8000"
# Prueba de registro y login de usuario
@pytest.mark.asyncio
async def test_register_and_login(): #se define la funcion de prueba
    async with httpx.AsyncClient(base_url=BASE) as client:     #se crea un cliente parea hacer peticiones HTTP 
        r = await client.post("/auth/register", json={"username":"ali","password":"Password123!","email":"alic@example.com"})
        assert r.status_code in (200,201)
        r = await client.post("/auth/login", data={"username":"ali","password":"Password123!"})
        assert r.status_code == 200
        token = r.json()["access_token"]  # Se obtiene el token de acceso
        assert token    
