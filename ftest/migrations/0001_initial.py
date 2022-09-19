# Generated by Django 4.1.1 on 2022-09-19 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('question_with_template', models.CharField(max_length=500)),
                ('options', models.JSONField(default=dict)),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuizUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)),
                ('active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuizSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ftest.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ftest.quizuser')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ftest.question')),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answers', to='ftest.quiz')),
                ('submission', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submission_answers', to='ftest.quizsubmission')),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ftest.question')),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_questions', to='ftest.quiz')),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(through='ftest.QuizQuestion', to='ftest.question'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_quiz', to='ftest.quizuser'),
        ),
    ]
