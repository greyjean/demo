from .models import Url, User



def increment_url(perma_url):
  url = Url.objects.get(perma_url=perma_url)
  clicks = url.clicks + 1
  url.clicks = clicks
  url.save()
  return True

def load_tweets(id):
  user = User.objects.get(id=id)
  user.update_tweets()
  user.save()
