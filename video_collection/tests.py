from django.test import TestCase
from django.urls import reverse
# Database
from .models import Video


class TestHomePageMessage(TestCase):
    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')  # Url to home page
        # Make a request to the home page from the client side. The value for the response will be the status code: e.g( <HttpResponse status_code=200, "text/html; charset=utf-8">)
        response = self.client.get(url)
        print('Status Code: ', response)

        self.assertContains(response, "The Weeknd")

    # Testing adding video to video list

    def test_add_video(self):

        # Example data of a YT video data input
        valid_video = {
            'name': "“I Was Never There” by The Weeknd but heartbroken in your loft.",
            'url': 'https://www.youtube.com/watch?v=wtlN-eNmjzI',
            'notes': 'This will be me soon in the future...'
        }

        # Make a POST request to add video
        # Note: If the post request was successful, it will send back a 200 status code. However, in our original code, we are redirecting, which will give us the status code 302. The tests doesn't know that, so we need to give the response to follow that redirection
        url = reverse('add_video')
        response = self.client.post(url, data=valid_video, follow=True)

        print(f'Response POST Status: {response}')

        # Assert template is used after the POST request was made, as in the original function in views.add, we are redirecting to the video_list.html
        self.assertTemplateUsed('video_collection/video_list.html')

        # In the video list that was redirected, is the video that we added through the POST method, does the video_list contains that video?

        # Video Title Name
        self.assertContains(
            response, "“I Was Never There” by The Weeknd but heartbroken in your loft.")

        # Video Url
        self.assertContains(
            response, 'https://www.youtube.com/watch?v=wtlN-eNmjzI')

        # Video Notes
        self.assertContains(response, 'This will be me soon in the future...')

        # Check the django's db to see if the video contains this?
        video_count = Video.objects.count()

        # Check to see of there is 1 video object in the db
        self.assertEqual(1, video_count)

        video = Video.objects.first()  # Getting the First object from the db

        # Check if the video name from the db is same as the testing value name
        self.assertEqual(
            '“I Was Never There” by The Weeknd but heartbroken in your loft.', video.name)

        # Video URL
        self.assertEqual(
            'https://www.youtube.com/watch?v=wtlN-eNmjzI', video.url)

        # Notes
        self.assertEqual('This will be me soon in the future...', video.notes)

        # Video ID
        self.assertEqual('wtlN-eNmjzI', video.video_id)

    def test_invalid_video_url_added(self):
        # List of invalid urls
        invalid_video_urls = [
            'https://www.youtube.com/watch',  'https://www.youtube.com/watch?', 'https://www.youtube.com/watch?abc=1234', 'https://www.youtube.com/watch?v=',
            'https://github.com',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=fdfads343'
        ]

        for invalid_video_url in invalid_video_urls:
            new_video = {
                'name': 'example',
                'url': invalid_video_url,
                'notes': 'example notes'
            }

            url = reverse('add_video')  # Url will be the add video site

            # Adding invalid new video
            response = self.client.post(url, data=new_video)

            # Assert that the template was used
            self.assertTemplateUsed('video_collection/add.html')

            # The messages that was being used to display mini messages for warning, info, etc
            messages = response.context['messages']

            # Extract that messages' message
            message_text = [message.message for message in messages]

            # Look for a string inside a list of strings
            self.assertIn('Invalid Youtube URL', message_text)
            self.assertIn('Please check data entered.', message_text)


class TestVideoList(TestCase):
    pass


class TestVideoSearch(TestCase):
    pass


class TestVideoModel(TestCase):
    pass
