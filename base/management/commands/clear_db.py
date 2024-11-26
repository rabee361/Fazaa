from django.core.management.base import BaseCommand, CommandError



# class ClearDB(BaseCommand):
#     help = "Clear the database"

#     def add_arguments(self, parser):
#         parser.add_argument("poll_ids", nargs="+", type=int)

#     def handle(self, *args, **options):
            
#             self.stdout.write(
#                 self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
#             )