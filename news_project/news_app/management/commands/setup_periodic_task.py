
# # from django_celery_beat.models import IntervalSchedule, PeriodicTask

# # # Use Django shell or add this to a Django data migration or startup script
# # schedule, created = IntervalSchedule.objects.get_or_create(
# #     every=1,
# #     period=IntervalSchedule.HOURS
# # )

# # PeriodicTask.objects.create(
# #     interval=schedule,
# #     name='Fetch news every hour',
# #     task='news_app.tasks.fetch_news_task'
# # )


# from django_celery_beat.models import IntervalSchedule, PeriodicTask

# # Create or get the interval schedule for every 5 minutes
# schedule, created = IntervalSchedule.objects.get_or_create(
#     every=5,
#     period=IntervalSchedule.MINUTES
# )

# # Create or update the periodic task with the new schedule
# PeriodicTask.objects.update_or_create(
#     name='Fetch news every 5 minutes',
#     defaults={
#         'interval': schedule,
#         'task': 'news_app.tasks.fetch_news_task'
#     }
# )
