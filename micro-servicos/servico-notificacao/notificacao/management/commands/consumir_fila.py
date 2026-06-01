from django.core.management.base import BaseCommand
from notificacao.consumer import consumir


class Command(BaseCommand):
    help = 'Consome mensagens da fila RabbitMQ e registra notificações de cozinha'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando worker da fila notificacao_cozinha...'))
        consumir()
