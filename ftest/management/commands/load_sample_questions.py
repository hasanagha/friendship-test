import json
from django.core.management import BaseCommand

from ftest.models import Question


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            f = open('questions.json', 'r')
        except OSError:
            exit('File not found')

        data = json.loads(f.read())

        for item in data:
            item_question = item.get('question', None)

            if item_question:
                record, created = Question.objects.get_or_create(question=item['question'])

                record.question_with_template = item.get('question_with_template', item_question)
                record.options = item.get('options', [])

                print(f'{"Adding" if created else "Updating"}: {item_question}')

                record.save()
