from django.contrib.syndication.views import Feed

class UpcommingEventsFeed(Feed):
    title = "Techism - IT-Events in Muenchen"
    link = "/events/"
    description = "Upcomming events in Munich"

    def items(self):
        return []

    def item_title(self, item):
        return "title"

    def item_description(self, item):
        return "description"

