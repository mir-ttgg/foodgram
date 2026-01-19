#!/usr/bin/env python
"""
Скрипт для проверки работы регистрации пользователя.
Использование: python test_registration.py
"""
import os
import sys
import django
import requests
from datetime import datetime

# Настройка Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')
django.setup()

# Теперь можно импортировать Django модули
from django.contrib.auth import get_user_model

User = get_user_model()

def test_registration():
    """Тестирует регистрацию через API"""
    base_url = os.getenv('API_URL', 'http://localhost:8000')
    
    # Генерируем уникальные данные
    timestamp = int(datetime.now().timestamp())
    test_data = {
        'username': f'testuser_{timestamp}',
        'email': f'test_{timestamp}@example.com',
        'first_name': 'Тест',
        'last_name': 'Пользователь',
        'password': 'testpass123'
    }
    
    print("🧪 Тестирование регистрации пользователя")
    print(f"📡 URL: {base_url}/api/users/")
    print(f"📝 Данные: {test_data['username']}, {test_data['email']}")
    print()
    
    try:
        response = requests.post(
            f'{base_url}/api/users/',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        print(f"📊 Статус ответа: {response.status_code}")
        print(f"📄 Тело ответа: {response.text[:200]}")
        print()
        
        if response.status_code == 201:
            print("✅ УСПЕХ! Регистрация работает корректно")
            # Проверяем, что пользователь создан в БД
            user = User.objects.filter(email=test_data['email']).first()
            if user:
                print(f"✓ Пользователь создан в БД: ID={user.id}, username={user.username}")
                # Удаляем тестового пользователя
                user.delete()
                print("✓ Тестовый пользователь удален")
            return True
        elif response.status_code == 400:
            print("⚠️  400 Bad Request - проверьте данные или логи")
            print(f"   Ошибки: {response.text}")
            return False
        elif response.status_code == 500:
            print("❌ ОШИБКА 500! Проблема на сервере.")
            print("   Проверьте логи Django сервера")
            return False
        else:
            print(f"❓ Неожиданный статус: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ОШИБКА: Не удалось подключиться к серверу")
        print(f"   Убедитесь, что сервер запущен на {base_url}")
        print("   Запустите: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ ОШИБКА: {type(e).__name__}: {e}")
        return False


if __name__ == '__main__':
    success = test_registration()
    sys.exit(0 if success else 1)
