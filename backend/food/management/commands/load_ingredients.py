import json
from pathlib import Path
from django.core.management.base import BaseCommand
from food.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из JSON'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str,
                            default='data/ingredients.json')

    def handle(self, *args, **options):
        file_path = Path(options['path'])
        created = 0
        updated = 0
        skipped = 0

        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            for row_num, item in enumerate(data, start=1):
                try:
                    name = item.get('name', '').strip()
                    unit = item.get('measurement_unit', '').strip()

                    if name:
                        ingredient, created_new = Ingredient.objects.get_or_create(
                            name=name,
                            defaults={'measurement_unit': unit}
                        )
                        if created_new:
                            created += 1
                        else:
                            ingredient.measurement_unit = unit
                            ingredient.save()
                            updated += 1
                    else:
                        skipped += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Элемент {row_num}: {e}'))
                    skipped += 1
        else:
            self.stdout.write(self.style.ERROR('JSON не является массивом'))

        self.stdout.write(self.style.SUCCESS(
            f'Создано: {created}, обновлено: {updated}, пропущено: {skipped}'))
