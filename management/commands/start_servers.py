from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    help = 'Starts the Django development server and Flask server'

    def handle(self, *args, **options):
        # Start Django development server
        self.stdout.write(self.style.SUCCESS('Starting Django development server...'))
        django_server_process = subprocess.Popen(['python', 'manage.py', 'runserver'])

        # Start Flask server
        self.stdout.write(self.style.SUCCESS('Starting Flask server...'))
        flask_server_process = subprocess.Popen(['python', 'NLP/src/TFIDF_Approach/app.py'])  # Adjust path as needed

        try:
            # Wait for servers to finish
            django_server_process.wait()
            flask_server_process.wait()
        except KeyboardInterrupt:
            # Handle keyboard interrupt
            django_server_process.terminate()
            flask_server_process.terminate()

        self.stdout.write(self.style.SUCCESS('Servers have been stopped.'))

